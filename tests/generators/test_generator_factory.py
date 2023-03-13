import pytest

from mimeo.config import MimeoConfig
from mimeo.exceptions import UnsupportedOutputFormat
from mimeo.generators import GeneratorFactory, XMLGenerator


def test_generator_factory_for_xml():
    config = {
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }
    mimeo_config = MimeoConfig(config)
    generator = GeneratorFactory.get_generator(mimeo_config)
    assert isinstance(generator, XMLGenerator)


def test_generator_factory_for_unsupported_format():
    config = {
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }
    mimeo_config = MimeoConfig(config)
    mimeo_config.output_format = "unsupported_format"

    with pytest.raises(UnsupportedOutputFormat) as err:
        GeneratorFactory.get_generator(mimeo_config)

    assert err.value.args[0] == "Provided format [unsupported_format] is not supported!"
