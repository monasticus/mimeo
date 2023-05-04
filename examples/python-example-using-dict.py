#!/usr/bin/python3

from mimeo import MimeoConfig, Mimeograph

config = {
  "_templates_": [
    {
      "count": 30,
      "model": {
        "SomeEntity": {
          "ChildNode1": 1,
          "ChildNode2": "value-2",
          "ChildNode3": True
        }
      }
    }
  ]
}
mimeo_config = MimeoConfig(config)
Mimeograph(mimeo_config).process()
