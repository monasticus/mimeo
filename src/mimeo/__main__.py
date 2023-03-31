import json
import logging
from argparse import ArgumentParser

from mimeo import Mimeograph
from mimeo.config import MimeoConfig
from mimeo.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class MimeoArgumentParser(ArgumentParser):

    def __init__(self):
        super().__init__(
            prog="mimeo",
            description="Generate data based on a template")
        self.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s v0.1.1")
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
            choices=["file", "stdout", "http"],
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
        mimeo_config_args.add_argument(
            "--http-method",
            type=str,
            metavar="METHOD",
            help="overwrite the output_details/method property")
        mimeo_config_args.add_argument(
            "--http-protocol",
            type=str,
            metavar="PROTOCOL",
            help="overwrite the output_details/protocol property")
        mimeo_config_args.add_argument(
            "--http-auth",
            type=str,
            metavar="AUTH",
            help="overwrite the output_details/auth property")
        mimeo_config_args.add_argument(
            "-H",
            "--http-host",
            type=str,
            metavar="HOST",
            help="overwrite the output_details/host property")
        mimeo_config_args.add_argument(
            "-p",
            "--http-port",
            type=str,
            metavar="HOST",
            help="overwrite the output_details/port property")
        mimeo_config_args.add_argument(
            "-e",
            "--http-endpoint",
            type=str,
            metavar="HOST",
            help="overwrite the output_details/endpoint property")
        mimeo_config_args.add_argument(
            "-u",
            "--http-user",
            type=str,
            metavar="USERNAME",
            help="overwrite the output_details/username property")

        logging_args = self.add_argument_group("Logging arguments")
        logging_args_excl = logging_args.add_mutually_exclusive_group()
        logging_args_excl.add_argument(
            "--silent",
            action="store_true",
            help="disable INFO logs")
        logging_args_excl.add_argument(
            "--debug",
            action="store_true",
            help="enable DEBUG mode")
        logging_args_excl.add_argument(
            "--fine",
            action="store_true",
            help="enable FINE mode")


def main():
    mimeo_parser = MimeoArgumentParser()
    args = mimeo_parser.parse_args()
    if args.silent:
        logging.getLogger("mimeo").setLevel(logging.WARNING)
    elif args.debug:
        logging.getLogger("mimeo").setLevel(logging.DEBUG)
    elif args.fine:
        logging.getLogger("mimeo").setLevel(logging.FINE)

    logger.info("Starting Mimeo job")
    for path in args.paths:
        logger.info(f"Data generation from Mimeo Config: {path}")
        mimeo_config = get_config(path, args)
        Mimeograph(mimeo_config).produce()


def get_config(config_path, args):
    with open(config_path) as config_file:
        config = json.load(config_file)
        if args.xml_declaration is not None:
            xml_declaration = args.xml_declaration.lower() == "true"
            logger.fine(f"Overwriting xml_declaration to [{xml_declaration}]")
            config[MimeoConfig.XML_DECLARATION_KEY] = xml_declaration
        if args.indent is not None:
            logger.fine(f"Overwriting indent to [{args.indent}]")
            config[MimeoConfig.INDENT_KEY] = args.indent
        if args.output is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY, args.output)
        if args.directory is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_DIRECTORY_PATH_KEY, args.directory)
        if args.file is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_FILE_NAME_KEY, args.file)
        if args.http_method is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_METHOD, args.http_method)
        if args.http_protocol is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_PROTOCOL, args.http_protocol)
        if args.http_auth is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_AUTH, args.http_auth)
        if args.http_host is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_HOST, args.http_host)
        if args.http_port is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_PORT, args.http_port)
        if args.http_endpoint is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_ENDPOINT, args.http_endpoint)
        if args.http_user is not None:
            customize_output_details(config, MimeoConfig.OUTPUT_DETAILS_USERNAME, args.http_user)
    mimeo_config = MimeoConfig(config)
    logger.debug(f"Mimeo Config: {mimeo_config}")
    return mimeo_config


def customize_output_details(config, key, value):
    if config.get(MimeoConfig.OUTPUT_DETAILS_KEY) is None:
        config[MimeoConfig.OUTPUT_DETAILS_KEY] = {}

    logger.fine(f"Overwriting output details' {key} to [{value}]")
    config[MimeoConfig.OUTPUT_DETAILS_KEY][key] = value


if __name__ == '__main__':
    main()
