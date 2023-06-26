#!/usr/bin/python3
import json
from pathlib import Path

from mimeo import MimeoConfigFactory, Mimeograph

config_paths = [
    "examples/1-introduction/01-basic.json",
    "examples/1-introduction/02-complex.json",
    "examples/1-introduction/03-output-format-xml.json",
    "examples/1-introduction/04-output-format-json.json",
]

with Mimeograph() as mimeo:
    for config_path in config_paths:
        mimeo_config = MimeoConfigFactory.parse(config_path)
        mimeo.submit((config_path, mimeo_config))
