
from mimeo.config.exc import InvalidMimeoConfigError, InvalidVarsError
from mimeo.config.mimeo_config import MimeoConfig
from tests.utils import assert_throws


def test_str():
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

    mimeo_config = MimeoConfig(config)
    assert str(mimeo_config) == str(config)


def test_parse_source_with_single_template():
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

    assert MimeoConfig.parse_source(config_xml) == expected_source


def test_parse_source_with_multiple_templates():
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
        "vars": {
            "CUSTOM_KEY1": "custom value",
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

    assert MimeoConfig.parse_source(config_xml) == expected_source


def test_parse_source_with_empty_templates():
    config_xml = """
    <mimeo_configuration>
        <output>
            <direction>stdout</direction>
        </output>
        <vars>
            <CUSTOM_KEY1>custom value</CUSTOM_KEY1>
        </vars>
        <_templates_ />
    </mimeo_configuration>
    """
    expected_source = {
        "output": {
            "direction": "stdout",
        },
        "vars": {
            "CUSTOM_KEY1": "custom value",
        },
        "_templates_": [],
    }

    assert MimeoConfig.parse_source(config_xml) == expected_source


def test_parse_source_with_no_template_child_in_templates():
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

    assert MimeoConfig.parse_source(config_xml) == expected_source


def test_parsing_config():
    config = {
        "output": {
            "direction": "stdout",
        },
        "vars": {
            "CUSTOM_KEY1": "custom value",
            "CUSTOM_KEY2": {
                "_mimeo_util": {
                    "_name": "auto_increment",
                    "pattern": "{}",
                },
            },
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

    mimeo_config = MimeoConfig(config)
    assert mimeo_config.output.direction == "stdout"
    assert mimeo_config.vars == {
        "CUSTOM_KEY1": "custom value",
        "CUSTOM_KEY2": {
            "_mimeo_util": {
                "_name": "auto_increment",
                "pattern": "{}",
            },
        },
    }


def test_parsing_config_default():
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

    mimeo_config = MimeoConfig(config)
    assert mimeo_config.output.direction == "file"
    assert mimeo_config.output.directory_path == "mimeo-output"
    assert mimeo_config.output.file_name == "mimeo-output-{}.xml"


@assert_throws(err_type=InvalidMimeoConfigError,
               msg="No templates in the Mimeo Config: {config}",
               config="{'output': {'direction': 'stdout'}}")
def test_parsing_config_without_templates():
    config = {
        "output": {
            "direction": "stdout",
        },
    }
    MimeoConfig(config)


@assert_throws(err_type=InvalidMimeoConfigError,
               msg="_templates_ property does not store an array: {config}",
               config="{'_templates_': {'count': 5, 'model': {'SomeEntity': "
                      "{'ChildNode': 'value'}}}}")
def test_parsing_config_with_templates_object():
    config = {
        "_templates_": {
            "count": 5,
            "model": {
                "SomeEntity": {
                    "ChildNode": "value",
                },
            },
        },
    }
    MimeoConfig(config)


@assert_throws(err_type=InvalidVarsError,
               msg="Provided var [{var}] is invalid (you can use upper-cased name "
                   "with underscore and digits, starting with a letter)!",
               var="CuSTOM_KEY2")
def test_parsing_config_with_invalid_vars_forbidden_character():
    config = {
        "vars": {
            "CUSTOM_KEY1": "value1",
            "CuSTOM_KEY2": "value2",
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
    MimeoConfig(config)


@assert_throws(err_type=InvalidVarsError,
               msg="Provided var [{var}] is invalid (you can use upper-cased name "
                   "with underscore and digits, starting with a letter)!",
               var="2CUSTOM_KEY")
def test_parsing_config_with_invalid_vars_starting_with_digit():
    config = {
        "vars": {
            "CUSTOM_KEY1": "value1",
            "2CUSTOM_KEY": "value2",
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
    MimeoConfig(config)


@assert_throws(err_type=InvalidVarsError,
               msg="Provided var [{var}] is invalid (you can use ony atomic values "
                   "and Mimeo Utils)!",
               var="CUSTOM_KEY1")
def test_parsing_config_with_invalid_vars_using_non_atomic_value_and_non_mimeo_util():
    config = {
        "vars": {
            "CUSTOM_KEY1": {},
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
    MimeoConfig(config)


@assert_throws(err_type=InvalidVarsError,
               msg="vars property does not store an object: {vars}",
               vars="[{'CUSTOM_KEY1': 'value1', 'CuSTOM_KEY1': 'value2'}]")
def test_parsing_config_invalid_vars_not_being_object():
    config = {
        "vars": [
            {
                "CUSTOM_KEY1": "value1",
                "CuSTOM_KEY1": "value2",
            },
        ],
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
    MimeoConfig(config)
