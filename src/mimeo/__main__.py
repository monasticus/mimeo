from mimeo.cli import MimeoJob
from mimeo.logging import setup_logging


def main():
    setup_logging()
    MimeoJob().run()


if __name__ == '__main__':
    main()
