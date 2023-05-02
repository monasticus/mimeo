"""The Mimeo module.

This module is a main module providing the most high level class
in Mimeo:
    * Mimeograph
        A class responsible for the Mimeo processing.
"""
from mimeo.config.mimeo_config import MimeoConfig
from mimeo.consumers import ConsumerFactory
from mimeo.generators import GeneratorFactory


class Mimeograph:
    """A class responsible for the Mimeo processing.

    Based on the Mimeo Configuration it instantiates generator and
    consumer to produce desired data.

    Methods
    -------
    process()
        Process the Mimeo Configuration (generate data and consume).
    """

    def __init__(self, mimeo_config: MimeoConfig):
        self._mimeo_config = mimeo_config
        self._generator = GeneratorFactory.get_generator(self._mimeo_config)
        self._consumer = ConsumerFactory.get_consumer(self._mimeo_config)

    def process(self):
        """Process the Mimeo Configuration (generate data and consume)."""
        for data in self._generator.generate(self._mimeo_config.templates):
            data_str = self._generator.stringify(data, self._mimeo_config)
            self._consumer.consume(data_str)
