"""The Mimeo Main module.

This module provides a CLI interface for the Mimeo.
It exports a single function:
    * main()
        Execute a Mimeo Job using CLI.
"""
from mimeo.cli import MimeoJob
from mimeo.logging import setup_logging


def main():
    """Execute a Mimeo Job using CLI."""
    setup_logging()
    MimeoJob().run()


if __name__ == '__main__':
    main()
