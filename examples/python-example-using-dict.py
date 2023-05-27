#!/usr/bin/python3

from mimeo import MimeoConfigFactory, Mimeograph

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
mimeo_config = MimeoConfigFactory.parse(config)
Mimeograph(mimeo_config).process()
