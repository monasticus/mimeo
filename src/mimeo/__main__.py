from sys import argv

from mimeo import Mimeograph


def main(argv: list):
    Mimeograph(argv[0]).produce()


if __name__ == '__main__':
    main(argv[1:])
