from mimeo.config.exc import UnsupportedPropertyValue
from mimeo.config.mimeo_config import MimeoConfig
from mimeo.generators import Generator, XMLGenerator


class GeneratorFactory:

    XML = MimeoConfig.OUTPUT_FORMAT_XML

    @staticmethod
    def get_generator(mimeo_config: MimeoConfig) -> Generator:
        output_format = mimeo_config.output_format
        if output_format == GeneratorFactory.XML:
            return XMLGenerator(mimeo_config)
        else:
            raise UnsupportedPropertyValue(MimeoConfig.OUTPUT_FORMAT_KEY,
                                           output_format,
                                           MimeoConfig.SUPPORTED_OUTPUT_FORMATS)
