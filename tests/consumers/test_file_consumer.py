import shutil
from os import path

from mimeo.config import MimeoConfig
from mimeo.consumers import ConsumerFactory
from mimeo.generators import GeneratorFactory


def test_consume():
    config = {
        "output_format": "xml",
        "output_details": {
            "direction": "file",
            "directory_path": "test-dir",
            "file_name": "test-output"
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
    assert consumer.directory == "test-dir"
    assert consumer.output_path_tmplt == "test-dir/test-output-{}.xml"

    generator = GeneratorFactory.get_generator(mimeo_config)
    data = [generator.stringify(root, mimeo_config)
            for root in generator.generate(mimeo_config.templates)]

    assert not path.exists("test-dir")
    consumer.consume(data[0])
    assert path.exists("test-dir")
    assert path.exists("test-dir/test-output-1.xml")
    consumer.consume(data[1])
    assert path.exists("test-dir/test-output-2.xml")

    shutil.rmtree("test-dir")

