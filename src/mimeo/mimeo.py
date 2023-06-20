"""The Mimeo module.

This module is a main module providing the most high level class
in Mimeo:
    * Mimeograph
        A class responsible for the Mimeo processing.
"""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ElemTree
from typing import Iterator, Iterable

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

    _GENERATORS = {}

    @classmethod
    async def process(
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
        await cls.consume(mimeo_config, data)

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
    async def consume(
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
        await consumer.consume(data)
