#!/usr/bin/python3
import json
from pathlib import Path

from mimeo import MimeoConfigFactory, Mimeograph

config_path = "examples/1-introduction/01-basic.json"
mimeo_config = MimeoConfigFactory.parse(config_path)
Mimeograph.process(mimeo_config)
