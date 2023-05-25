from mimeo.config import MimeoConfigFactory


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
    <model>
        <context>My Context</context>
        <SomeEntity>
            <ChildNode>false</ChildNode>
        </SomeEntity>
    </model>
    """
    expected_source = {
        "context": "My Context",
        "SomeEntity": {
            "ChildNode": False,
        },
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


def test_mimeo_config_from_dict():
    config = {
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

    mimeo_config = MimeoConfigFactory.from_dict(config)
    assert str(mimeo_config) == str(config)