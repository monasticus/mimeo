from mimeo.config import MimeoConfigFactory
from mimeo.config.exc import UnsupportedPropertyValueError
from mimeo.generators import GeneratorFactory, JSONGenerator, XMLGenerator
from tests.utils import assert_throws


def test_generator_factory_for_xml():
    config = {
        "output": {
            "format": "xml",
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
    mimeo_config = MimeoConfigFactory.parse(config)
    generator = GeneratorFactory.get_generator(mimeo_config)
    assert isinstance(generator, XMLGenerator)


def test_generator_factory_for_json():
    config = {
        "output": {
            "format": "json",
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
    mimeo_config = MimeoConfigFactory.parse(config)
    generator = GeneratorFactory.get_generator(mimeo_config)
    assert isinstance(generator, JSONGenerator)


@assert_throws(err_type=UnsupportedPropertyValueError,
               msg="Provided format [{format}] is not supported! "
                   "Supported values: [{values}].",
               format="unsupported_format", values="xml, json")
def test_generator_factory_for_unsupported_format():
    config = {
        "output": {
            "format": "xml",
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
    mimeo_config = MimeoConfigFactory.parse(config)
    mimeo_config.output.format = "unsupported_format"

    GeneratorFactory.get_generator(mimeo_config)
