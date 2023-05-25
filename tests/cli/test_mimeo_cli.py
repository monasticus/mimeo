import json
import logging
import shutil
import sys
from glob import glob
from os import listdir
from pathlib import Path

import pytest

import mimeo.__main__ as mimeo_cli
from mimeo.cli.exc import (EnvironmentNotFoundError,
                           EnvironmentsFileNotFoundError, PathNotFoundError)
from mimeo.config.exc import MissingRequiredPropertyError
from tests import utils
from tests.utils import assert_throws


@pytest.fixture(autouse=True)
def minimum_json_config():
    return {
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }


@pytest.fixture(autouse=True)
def minimum_xml_config():
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            "<mimeo-configuration>\n"
            "    <_templates_>\n"
            "        <_template_>\n"
            "            <count>10</count>\n"
            "            <model>\n"
            "\n"
            "                <SomeEntity>\n"
            "                    <ChildNode1>1</ChildNode1>\n"
            "                    <ChildNode2>value-2</ChildNode2>\n"
            "                    <ChildNode3>true</ChildNode3>\n"
            "                </SomeEntity>\n"
            "\n"
            "            </model>\n"
            "        </_template_>\n"
            "    </_templates_>\n"
            "</mimeo-configuration>")


@pytest.fixture(autouse=True)
def default_json_config():
    return {
        "output": {
            "direction": "file",
            "format": "xml",
            "indent": 4,
            "xml_declaration": True,
            "directory_path": "test_mimeo_cli-dir/output",
            "file_name": "output-file",
        },
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }


@pytest.fixture(autouse=True)
def default_xml_config():
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            "<mimeo-configuration>\n"
            "    <output>\n"
            "        <direction>file</direction>\n"
            "        <format>xml</format>\n"
            "        <indent>4</indent>\n"
            "        <xml_declaration>true</xml_declaration>\n"
            "        <directory_path>test_mimeo_cli-dir/output</directory_path>\n"
            "        <file_name>output-file</file_name>\n"
            "    </output>\n"
            "    <_templates_>\n"
            "        <_template_>\n"
            "            <count>10</count>\n"
            "            <model>\n"
            "\n"
            "                <SomeEntity>\n"
            "                    <ChildNode1>1</ChildNode1>\n"
            "                    <ChildNode2>value-2</ChildNode2>\n"
            "                    <ChildNode3>true</ChildNode3>\n"
            "                </SomeEntity>\n"
            "\n"
            "            </model>\n"
            "        </_template_>\n"
            "    </_templates_>\n"
            "</mimeo-configuration>")


@pytest.fixture(autouse=True)
def http_json_config():
    return {
        "output": {
            "direction": "http",
            "method": "POST",
            "protocol": "http",
            "host": "localhost",
            "port": 8080,
            "endpoint": "/document",
            "username": "admin",
            "password": "admin",
        },
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    }


@pytest.fixture(autouse=True)
def http_xml_config():
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            "<mimeo-configuration>\n"
            "    <output>\n"
            "        <direction>http</direction>\n"
            "        <method>POST</method>\n"
            "        <protocol>http</protocol>\n"
            "        <host>localhost</host>\n"
            "        <port>8080</port>\n"
            "        <endpoint>/document</endpoint>\n"
            "        <username>admin</username>\n"
            "        <password>admin</password>\n"
            "    </output>\n"
            "    <_templates_>\n"
            "        <_template_>\n"
            "            <count>1</count>\n"
            "            <model>\n"
            "\n"
            "                <SomeEntity>\n"
            "                    <ChildNode1>1</ChildNode1>\n"
            "                    <ChildNode2>value-2</ChildNode2>\n"
            "                    <ChildNode3>true</ChildNode3>\n"
            "                </SomeEntity>\n"
            "\n"
            "            </model>\n"
            "        </_template_>\n"
            "    </_templates_>\n"
            "</mimeo-configuration>")


@pytest.fixture(autouse=True)
def http_default_envs():
    return {
        "default": {
            "protocol": "https",
            "host": "11.111.11.111",
            "port": 8000,
            "username": "custom-username",
            "password": "custom-password",
        },
    }


@pytest.fixture(autouse=True)
def http_custom_envs():
    return {
        "custom": {
            "protocol": "https",
            "host": "11.111.11.111",
            "port": 8000,
            "username": "custom-username",
            "password": "custom-password",
        },
    }


@pytest.fixture(autouse=True)
def _setup_and_teardown(
        minimum_json_config,
        minimum_xml_config,
        default_json_config,
        default_xml_config,
        http_json_config,
        http_xml_config,
        http_default_envs,
        http_custom_envs,
):
    # Setup
    Path("test_mimeo_cli-dir").mkdir(parents=True, exist_ok=True)
    with Path("test_mimeo_cli-dir/minimum-config.json").open("w") as file:
        json.dump(minimum_json_config, file)
    with Path("test_mimeo_cli-dir/minimum-config.xml").open("w") as file:
        file.write(minimum_xml_config)
    with Path("test_mimeo_cli-dir/default-config.json").open("w") as file:
        json.dump(default_json_config, file)
    with Path("test_mimeo_cli-dir/default-config.xml").open("w") as file:
        file.write(default_xml_config)
    with Path("test_mimeo_cli-dir/http-config.json").open("w") as file:
        json.dump(http_json_config, file)
    with Path("test_mimeo_cli-dir/http-config.xml").open("w") as file:
        file.write(http_xml_config)
    with Path("mimeo.envs.json").open("w") as file:
        json.dump(http_default_envs, file)
    with Path("custom-mimeo-envs-file.json").open("w") as file:
        json.dump(http_custom_envs, file)

    yield

    # Teardown
    shutil.rmtree("test_mimeo_cli-dir")
    Path("mimeo.envs.json").unlink()
    Path("custom-mimeo-envs-file.json").unlink()
    for filename in glob("mimeo-output/customized-output-file*"):
        Path(filename).unlink()
    for filename in glob("mimeo-output/mimeo-output*"):
        Path(filename).unlink()
    if Path("mimeo-output").exists() and not listdir("mimeo-output"):
        Path("mimeo-output").rmdir()


def test_file_path_json():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_file_path_xml():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_directory_path(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir"]

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert not Path("mimeo-output").exists()

    aioresponses.post("http://localhost:8080/document", status=200, repeat=True)
    mimeo_cli.main()

    # http-config.json + http-config.xml
    utils.assert_requests_sent(
        aioresponses, [
            {
                "method": "POST",
                "url": "http://localhost:8080/document",
                "body": "<SomeEntity>"
                        "<ChildNode1>1</ChildNode1>"
                        "<ChildNode2>value-2</ChildNode2>"
                        "<ChildNode3>true</ChildNode3>"
                        "</SomeEntity>",
            },
            {
                "method": "POST",
                "url": "http://localhost:8080/document",
                "body": "<SomeEntity>"
                        "<ChildNode1>1</ChildNode1>"
                        "<ChildNode2>value-2</ChildNode2>"
                        "<ChildNode3>true</ChildNode3>"
                        "</SomeEntity>",
            },
        ],
    )

    # default-config.json and default-config.xml
    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"

    # minimum-config.json and minimum-config.xml
    assert Path("mimeo-output").exists()
    for i in range(1, 11):
        file_path = f"mimeo-output/mimeo-output-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == ("<SomeEntity>"
                                               "<ChildNode1>1</ChildNode1>"
                                               "<ChildNode2>value-2</ChildNode2>"
                                               "<ChildNode3>true</ChildNode3>"
                                               "</SomeEntity>")


@assert_throws(err_type=PathNotFoundError,
               msg="No such file or directory [{path}]",
               path="non-existing-path")
def test_non_existing_path():
    sys.argv = ["mimeo", "non-existing-path"]
    mimeo_cli.main()


@assert_throws(err_type=PathNotFoundError,
               msg="No such file or directory [{path}]",
               path="non-existing-path")
def test_existing_and_non_existing_path():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json", "non-existing-path"]
    mimeo_cli.main()


def test_json_custom_short_xml_declaration_false():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "-x", "false"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_short_xml_declaration_false():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "-x", "false"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_short_xml_declaration_true():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "-x", "true"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_short_xml_declaration_true():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "-x", "true"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_long_xml_declaration_false():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--xml-declaration", "false"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_long_xml_declaration_false():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "--xml-declaration", "false"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_long_xml_declaration_true():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--xml-declaration", "true"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_long_xml_declaration_true():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "--xml-declaration", "true"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_short_indent_non_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "-i", "2"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "  <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "  <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "  <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_short_indent_non_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "-i", "2"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "  <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "  <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "  <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_short_indent_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "-i", "0"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == "<?xml version='1.0' encoding='utf-8'?>\n"
            assert file_content.readline() == ("<SomeEntity>"
                                               "<ChildNode1>1</ChildNode1>"
                                               "<ChildNode2>value-2</ChildNode2>"
                                               "<ChildNode3>true</ChildNode3>"
                                               "</SomeEntity>")


def test_xml_custom_short_indent_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "-i", "0"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == "<?xml version='1.0' encoding='utf-8'?>\n"
            assert file_content.readline() == ("<SomeEntity>"
                                               "<ChildNode1>1</ChildNode1>"
                                               "<ChildNode2>value-2</ChildNode2>"
                                               "<ChildNode3>true</ChildNode3>"
                                               "</SomeEntity>")


def test_json_custom_long_indent_non_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--indent", "2"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "  <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "  <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "  <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_long_indent_non_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "--indent", "2"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "  <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "  <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "  <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_long_indent_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--indent", "0"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == "<?xml version='1.0' encoding='utf-8'?>\n"
            assert file_content.readline() == ("<SomeEntity>"
                                               "<ChildNode1>1</ChildNode1>"
                                               "<ChildNode2>value-2</ChildNode2>"
                                               "<ChildNode3>true</ChildNode3>"
                                               "</SomeEntity>")


def test_xml_custom_long_indent_zero():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "--indent", "0"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == "<?xml version='1.0' encoding='utf-8'?>\n"
            assert file_content.readline() == ("<SomeEntity>"
                                               "<ChildNode1>1</ChildNode1>"
                                               "<ChildNode2>value-2</ChildNode2>"
                                               "<ChildNode3>true</ChildNode3>"
                                               "</SomeEntity>")


def test_json_custom_short_direction():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "-o", "stdout"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert not Path("test_mimeo_cli-dir/output").exists()


def test_xml_custom_short_direction():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "-o", "stdout"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert not Path("test_mimeo_cli-dir/output").exists()


def test_json_custom_long_direction():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--output", "stdout"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert not Path("test_mimeo_cli-dir/output").exists()


def test_xml_custom_long_direction():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "--output", "stdout"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert not Path("test_mimeo_cli-dir/output").exists()


def test_json_custom_direction_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "stdout"]

    try:
        mimeo_cli.main()
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_direction_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "stdout"]

    try:
        mimeo_cli.main()
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_short_directory_path():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "-d", "test_mimeo_cli-dir/customized-output"]

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert not Path("test_mimeo_cli-dir/customized-output").exists()

    mimeo_cli.main()

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert Path("test_mimeo_cli-dir/customized-output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/customized-output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_short_directory_path():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "-d", "test_mimeo_cli-dir/customized-output"]

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert not Path("test_mimeo_cli-dir/customized-output").exists()

    mimeo_cli.main()

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert Path("test_mimeo_cli-dir/customized-output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/customized-output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_long_directory_path():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--directory", "test_mimeo_cli-dir/customized-output"]

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert not Path("test_mimeo_cli-dir/customized-output").exists()

    mimeo_cli.main()

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert Path("test_mimeo_cli-dir/customized-output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/customized-output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_long_directory_path():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "--directory", "test_mimeo_cli-dir/customized-output"]

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert not Path("test_mimeo_cli-dir/customized-output").exists()

    mimeo_cli.main()

    assert not Path("test_mimeo_cli-dir/output").exists()
    assert Path("test_mimeo_cli-dir/customized-output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/customized-output/output-file-{i}.xml"
        assert Path(file_path).exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_directory_path_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-d", "test_mimeo_cli-dir/customized-output"]

    try:
        mimeo_cli.main()
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_directory_path_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-d", "test_mimeo_cli-dir/customized-output"]

    try:
        mimeo_cli.main()
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_short_file_name():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "-f", "customized-output-file"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/customized-output-file-{i}.xml"
        assert Path(file_path).exists()
        assert not Path(f"test_mimeo_cli-dir/output/output-file-{i}.xml").exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_short_file_name():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "-f", "customized-output-file"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/customized-output-file-{i}.xml"
        assert Path(file_path).exists()
        assert not Path(f"test_mimeo_cli-dir/output/output-file-{i}.xml").exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_long_file_name():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--file", "customized-output-file"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/customized-output-file-{i}.xml"
        assert Path(file_path).exists()
        assert not Path(f"test_mimeo_cli-dir/output/output-file-{i}.xml").exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_xml_custom_long_file_name():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.xml",
                "--file", "customized-output-file"]

    assert not Path("test_mimeo_cli-dir/output").exists()

    mimeo_cli.main()

    assert Path("test_mimeo_cli-dir/output").exists()
    for i in range(1, 11):
        file_path = f"test_mimeo_cli-dir/output/customized-output-file-{i}.xml"
        assert Path(file_path).exists()
        assert not Path(f"test_mimeo_cli-dir/output/output-file-{i}.xml").exists()

        with Path(file_path).open() as file_content:
            assert file_content.readline() == '<?xml version="1.0" encoding="utf-8"?>\n'
            assert file_content.readline() == "<SomeEntity>\n"
            assert file_content.readline() == "    <ChildNode1>1</ChildNode1>\n"
            assert file_content.readline() == "    <ChildNode2>value-2</ChildNode2>\n"
            assert file_content.readline() == "    <ChildNode3>true</ChildNode3>\n"
            assert file_content.readline() == "</SomeEntity>\n"


def test_json_custom_file_name_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-f", "customized-output-file"]

    try:
        mimeo_cli.main()
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_file_name_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-f", "customized-output-file"]

    try:
        mimeo_cli.main()
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_short_http_host(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "-H", "198.168.1.1"]

    aioresponses.post("http://198.168.1.1:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://198.168.1.1:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_xml_custom_short_http_host(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "-H", "198.168.1.1"]

    aioresponses.post("http://198.168.1.1:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://198.168.1.1:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_json_custom_long_http_host(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-host", "198.168.1.1"]

    aioresponses.post("http://198.168.1.1:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://198.168.1.1:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_xml_custom_long_http_host(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-host", "198.168.1.1"]

    aioresponses.post("http://198.168.1.1:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://198.168.1.1:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_json_custom_http_host_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "http",
                "-H", "198.168.1.1"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_http_host_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "-H", "198.168.1.1"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_short_http_port(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "-p", "8081"]

    aioresponses.post("http://localhost:8081/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8081/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_xml_custom_short_http_port(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "-p", "8081"]

    aioresponses.post("http://localhost:8081/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8081/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_json_custom_long_http_port(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-port", "8081"]

    aioresponses.post("http://localhost:8081/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8081/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_xml_custom_long_http_port(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-port", "8081"]

    aioresponses.post("http://localhost:8081/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8081/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_xml_custom_http_port_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "-p", "8081"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_short_http_endpoint(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "-E", "/v2/document"]

    aioresponses.post("http://localhost:8080/v2/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/v2/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_xml_custom_short_http_endpoint(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "-E", "/v2/document"]

    aioresponses.post("http://localhost:8080/v2/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/v2/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_json_custom_long_http_endpoint(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-endpoint", "/v2/document"]

    aioresponses.post("http://localhost:8080/v2/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/v2/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_xml_custom_long_http_endpoint(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-endpoint", "/v2/document"]

    aioresponses.post("http://localhost:8080/v2/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/v2/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
    )


def test_json_custom_http_endpoint_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "http",
                "-E", "/v2/document"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_http_endpoint_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "-E", "/v2/document"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_short_http_username(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "-U", "custom-user"]

    aioresponses.post("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-user", "admin"),
    )


def test_xml_custom_short_http_username(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "-U", "custom-user"]

    aioresponses.post("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-user", "admin"),
    )


def test_json_custom_long_http_username(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-user", "custom-user"]

    aioresponses.post("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-user", "admin"),
    )


def test_xml_custom_long_http_username(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-user", "custom-user"]

    aioresponses.post("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-user", "admin"),
    )


def test_json_custom_http_username_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "http",
                "-U", "custom-user"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_http_username_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "-U", "custom-user"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_short_http_password(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "-P", "custom-password"]

    aioresponses.post("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("admin", "custom-password"),
    )


def test_xml_custom_short_http_password(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "-P", "custom-password"]

    aioresponses.post("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("admin", "custom-password"),
    )


def test_json_custom_long_http_password(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-password", "custom-password"]

    aioresponses.post("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("admin", "custom-password"),
    )


def test_xml_custom_long_http_password(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-password", "custom-password"]

    aioresponses.post("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("admin", "custom-password"),
    )


def test_json_custom_http_password_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "http",
                "-P", "custom-password"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_http_password_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "-P", "custom-password"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_long_http_method(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-method", "PUT"]

    aioresponses.put("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "PUT", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("admin", "admin"),
    )


def test_xml_custom_long_http_method(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-method", "PUT"]

    aioresponses.put("http://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "PUT", "http://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("admin", "admin"),
    )


def test_json_custom_http_method_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "http",
                "--http-method", "PUT"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_http_method_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "--http-method", "PUT"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_long_http_protocol(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-protocol", "https"]

    aioresponses.post("https://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "https://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("admin", "admin"),
    )


def test_xml_custom_long_http_protocol(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-protocol", "https"]

    aioresponses.post("https://localhost:8080/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "https://localhost:8080/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("admin", "admin"),
    )


def test_json_custom_http_protocol_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "http",
                "--http-protocol", "https"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_http_protocol_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "--http-protocol", "https"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_json_custom_short_env(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "-e", "default"]

    aioresponses.post("https://11.111.11.111:8000/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "https://11.111.11.111:8000/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-username", "custom-password"),
    )


def test_xml_custom_short_env(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "-e", "default"]

    aioresponses.post("https://11.111.11.111:8000/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "https://11.111.11.111:8000/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-username", "custom-password"),
    )


def test_json_custom_long_env(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-env", "default"]

    aioresponses.post("https://11.111.11.111:8000/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "https://11.111.11.111:8000/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-username", "custom-password"),
    )


def test_xml_custom_long_env(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-env", "default"]

    aioresponses.post("https://11.111.11.111:8000/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "https://11.111.11.111:8000/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-username", "custom-password"),
    )


def test_json_custom_env_file(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-envs-file", "custom-mimeo-envs-file.json",
                "-e", "custom"]

    aioresponses.post("https://11.111.11.111:8000/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "https://11.111.11.111:8000/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-username", "custom-password"),
    )


def test_xml_custom_env_file(aioresponses):
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-envs-file", "custom-mimeo-envs-file.json",
                "-e", "custom"]

    aioresponses.post("https://11.111.11.111:8000/document", status=200)
    mimeo_cli.main()

    utils.assert_requests_count(aioresponses, 1)
    utils.assert_request_sent(
        aioresponses, "POST", "https://11.111.11.111:8000/document",
        body="<SomeEntity>"
             "<ChildNode1>1</ChildNode1>"
             "<ChildNode2>value-2</ChildNode2>"
             "<ChildNode3>true</ChildNode3>"
             "</SomeEntity>",
        auth=("custom-username", "custom-password"),
    )


@assert_throws(err_type=EnvironmentsFileNotFoundError,
               msg="Environments file not found [{file}]",
               file="non-existing-environments-file.json")
def test_json_custom_env_file_does_throw_error_when_file_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.json",
                "--http-envs-file", "non-existing-environments-file.json",
                "-e", "custom"]
    mimeo_cli.main()


@assert_throws(err_type=EnvironmentsFileNotFoundError,
               msg="Environments file not found [{file}]",
               file="non-existing-environments-file.json")
def test_xml_custom_env_file_does_throw_error_when_file_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/http-config.xml",
                "--http-envs-file", "non-existing-environments-file.json",
                "-e", "custom"]
    mimeo_cli.main()


def test_json_custom_env_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "http",
                "-e", "default"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


def test_xml_custom_env_does_not_throw_error_when_output_is_none():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "-e", "default"]

    try:
        mimeo_cli.main()
    except MissingRequiredPropertyError:
        assert True
    except KeyError:
        raise AssertionError from KeyError


@assert_throws(err_type=EnvironmentNotFoundError,
               msg="No such env [{env}] in environments file [{file}]",
               env="non-existing", file="mimeo.envs.json")
def test_json_custom_env_does_throw_error_when_environment_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.json",
                "-o", "http",
                "-e", "non-existing"]
    mimeo_cli.main()


@assert_throws(err_type=EnvironmentNotFoundError,
               msg="No such env [{env}] in environments file [{file}]",
               env="non-existing", file="mimeo.envs.json")
def test_xml_custom_env_does_throw_error_when_environment_does_not_exist():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/minimum-config.xml",
                "-o", "http",
                "-e", "non-existing"]
    mimeo_cli.main()


def test_logging_mode_default():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json"]
    logger = logging.getLogger("mimeo")

    mimeo_cli.main()

    assert logger.getEffectiveLevel() == logging.INFO


def test_logging_mode_silent():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--silent"]
    logger = logging.getLogger("mimeo")

    mimeo_cli.main()

    assert logger.getEffectiveLevel() == logging.WARNING


def test_logging_mode_debug():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--debug"]
    logger = logging.getLogger("mimeo")

    mimeo_cli.main()

    assert logger.getEffectiveLevel() == logging.DEBUG


def test_logging_mode_fine():
    sys.argv = ["mimeo", "test_mimeo_cli-dir/default-config.json",
                "--fine"]
    logger = logging.getLogger("mimeo")

    mimeo_cli.main()

    assert logger.getEffectiveLevel() == logging.FINE
