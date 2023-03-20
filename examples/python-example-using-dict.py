#!/usr/bin/env python3

from mimeo import Mimeograph
from mimeo.config import MimeoConfig

with open(config_path) as config_file:
    config = json.load(config_file)
mimeo_config = MimeoConfig(config)
Mimeograph(mimeo_config).produce()
Mimeograph("examples/config-5.json").produce()
