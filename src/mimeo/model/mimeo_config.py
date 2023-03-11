import json

from mimeo.model.exceptions import (UnsupportedOutputDirection,
                                    UnsupportedOutputFormat)


class MimeoConfig:

    OUTPUT_FORMAT_KEY = "output_format"
    OUTPUT_DETAILS_KEY = "output_details"
    XML_DECLARATION_KEY = "xml_declaration"
    INDENT_KEY = "indent"
    TEMPLATES_KEY = "_templates_"

    SUPPORTED_OUTPUT_FORMATS = ("xml",)

    def __init__(self, config_path: str):
        config = MimeoConfig.__get_config(config_path)
        self.output_format = MimeoConfig.__get_output_format(config)
        self.output_details = MimeoOutputDetails(self.output_format, config.get(self.OUTPUT_DETAILS_KEY, {}))
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


class MimeoOutputDetails:
    
    DIRECTION_KEY = "direction"
    DIRECTORY_PATH_KEY = "directory_path"
    FILE_NAME_KEY = "file_name"

    SUPPORTED_OUTPUT_DIRECTIONS = ("stdout", "file")

    def __init__(self, output_format: str, output_details: dict):
        self.direction = MimeoOutputDetails.__get_direction(output_details)
        self.directory_path = MimeoOutputDetails.__get_directory_path(self.direction, output_details)
        self.file_name_tmplt = MimeoOutputDetails.__get_file_name_template(self.direction, output_details, output_format)

    @staticmethod
    def __get_direction(output_details):
        direction = output_details.get(MimeoOutputDetails.DIRECTION_KEY, "file")
        if direction in MimeoOutputDetails.SUPPORTED_OUTPUT_DIRECTIONS:
            return direction
        else:
            raise UnsupportedOutputDirection(f"Provided direction ({direction}) is not supported!")

    @staticmethod
    def __get_directory_path(direction: str, output_details: dict):
        if direction == "file":
            return output_details.get(MimeoOutputDetails.DIRECTORY_PATH_KEY, "mimeo-output")

    @staticmethod
    def __get_file_name_template(direction: str, output_details: dict, output_format: str):
        if direction == "file":
            file_name = output_details.get(MimeoOutputDetails.FILE_NAME_KEY, "mimeo-output")
            return f"{file_name}-{'{}'}.{output_format}"
