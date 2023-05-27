from mimeo.config import MimeoConfigFactory
from mimeo.config.exc import UnsupportedPropertyValueError
from mimeo.consumers import (ConsumerFactory, FileConsumer, HttpConsumer,
                             RawConsumer)
from tests.utils import assert_throws


def test_get_consumer_for_file_direction():
    config = {
        "output": {
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
    mimeo_config = MimeoConfigFactory.parse(config)
    generator = ConsumerFactory.get_consumer(mimeo_config)
    assert isinstance(generator, FileConsumer)


def test_get_consumer_for_stdout_direction():
    config = {
        "output": {
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
    mimeo_config = MimeoConfigFactory.parse(config)
    generator = ConsumerFactory.get_consumer(mimeo_config)
    assert isinstance(generator, RawConsumer)


def test_get_consumer_for_http_direction():
    config = {
        "output": {
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
    mimeo_config = MimeoConfigFactory.parse(config)
    generator = ConsumerFactory.get_consumer(mimeo_config)
    assert isinstance(generator, HttpConsumer)


@assert_throws(err_type=UnsupportedPropertyValueError,
               msg="Provided direction [{direction}] is not supported! "
                   "Supported values: [{values}].",
               direction="unsupported_direction", values="stdout, file, http")
def test_get_consumer_for_unsupported_format():
    config = {
        "output": {
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
    mimeo_config = MimeoConfigFactory.parse(config)
    mimeo_config.output.direction = "unsupported_direction"

    ConsumerFactory.get_consumer(mimeo_config)
