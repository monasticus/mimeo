"""The Mimeo module.

This module is a main module providing the most high level class
in Mimeo:
    * Mimeograph
        A class responsible for the Mimeo processing.
"""
from __future__ import annotations

import asyncio
import logging
import queue
import xml.etree.ElementTree as ElemTree
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Iterator

from mimeo.config.mimeo_config import MimeoConfig
from mimeo.consumers import ConsumerFactory
from mimeo.context import MimeoContextManager
from mimeo.generators import GeneratorFactory

logger = logging.getLogger(__name__)


class Mimeograph:
    """A class responsible for the Mimeo processing.

    Based on the Mimeo Configuration it instantiates generator and
    consumer to produce desired data.

    Methods
    -------
    generate(
        mimeo_config: MimeoConfig,
        stringify: bool = False,
    ) -> Iterator[ElemTree.Element | dict | str]
        Generate data from the Mimeo Configuration.

    consume(
        mimeo_config: MimeoConfig,
        data: Iterable,
    )
        Consume data generated from the Mimeo Configuration.

    process(
        mimeo_config: MimeoConfig,
    )
        Process the Mimeo Configuration (generate data and consume).
    """

    _CONSUMER_THREADS: int = 5

    def __enter__(self):
        self._generate_queue = queue.Queue()
        self._consume_queue = queue.Queue()
        self._generate_executor = ThreadPoolExecutor(max_workers=1,
                                                     thread_name_prefix="generate")
        self._consume_executor = ThreadPoolExecutor(max_workers=self._CONSUMER_THREADS,
                                                    thread_name_prefix="consume")

        self._generate_executor.submit(self._start_generate)
        for _ in range(self._CONSUMER_THREADS):
            self._consume_executor.submit(self._start_consume)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._consume_queue.join()
        self._generate_queue.join()
        self._generate_executor.shutdown(wait=True)
        self._consume_executor.shutdown(wait=True)

    def _start_generate(self):
        while True:
            logger.fine("Getting a config for data generation from queue")
            mimeo_config = self._generate_queue.get()
            if mimeo_config is None:
                logger.fine("Closing config generation")
                for _ in range(self._CONSUMER_THREADS):
                    self._consume_queue.put((None, None))
                self._generate_queue.task_done()
                break
            data = list(self.generate(mimeo_config, stringify=True))
            logger.info("Putting data to consume to queue")
            self._consume_queue.put((mimeo_config, data))
            self._generate_queue.task_done()

    def _start_consume(self):
        while True:
            logger.fine("Getting data to consume from queue")
            mimeo_config, data = self._consume_queue.get()
            if mimeo_config is None and data is None:
                logger.fine("Closing data consumption")
                self._consume_queue.task_done()
                break
            self.consume(mimeo_config, data)
            self._consume_queue.task_done()

    def submit(self, mimeo_config: MimeoConfig | None):
        logger.fine("Putting a config for data generation into queue")
        self._generate_queue.put(mimeo_config)

    @classmethod
    def process(
            cls,
            mimeo_config: MimeoConfig,
    ):
        """Process the Mimeo Configuration (generate data and consume).

        Parameters
        ----------
        mimeo_config: MimeoConfig
            A Mimeo Configuration to process
        """
        data = cls.generate(mimeo_config, stringify=True)
        cls.consume(mimeo_config, data)

        logger.info("Data has been processed")

    @classmethod
    def generate(
            cls,
            mimeo_config: MimeoConfig,
            stringify: bool = False,
    ) -> Iterator[ElemTree.Element | dict | str]:
        """Generate data from the Mimeo Configuration.

        Parameters
        ----------
        mimeo_config: MimeoConfig
            A Mimeo Configuration for data generation
        stringify: bool
            Indicate if data should be stringified

        Returns
        -------
        Iterator[ElemTree.Element | dict | str]
            Iterator for generated data
        """
        generator = GeneratorFactory.get_generator(mimeo_config)
        logger.info("Starting data generation")
        with MimeoContextManager(mimeo_config):
            for data in generator.generate(mimeo_config.templates):
                yield data if not stringify else generator.stringify(data)

    @classmethod
    def consume(
            cls,
            mimeo_config: MimeoConfig,
            data: Iterable,
    ):
        """Consume data generated from the Mimeo Configuration.

        Parameters
        ----------
        mimeo_config: MimeoConfig
            A Mimeo Configuration for data generation
        data: Iterable
            Data to consume
        """
        consumer = ConsumerFactory.get_consumer(mimeo_config)
        asyncio.run(consumer.consume(data))
