"""The Mimeo module.

This module is a main module providing the most high level class
in Mimeo:
    * Mimeograph
        A class responsible for the Mimeo processing.
"""
from __future__ import annotations

import logging

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
    process()
        Process the Mimeo Configuration (generate data and consume).
    """

    @staticmethod
    async def process(
            mimeo_config: MimeoConfig,
    ):
        """Process the Mimeo Configuration (generate data and consume).

        Parameters
        ----------
        mimeo_config: MimeoConfig
            A Mimeo Configuration to process
        """
        generator = GeneratorFactory.get_generator(mimeo_config)
        consumer = ConsumerFactory.get_consumer(mimeo_config)
        logger.info("Starting data generation")
        with MimeoContextManager(mimeo_config):
            data = generator.generate(mimeo_config.templates)
            data_str = (generator.stringify(data_unit) for data_unit in data)
            await consumer.consume(data_str)
        logger.info("Data has been processed")
