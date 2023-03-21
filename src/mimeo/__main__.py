import json
from argparse import ArgumentParser

from mimeo import Mimeograph
from mimeo.config import MimeoConfig


class MimeoArgumentParser(ArgumentParser):

    def __init__(self):
        super().__init__(
            prog="mimeo",
            description="Generate data based on a template")
        self.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s v2.4.0")
        self.add_argument(
            "paths",
            nargs="+",
            type=str,
            help="take paths to Mimeo Configurations")

        mimeo_config_args = self.add_argument_group("Mimeo Configuration arguments")
        mimeo_config_args.add_argument(
            "-x",
            "--xml-declaration",
            type=str,
            choices=["true", "false"],
            help="overwrite the xml_declaration property")
        mimeo_config_args.add_argument(
            "-i",
            "--indent",
            type=int,
            help="overwrite the indent property")
        mimeo_config_args.add_argument(
            "-o",
            "--output",
            type=str,
            choices=["file", "stdout"],
            help="overwrite the output_details/direction property")
        mimeo_config_args.add_argument(
            "-d",
            "--directory",
            type=str,
            metavar="DIRECTORY_PATH",
            help="overwrite the output_details/directory_path property")
        mimeo_config_args.add_argument(
            "-f",
            "--file",
            type=str,
            metavar="FILE_NAME",
            help="overwrite the output_details/file_name property")


def main():
    mimeo_parser = MimeoArgumentParser()
    args = mimeo_parser.parse_args()
    for path in args.paths:
        mimeo_config = get_config(path, args)
        Mimeograph(mimeo_config).produce()


def get_config(config_path, args):
    with open(config_path) as config_file:
        config = json.load(config_file)
        if args.xml_declaration is not None:
            config[MimeoConfig.XML_DECLARATION_KEY] = args.xml_declaration.lower() == "true"
        if args.indent is not None:
            config[MimeoConfig.INDENT_KEY] = args.indent
        if args.output is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY, args.output)
        if args.directory is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_DIRECTORY_PATH_KEY, args.directory)
        if args.file is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_FILE_NAME_KEY, args.file)
    return MimeoConfig(config)


def customize_output_details(config, key, value):
    if config.get(MimeoConfig.OUTPUT_DETAILS_KEY) is None:
        config[MimeoConfig.OUTPUT_DETAILS_KEY] = {}

    config[MimeoConfig.OUTPUT_DETAILS_KEY][key] = value


if __name__ == '__main__':
    main()
