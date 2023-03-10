from generators import GeneratorFactory
from model.mimeo_config import MimeoConfig


class Mimeograph:

    def __init__(self, config_path):
        self.mimeo_config = MimeoConfig(config_path)
        self.__generator = GeneratorFactory.get_generator(self.mimeo_config.output_format)

    def produce(self):
        for data in self.__generator.generate(self.mimeo_config.templates):
            data_str = self.__generator.stringify(data, self.mimeo_config)
            print(data_str)