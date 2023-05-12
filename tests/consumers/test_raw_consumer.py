import sys
from io import StringIO

import pytest

from mimeo.config import MimeoConfig
from mimeo.consumers import ConsumerFactory
from mimeo.context import MimeoContextManager
from mimeo.generators import GeneratorFactory


@pytest.fixture(autouse=True)
def _teardown():
    yield
    # Teardown
    sys.stdout = sys.__stdout__


@pytest.mark.asyncio()
async def test_consume():
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
    mimeo_config = MimeoConfig(config)
    consumer = ConsumerFactory.get_consumer(mimeo_config)

    with MimeoContextManager(mimeo_config):
        generator = GeneratorFactory.get_generator(mimeo_config)
        data = [generator.stringify(root)
                for root in generator.generate(mimeo_config.templates)]

        output_redirection = StringIO()
        sys.stdout = output_redirection

        await consumer.consume(data)

        assert output_redirection.getvalue() == "<SomeEntity />\n" * 5
