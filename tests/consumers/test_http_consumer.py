from http import HTTPStatus

import pytest
import responses

from mimeo.config import MimeoConfig
from mimeo.consumers import ConsumerFactory
from mimeo.generators import GeneratorFactory


@responses.activate
def test_consume_post():
    config = {
        "output_format": "xml",
        "output_details": {
            "direction": "http",
            "host": "localhost",
            "port": 8080,
            "endpoint": "/documents",
            "username": "admin",
            "password": "admin"
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {}
                }
            }
        ]
    }
    mimeo_config = MimeoConfig(config)
    consumer = ConsumerFactory.get_consumer(mimeo_config)
    assert consumer.method == "POST"
    assert consumer.url == "http://localhost:8080/documents"

    responses.add(responses.POST, consumer.url, json={"success": True}, status=HTTPStatus.OK)

    generator = GeneratorFactory.get_generator(mimeo_config)
    data = (generator.stringify(root, mimeo_config)
            for root in generator.generate(mimeo_config.templates))

    for root in data:
        resp = consumer.consume(root)
        assert resp.request.method == "POST"
        assert resp.request.body == root
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == {"success": True}


@responses.activate
def test_consume_put():
    config = {
        "output_format": "xml",
        "output_details": {
            "direction": "http",
            "method": "PUT",
            "host": "localhost",
            "port": 8080,
            "endpoint": "/documents",
            "auth": "digest",
            "username": "admin",
            "password": "admin"
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {}
                }
            }
        ]
    }
    mimeo_config = MimeoConfig(config)
    consumer = ConsumerFactory.get_consumer(mimeo_config)
    assert consumer.method == "PUT"
    assert consumer.url == "http://localhost:8080/documents"

    responses.add(responses.PUT, consumer.url, json={"success": True}, status=HTTPStatus.OK)

    generator = GeneratorFactory.get_generator(mimeo_config)
    data = (generator.stringify(root, mimeo_config)
            for root in generator.generate(mimeo_config.templates))

    for root in data:
        resp = consumer.consume(root)
        assert resp.request.method == "PUT"
        assert resp.request.body == root
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == {"success": True}


@responses.activate
def test_consume_without_port():
    config = {
        "output_format": "xml",
        "output_details": {
            "direction": "http",
            "host": "localhost",
            "endpoint": "/documents",
            "username": "admin",
            "password": "admin"
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {}
                }
            }
        ]
    }
    mimeo_config = MimeoConfig(config)
    consumer = ConsumerFactory.get_consumer(mimeo_config)
    assert consumer.method == "POST"
    assert consumer.url == "http://localhost/documents"

    responses.add(responses.POST, consumer.url, json={"success": True}, status=HTTPStatus.OK)

    generator = GeneratorFactory.get_generator(mimeo_config)
    data = (generator.stringify(root, mimeo_config)
            for root in generator.generate(mimeo_config.templates))

    for root in data:
        resp = consumer.consume(root)
        assert resp.request.method == "POST"
        assert resp.request.body == root
        assert resp.status_code == HTTPStatus.OK
        assert resp.json() == {"success": True}

