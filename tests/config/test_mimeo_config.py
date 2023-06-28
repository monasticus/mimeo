from mimeo.config import MimeoConfigFactory
from mimeo.config.exc import InvalidMimeoConfigError, InvalidVarsError
from tests.utils import assert_throws


def test_str():
    config = {
        "output": {
            "direction": "stdout",
        },
        "vars": {
            "CUSTOM_KEY1": "custom value",
        },
        "refs": {
            "custom_ref": {
                "context": "SomeEntity",
                "field": "ChildNode",
                "type": "any",
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

    mimeo_config = MimeoConfigFactory.parse(config)
    assert str(mimeo_config) == str(config)


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
        "refs": {
            "custom_ref_1": {
                "context": "SomeEntity",
                "field": "ChildNode",
                "type": "any",
            },
            "custom_ref_2": {
                "context": "SomeEntity",
                "field": "ChildNode",
                "type": "parallel",
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

    mimeo_config = MimeoConfigFactory.parse(config)
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
    assert mimeo_config.refs == {
        "custom_ref_1": {
            "context": "SomeEntity",
            "field": "ChildNode",
            "type": "any",
        },
        "custom_ref_2": {
            "context": "SomeEntity",
            "field": "ChildNode",
            "type": "parallel",
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

    mimeo_config = MimeoConfigFactory.parse(config)
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
    MimeoConfigFactory.parse(config)


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
    MimeoConfigFactory.parse(config)


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
    MimeoConfigFactory.parse(config)


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
    MimeoConfigFactory.parse(config)


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
    MimeoConfigFactory.parse(config)


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
    MimeoConfigFactory.parse(config)
