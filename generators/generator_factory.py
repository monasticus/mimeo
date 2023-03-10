from generators import Generator, XMLGenerator
from model.mimeo_config import UnsupportedOutputFormat


class GeneratorFactory:

    XML = "xml"

    @staticmethod
    def get_generator(output_format) -> Generator:
        if output_format == GeneratorFactory.XML:
            return XMLGenerator()
        else:
            raise UnsupportedOutputFormat(f"Provided format ({output_format}) is not supported!")
