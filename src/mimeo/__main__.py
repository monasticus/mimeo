import json
from argparse import ArgumentParser

from mimeo import Mimeograph
from mimeo.config import MimeoConfig


def main():
    parser = ArgumentParser(prog="mimeo", description="Generate data based on a simple template")
    parser.add_argument("paths", nargs="+", type=str, help="take paths to Mimeo Configurations")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v1.0.2")
    args = parser.parse_args()
    for path in args.paths:
        mimeo_config = get_config(path)
        Mimeograph(mimeo_config).produce()


def get_config(config_path):
    with open(config_path) as config_file:
        config = json.load(config_file)
    return MimeoConfig(config)


if __name__ == '__main__':
    main()
