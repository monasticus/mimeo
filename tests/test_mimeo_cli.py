import json
import shutil
import sys
from os import path
from pathlib import Path

import pytest

import mimeo.__main__ as MimeoCLI


@pytest.fixture(autouse=True)
def default_config():
    return {
        "output_format": "xml",
        "indent": 4,
        "xml_declaration": True,
        "output_details": {
            "direction": "file",
            "directory_path": "test_mimeo_cli-dir/output",
            "file_name": "output-file"
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True
                    }
                }
            }
        ]
    }


@pytest.fixture(autouse=True)
def setup_and_teardown(default_config):
    # Setup
    Path("test_mimeo_cli-dir").mkdir(parents=True, exist_ok=True)
    with open("test_mimeo_cli-dir/config-1.json", "w") as file:
        json.dump(default_config, file)

    yield

    # Teardown
    shutil.rmtree("test_mimeo_cli-dir")


def test_basic_use():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/config-1.json"]

    assert not path.exists("test_mimeo_cli-dir/output")

    MimeoCLI.main()

    assert path.exists("test_mimeo_cli-dir/output")
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert path.exists(file_path)

        with open(file_path, "r") as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == '<SomeEntity>\n'
            assert file_content.readline() == '    <ChildNode1>1</ChildNode1>\n'
            assert file_content.readline() == '    <ChildNode2>value-2</ChildNode2>\n'
            assert file_content.readline() == '    <ChildNode3>true</ChildNode3>\n'
            assert file_content.readline() == '</SomeEntity>\n'
