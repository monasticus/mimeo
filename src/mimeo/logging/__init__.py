try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

import logging.config

import yaml
from haggis.logs import add_logging_level

from mimeo import resources as data

from .filters import DetailedFilter, RegularFilter


def setup_logging():
    add_logging_level("FINE", logging.DEBUG - 1)
    with pkg_resources.open_text(data, "logging.yaml") as config_file:
        config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)
