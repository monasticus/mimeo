from http import HTTPStatus

import responses

from mimeo.config import MimeoConfig
from mimeo.consumers import ConsumerFactory
from mimeo.context import MimeoContextManager
from mimeo.generators import GeneratorFactory
from tests import utils


@responses.activate
def test_consume_post():
    config = {
        "format": "xml",
        "output": {
            "direction": "http",
            "host": "localhost",
            "port": 8080,
            "endpoint": "/documents",
            "username": "admin",
            "password": "admin",
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {
                        "Id": "{curr_iter}",
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfig(config)
    consumer = ConsumerFactory.get_consumer(mimeo_config)
    assert consumer.method == "POST"
    assert consumer.url == "http://localhost:8080/documents"

    responses.post(
        consumer.url,
        json={"success": True},
        status=HTTPStatus.OK,
        match=[utils.get_request_body_matcher(["<SomeEntity><Id>1</Id></SomeEntity>",
                                               "<SomeEntity><Id>2</Id></SomeEntity>"])])

    with MimeoContextManager(mimeo_config):
        generator = GeneratorFactory.get_generator(mimeo_config)
        data = [generator.stringify(root)
                for root in generator.generate(mimeo_config.templates)]

        consumer.consume(data)
    # would throw a ConnectionError when any request call doesn't match registered mocks



@responses.activate
def test_consume_put():
    config = {
        "format": "xml",
        "output": {
            "direction": "http",
            "method": "PUT",
            "host": "localhost",
            "port": 8080,
            "endpoint": "/documents",
            "auth": "digest",
            "username": "admin",
            "password": "admin",
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {
                        "Id": "{curr_iter}",
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfig(config)
    consumer = ConsumerFactory.get_consumer(mimeo_config)
    assert consumer.method == "PUT"
    assert consumer.url == "http://localhost:8080/documents"

    responses.put(
        consumer.url,
        json={"success": True},
        status=HTTPStatus.OK,
        match=[utils.get_request_body_matcher(["<SomeEntity><Id>1</Id></SomeEntity>",
                                               "<SomeEntity><Id>2</Id></SomeEntity>"])])

    with MimeoContextManager(mimeo_config):
        generator = GeneratorFactory.get_generator(mimeo_config)
        data = [generator.stringify(root)
                for root in generator.generate(mimeo_config.templates)]

        consumer.consume(data)
    # would throw a ConnectionError when any request call doesn't match registered mocks


@responses.activate
def test_consume_without_port():
    config = {
        "format": "xml",
        "output": {
            "direction": "http",
            "host": "localhost",
            "endpoint": "/documents",
            "username": "admin",
            "password": "admin",
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {
                        "Id": "{curr_iter}",
                    },
                },
            },
        ],
    }
    mimeo_config = MimeoConfig(config)
    consumer = ConsumerFactory.get_consumer(mimeo_config)
    assert consumer.method == "POST"
    assert consumer.url == "http://localhost/documents"

    responses.post(
        consumer.url,
        json={"success": True},
        status=HTTPStatus.OK,
        match=[utils.get_request_body_matcher(["<SomeEntity><Id>1</Id></SomeEntity>",
                                               "<SomeEntity><Id>2</Id></SomeEntity>"])])

    with MimeoContextManager(mimeo_config):
        generator = GeneratorFactory.get_generator(mimeo_config)
        data = [generator.stringify(root)
                for root in generator.generate(mimeo_config.templates)]

        consumer.consume(data)
    # would throw a ConnectionError when any request call doesn't match registered mocks
