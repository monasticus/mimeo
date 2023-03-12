from argparse import ArgumentParser

from mimeo import Mimeograph


def main():
    parser = ArgumentParser(prog="mimeo", description="Generate data based on a simple template")
    parser.add_argument("paths", nargs="+", type=str, help="take paths to Mimeo Configurations")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v1.0.2")
    args = parser.parse_args()
    for path in args.paths:
        Mimeograph(path).produce()


if __name__ == '__main__':
    main()
