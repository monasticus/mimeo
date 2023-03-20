import pytest

from mimeo.config import MimeoConfig
from mimeo.consumers import (ConsumerFactory, FileConsumer, HttpConsumer,
                             RawConsumer)
from mimeo.exceptions import UnsupportedOutputDirection


def test_get_consumer_for_file_direction():
    config = {
        "output_details": {
            "direction": "file"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {}
                }
            }
        ]
    }
    mimeo_config = MimeoConfig(config)
    generator = ConsumerFactory.get_consumer(mimeo_config)
    assert isinstance(generator, FileConsumer)


def test_get_consumer_for_stdout_direction():
    config = {
        "output_details": {
            "direction": "stdout"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {}
                }
            }
        ]
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
            "password": "admin"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {}
                }
            }
        ]
    }
    mimeo_config = MimeoConfig(config)
    generator = ConsumerFactory.get_consumer(mimeo_config)
    assert isinstance(generator, HttpConsumer)


def test_get_consumer_for_unsupported_format():
    config = {
        "output_details": {
            "direction": "stdout"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {}
                }
            }
        ]
    }
    mimeo_config = MimeoConfig(config)
    mimeo_config.output_details.direction = "unsupported_direction"

    with pytest.raises(UnsupportedOutputDirection) as err:
        ConsumerFactory.get_consumer(mimeo_config)

    assert err.value.args[0] == "Provided direction [unsupported_direction] is not supported!"
