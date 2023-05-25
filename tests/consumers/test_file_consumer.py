import shutil
from pathlib import Path

import pytest

from mimeo.config import MimeoConfigFactory
from mimeo.consumers import ConsumerFactory
from mimeo.context import MimeoContextManager
from mimeo.generators import GeneratorFactory


@pytest.fixture(autouse=True)
def _teardown():
    yield
    # Teardown
    shutil.rmtree("test_file_consumer-dir")


@pytest.mark.asyncio()
async def test_consume():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
            "directory_path": "test_file_consumer-dir",
            "file_name": "test-output",
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {},
                },
            },
        ],
    }
    mimeo_config = MimeoConfigFactory.parse(config)
    consumer = ConsumerFactory.get_consumer(mimeo_config)
    assert consumer.directory == "test_file_consumer-dir"
    assert consumer.output_path_tmplt == "test_file_consumer-dir/test-output-{}.xml"

    with MimeoContextManager(mimeo_config):
        generator = GeneratorFactory.get_generator(mimeo_config)
        data = [generator.stringify(root)
                for root in generator.generate(mimeo_config.templates)]

        assert not Path("test_file_consumer-dir").exists()

        await consumer.consume(data)
        assert Path("test_file_consumer-dir").exists()
        assert Path("test_file_consumer-dir/test-output-1.xml").exists()
        assert Path("test_file_consumer-dir/test-output-2.xml").exists()

        for i in range(1, 3):
            file_path = f"test_file_consumer-dir/test-output-{i}.xml"
            with Path(file_path).open() as file_content:
                assert file_content.readline() == "<SomeEntity />"

