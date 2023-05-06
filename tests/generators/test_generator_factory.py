from mimeo.config import MimeoConfig
from mimeo.config.exc import UnsupportedPropertyValue
from mimeo.generators import GeneratorFactory, XMLGenerator
from tests.utils import assert_throws


def test_generator_factory_for_xml():
    config = {
        "output_details": {
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
    mimeo_config = MimeoConfig(config)
    generator = GeneratorFactory.get_generator(mimeo_config)
    assert isinstance(generator, XMLGenerator)


@assert_throws(err_type=UnsupportedPropertyValue,
               message="Provided format [{format}] is not supported! Supported values: [{values}].",
               params={"format": "unsupported_format",
                       "values": "xml"})
def test_generator_factory_for_unsupported_format():
    config = {
        "output_details": {
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
    mimeo_config = MimeoConfig(config)
    mimeo_config.output_details.format = "unsupported_format"

    GeneratorFactory.get_generator(mimeo_config)
