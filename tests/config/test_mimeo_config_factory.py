import json
import shutil
from pathlib import Path

from mimeo import MimeoConfig
from mimeo.config import MimeoConfigFactory
from mimeo.config.exc import (MimeoConfigurationNotFoundError,
                              UnsupportedMimeoConfigSourceError)
from tests.utils import assert_throws


@assert_throws(err_type=MimeoConfigurationNotFoundError,
               msg="<mimeo_configuration/> not found! {root_name} is not "
                   "a proper Mimeo Configuration root node.",
               root_name="configuration")
def test_parse_source_with_wrong_root_node():
    output_xml = """
    <configuration>
        <output>
            <direction>stdout</direction>
            <format>xml</format>
            <xml_declaration>true</xml_declaration>
            <indent>4</indent>
            <directory_path>out</directory_path>
            <file_name>out-file</file_name>
            <method>PUT</method>
            <protocol>https</protocol>
            <host>localhost</host>
            <port>8080</port>
            <endpoint>/document</endpoint>
            <username>admin</username>
            <password>admin</password>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>value</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </configuration>
    """
    MimeoConfigFactory.parse_source(output_xml)


def test_parse_source_output():
    output_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
            <format>xml</format>
            <xml_declaration>true</xml_declaration>
            <indent>4</indent>
            <directory_path>out</directory_path>
            <file_name>out-file</file_name>
            <method>PUT</method>
            <protocol>https</protocol>
            <host>localhost</host>
            <port>8080</port>
            <endpoint>/document</endpoint>
            <username>admin</username>
            <password>admin</password>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>value</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
            "format": "xml",
            "xml_declaration": True,
            "indent": 4,
            "directory_path": "out",
            "file_name": "out-file",
            "method": "PUT",
            "protocol": "https",
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
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(output_xml) == expected_source


def test_parse_source_config_vars():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <vars>
            <CUSTOM_KEY1>custom value</CUSTOM_KEY1>
        </vars>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>value</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "vars": {
            "CUSTOM_KEY1": "custom value",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_templates_with_single_template():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>value</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_templates_with_multiple_templates():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>30</count>
                <model>
                    <SomeEntity1>
                        <ChildNode>value-1</ChildNode>
                    </SomeEntity1>
                </model>
            </_template_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity2>
                        <ChildNode>value-2</ChildNode>
                    </SomeEntity2>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 30,
                "model": {
                    "SomeEntity1": {
                        "ChildNode": "value-1",
                    },
                },
            },
            {
                "count": 5,
                "model": {
                    "SomeEntity2": {
                        "ChildNode": "value-2",
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_templates_with_empty_templates():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_ />
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_templates_with_atomic_template():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>str</_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": ["str"],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_templates_with_direct_templates_list():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <count>30</count>
            <model>
                <SomeEntity1>
                    <ChildNode>value-1</ChildNode>
                </SomeEntity1>
            </model>
        </_templates_>
        <_templates_>
            <count>5</count>
            <model>
                <SomeEntity2>
                    <ChildNode>value-2</ChildNode>
                </SomeEntity2>
            </model>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 30,
                "model": {
                    "SomeEntity1": {
                        "ChildNode": "value-1",
                    },
                },
            },
            {
                "count": 5,
                "model": {
                    "SomeEntity2": {
                        "ChildNode": "value-2",
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_templates_with_no_template_child_in_templates():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <vars>
            <CUSTOM_KEY1>custom value</CUSTOM_KEY1>
        </vars>
        <_templates_>
            <count>5</count>
            <model>
                <SomeEntity>
                    <ChildNode />
                </SomeEntity>
            </model>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "vars": {
            "CUSTOM_KEY1": "custom value",
        },
        "_templates_": {
            "count": 5,
            "model": {
                "SomeEntity": {
                    "ChildNode": None,
                },
            },
        },
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_model():
    model_xml = """
    <mimeo_configuration>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <context>My Context</context>
                    <SomeEntity>
                        <ChildNode>false</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "My Context",
                    "SomeEntity": {
                        "ChildNode": False,
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(model_xml) == expected_source


def test_parse_source_config_str_value():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>value</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_config_int_value():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>1</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": 1,
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_config_negative_int_value():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>-1</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": -1,
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_config_float_value():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>1.5</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": 1.5,
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_config_negative_float_value():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>-1.5</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": -1.5,
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_config_bool_values():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode1>true</ChildNode1>
                        <ChildNode2>false</ChildNode2>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": True,
                        "ChildNode2": False,
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_config_list_value():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <ChildNode>1</ChildNode>
                        <ChildNode>2</ChildNode>
                        <ChildNode>3</ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": [1, 2, 3],
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_config_special_fields():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <SomeEntity>
                        <:ChildNode1:>value</:ChildNode1:>
                        <ChildNode2>{:ChildNode1:}</ChildNode2>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "{:ChildNode1:}": "value",
                        "ChildNode2": "{:ChildNode1:}",
                    },
                },
            },
        ],
    }

    assert MimeoConfigFactory.parse_source(config_xml) == expected_source


def test_parse_source_random_item_mimeo_util_with_single_item():
    model_xml = """
    <mimeo_configuration>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <context>My Context</context>
                    <SomeEntity>
                        <ChildNode>
                            <_mimeo_util>
                                <_name>random_item</_name>
                                <items>
                                    <item>value</item>
                                </items>
                            </_mimeo_util>
                        </ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "My Context",
                    "SomeEntity": {
                        "ChildNode": {
                            "_mimeo_util": {
                                "_name": "random_item",
                                "items": ["value"],
                            },
                        },
                    },
                },
            },
        ],
    }
    assert MimeoConfigFactory.parse_source(model_xml) == expected_source


def test_parse_source_random_item_mimeo_util_with_multiple_items():
    model_xml = """
    <mimeo_configuration>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <context>My Context</context>
                    <SomeEntity>
                        <ChildNode>
                            <_mimeo_util>
                                <_name>random_item</_name>
                                <items>
                                    <item>value</item>
                                    <item>1</item>
                                    <item>true</item>
                                </items>
                            </_mimeo_util>
                        </ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "My Context",
                    "SomeEntity": {
                        "ChildNode": {
                            "_mimeo_util": {
                                "_name": "random_item",
                                "items": ["value", 1, True],
                            },
                        },
                    },
                },
            },
        ],
    }
    assert MimeoConfigFactory.parse_source(model_xml) == expected_source


def test_parse_source_random_item_mimeo_util_with_empty_items():
    model_xml = """
    <mimeo_configuration>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <context>My Context</context>
                    <SomeEntity>
                        <ChildNode>
                            <_mimeo_util>
                                <_name>random_item</_name>
                                <items />
                            </_mimeo_util>
                        </ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "My Context",
                    "SomeEntity": {
                        "ChildNode": {
                            "_mimeo_util": {
                                "_name": "random_item",
                                "items": [],
                            },
                        },
                    },
                },
            },
        ],
    }
    assert MimeoConfigFactory.parse_source(model_xml) == expected_source


def test_parse_source_random_item_mimeo_util_with_complex_item():
    model_xml = """
    <mimeo_configuration>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <context>My Context</context>
                    <SomeEntity>
                        <ChildNode>
                            <_mimeo_util>
                                <_name>random_item</_name>
                                <items>
                                    <item>
                                        <SomeItem>1</SomeItem>
                                    </item>
                                </items>
                            </_mimeo_util>
                        </ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "My Context",
                    "SomeEntity": {
                        "ChildNode": {
                            "_mimeo_util": {
                                "_name": "random_item",
                                "items": [
                                    {
                                        "SomeItem": 1,
                                    },
                                ],
                            },
                        },
                    },
                },
            },
        ],
    }
    assert MimeoConfigFactory.parse_source(model_xml) == expected_source


def test_parse_source_random_item_mimeo_util_with_direct_items_list():
    model_xml = """
    <mimeo_configuration>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <context>My Context</context>
                    <SomeEntity>
                        <ChildNode>
                            <_mimeo_util>
                                <_name>random_item</_name>
                                <items>value</items>
                                <items>1</items>
                                <items>true</items>
                            </_mimeo_util>
                        </ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "My Context",
                    "SomeEntity": {
                        "ChildNode": {
                            "_mimeo_util": {
                                "_name": "random_item",
                                "items": ["value", 1, True],
                            },
                        },
                    },
                },
            },
        ],
    }
    assert MimeoConfigFactory.parse_source(model_xml) == expected_source


def test_parse_source_empty_mimeo_util_does_not_throw_any_error():
    model_xml = """
    <mimeo_configuration>
        <_templates_>
            <_template_>
                <count>5</count>
                <model>
                    <context>My Context</context>
                    <SomeEntity>
                        <ChildNode>
                            <_mimeo_util />
                        </ChildNode>
                    </SomeEntity>
                </model>
            </_template_>
        </_templates_>
    </mimeo_configuration>
    """
    expected_source = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "My Context",
                    "SomeEntity": {
                        "ChildNode": {
                            "_mimeo_util": None,
                        },
                    },
                },
            },
        ],
    }
    assert MimeoConfigFactory.parse_source(model_xml) == expected_source


def test_parse_source_from_json_file():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
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
    dir_path = "test_mimeo_config_factory-dir"
    file_path = f"{dir_path}/config.json"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    with Path(file_path).open("w") as file:
        json.dump(config, file)

    source = MimeoConfigFactory.parse_source(file_path)
    assert isinstance(source, dict)
    assert source == config

    shutil.rmtree(dir_path)


def test_parse_source_from_xml_file():
    config_xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
                  "<mimeo_configuration>\n"
                  "    <output>\n"
                  "        <direction>file</direction>\n"
                  "        <format>xml</format>\n"
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
                  "</mimeo_configuration>")
    expected_config = {
        "output": {
            "direction": "file",
            "format": "xml",
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

    dir_path = "test_mimeo_config_factory-dir"
    file_path = f"{dir_path}/config.xml"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    with Path(file_path).open("w") as file:
        file.write(config_xml)

    source = MimeoConfigFactory.parse_source(file_path)
    assert isinstance(source, dict)
    assert source == expected_config

    shutil.rmtree(dir_path)


@assert_throws(err_type=UnsupportedMimeoConfigSourceError,
               msg="Mimeo Configuration source [{source}] is unsupported. "
                   "Use a file path, stringified configuration or a dictionary.",
               source="[]")
def test_parse_neither_dict_nor_str():
    MimeoConfigFactory.parse([])


def test_from_json_file():
    config = {
        "output": {
            "direction": "file",
            "format": "xml",
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
    dir_path = "test_mimeo_config_factory-dir"
    file_path = f"{dir_path}/config.json"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    with Path(file_path).open("w") as file:
        json.dump(config, file)

    mimeo_config = MimeoConfigFactory.parse(file_path)
    assert isinstance(mimeo_config, MimeoConfig)
    assert str(mimeo_config) == str(config)

    shutil.rmtree(dir_path)


def test_from_xml_file():
    config = ('<?xml version="1.0" encoding="utf-8"?>\n'
              "<mimeo_configuration>\n"
              "    <output>\n"
              "        <direction>file</direction>\n"
              "        <format>xml</format>\n"
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
              "</mimeo_configuration>")
    expected_config = {
        "output": {
            "direction": "file",
            "format": "xml",
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

    dir_path = "test_mimeo_config_factory-dir"
    file_path = f"{dir_path}/config.xml"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    with Path(file_path).open("w") as file:
        file.write(config)

    mimeo_config = MimeoConfigFactory.parse(file_path)
    assert isinstance(mimeo_config, MimeoConfig)
    assert str(mimeo_config) == str(expected_config)

    shutil.rmtree(dir_path)


def test_mimeo_config_from_dict():
    config = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    }

    mimeo_config = MimeoConfigFactory.parse(config)
    assert isinstance(mimeo_config, MimeoConfig)
    assert str(mimeo_config) == str(config)


def test_parse_mimeo_config_from_dict():
    config = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    }

    mimeo_config = MimeoConfigFactory.parse(config)
    assert isinstance(mimeo_config, MimeoConfig)
    assert str(mimeo_config) == str(config)


def test_parse_mimeo_config_from_xml_str():
    config_str = """
        <mimeo_configuration>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>value</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """
    expected_config = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    }

    mimeo_config = MimeoConfigFactory.parse(config_str)
    assert isinstance(mimeo_config, MimeoConfig)
    assert str(mimeo_config) == str(expected_config)
