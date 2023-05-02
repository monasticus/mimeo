from argparse import ArgumentParser


class MimeoArgumentParser(ArgumentParser):

    def __init__(self):
        super().__init__(
            prog="mimeo",
            description="Generate data based on a template",
            usage="%(prog)s [OPTIONS] paths")
        self.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s v0.4.1")
        self.add_argument(
            "paths",
            nargs="+",
            type=str,
            help="take paths to Mimeo Configuration files")

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
            "-H",
            "--http-host",
            type=str,
            metavar="HOST",
            help="overwrite the output_details/host property")
        mimeo_config_args.add_argument(
            "-p",
            "--http-port",
            type=str,
            metavar="PORT",
            help="overwrite the output_details/port property")
        mimeo_config_args.add_argument(
            "-E",
            "--http-endpoint",
            type=str,
            metavar="ENDPOINT",
            help="overwrite the output_details/endpoint property")
        mimeo_config_args.add_argument(
            "-U",
            "--http-user",
            type=str,
            metavar="USERNAME",
            help="overwrite the output_details/username property")
        mimeo_config_args.add_argument(
            "-P",
            "--http-password",
            type=str,
            metavar="PASSWORD",
            help="overwrite the output_details/password property")
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
            "-e",
            "--http-env",
            type=str,
            metavar="ENVIRONMENT",
            help="overwrite the output_details http properties using a mimeo environment configuration")
        mimeo_config_args.add_argument(
            "--http-envs-file",
            type=str,
            metavar="PATH",
            help=f"use a custom environments file (by default: mimeo.envs.json)")

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
