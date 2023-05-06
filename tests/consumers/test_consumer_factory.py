from mimeo.config import MimeoConfig
from mimeo.config.exc import UnsupportedPropertyValue
from mimeo.consumers import (ConsumerFactory, FileConsumer, HttpConsumer,
                             RawConsumer)
from tests.utils import assert_throws


def test_get_consumer_for_file_direction():
    config = {
        "output_details": {
            "direction": "file",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {},
                },
            },
        ],
    }
    mimeo_config = MimeoConfig(config)
    generator = ConsumerFactory.get_consumer(mimeo_config)
    assert isinstance(generator, FileConsumer)


def test_get_consumer_for_stdout_direction():
    config = {
        "output_details": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {},
                },
            },
        ],
    }
    mimeo_config = MimeoConfig(config)
    generator = ConsumerFactory.get_consumer(mimeo_config)
    assert isinstance(generator, RawConsumer)


def test_get_consumer_for_http_direction():
    config = {
        "output_details": {
            "direction": "http",
            "host": "localhost",
            "port": 8080,
            "endpoint": "/document",
            "username": "admin",
            "password": "admin",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {},
                },
            },
        ],
    }
    mimeo_config = MimeoConfig(config)
    generator = ConsumerFactory.get_consumer(mimeo_config)
    assert isinstance(generator, HttpConsumer)


@assert_throws(err_type=UnsupportedPropertyValue,
               msg="Provided direction [{direction}] is not supported! "
                   "Supported values: [{values}].",
               params={"direction": "unsupported_direction",
                       "values": "stdout, file, http"})
def test_get_consumer_for_unsupported_format():
    config = {
        "output_details": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {},
                },
            },
        ],
    }
    mimeo_config = MimeoConfig(config)
    mimeo_config.output_details.direction = "unsupported_direction"

    ConsumerFactory.get_consumer(mimeo_config)
