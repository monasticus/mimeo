from mimeo.config import MimeoConfigFactory


def test_mimeo_config_from_dict():
    config = {
        "output": {
            "direction": "stdout",
        },
        "vars": {
            "CUSTOM_KEY1": "custom value",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    }

    mimeo_config = MimeoConfigFactory.from_dict(config)
    assert str(mimeo_config) == str(config)
