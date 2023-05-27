#!/usr/bin/python3
import json
from pathlib import Path

from mimeo import MimeoConfigFactory, Mimeograph

with Path("examples/1-introduction/01-basic.json").open() as config_file:
    config = json.load(config_file)
    mimeo_config = MimeoConfigFactory.parse(config)
    Mimeograph(mimeo_config).process()
