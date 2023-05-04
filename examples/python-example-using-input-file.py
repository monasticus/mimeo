#!/usr/bin/python3
import json

from mimeo import MimeoConfig, Mimeograph

with open("examples/1-introduction/01-basic.json") as config_file:
    config = json.load(config_file)
    mimeo_config = MimeoConfig(config)
    Mimeograph(mimeo_config).process()
