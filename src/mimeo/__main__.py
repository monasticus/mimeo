import json
from argparse import ArgumentParser

from mimeo import Mimeograph
from mimeo.config import MimeoConfig


class MimeoArgumentParser(ArgumentParser):

    def __init__(self):
        super().__init__(prog="mimeo", description="Generate data based on a simple template")
        self.add_argument("paths", nargs="+", type=str, help="take paths to Mimeo Configurations")
        self.add_argument("-x", "--xml-declaration", type=str, choices=["true", "false"])
        self.add_argument("-i", "--indent", type=int)
        self.add_argument("-o", "--output", type=str, choices=["file", "stdout"])
        self.add_argument("-v", "--version", action="version", version="%(prog)s v1.0.2")


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
            config[MimeoConfig.OUTPUT_DETAILS_KEY][MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY] = args.output
    return MimeoConfig(config)


if __name__ == '__main__':
    main()
