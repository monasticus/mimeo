import json

from model.exceptions import UnsupportedOutputFormat


class MimeoConfig:

    OUTPUT_FORMAT_KEY = "output_format"
    XML_DECLARATION_KEY = "xml_declaration"
    INDENT_KEY = "indent"
    TEMPLATES_KEY = "_templates_"

    SUPPORTED_OUTPUT_FORMATS = ("xml",)

    def __init__(self, config_path: str):
        config = MimeoConfig.__get_config(config_path)
        self.output_format = MimeoConfig.__get_output_format(config)
        self.xml_declaration = config.get(self.XML_DECLARATION_KEY, False)
        self.indent = config.get(self.INDENT_KEY)
        self.templates = (MimeoTemplate(**template) for template in config.get(self.TEMPLATES_KEY))

    @staticmethod
    def __get_config(config_path):
        with open(config_path) as config_file:
            return json.load(config_file)

    @staticmethod
    def __get_output_format(config):
        output_format = config.get(MimeoConfig.OUTPUT_FORMAT_KEY, "xml")
        if output_format in MimeoConfig.SUPPORTED_OUTPUT_FORMATS:
            return output_format
        else:
            raise UnsupportedOutputFormat(f"Provided format ({output_format}) is not supported!")


class MimeoTemplate:

    def __init__(self, count: int, model: dict):
        self.count = count
        self.model = MimeoModel(model)


class MimeoModel:

    def __init__(self, model: dict):
        self.attributes = model.get("attributes", {})
        self.root_name = next(filter(MimeoModel.__is_not_attributes_key, iter(model)))
        self.root_data = model.get(self.root_name)

    @staticmethod
    def __is_not_attributes_key(dict_key):
        return dict_key != "attributes"
