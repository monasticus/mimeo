
from mimeo.config.exc import InvalidMimeoConfig, InvalidVars
from mimeo.config.mimeo_config import MimeoConfig
from tests.test_tools import assert_throws


def test_str():
    config = {
        "output_details": {
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


def test_parsing_config():
    config = {
        "output_details": {
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
    assert mimeo_config.output_details.direction == "stdout"
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
    assert mimeo_config.output_details.direction == "file"
    assert mimeo_config.output_details.directory_path == "mimeo-output"
    assert mimeo_config.output_details.file_name_tmplt == "mimeo-output-{}.xml"


@assert_throws(err_type=InvalidMimeoConfig,
               message="No templates in the Mimeo Config: {config}",
               params={"config": "{'output_details': {'direction': 'stdout'}}"})
def test_parsing_config_without_templates():
    config = {
        "output_details": {
            "direction": "stdout",
        },
    }
    MimeoConfig(config)


@assert_throws(err_type=InvalidMimeoConfig,
               message="_templates_ property does not store an array: {config}",
               params={"config": "{'_templates_': {'count': 5, 'model': {'SomeEntity': {'ChildNode': 'value'}}}}"})
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


@assert_throws(err_type=InvalidVars,
               message="Provided var [{var}] is invalid (you can use upper-cased name "
                       "with underscore and digits, starting with a letter)!",
               params={"var": "CuSTOM_KEY2"})
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


@assert_throws(err_type=InvalidVars,
               message="Provided var [{var}] is invalid (you can use upper-cased name "
                       "with underscore and digits, starting with a letter)!",
               params={"var": "2CUSTOM_KEY"})
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


@assert_throws(err_type=InvalidVars,
               message="Provided var [{var}] is invalid (you can use ony atomic values "
                       "and Mimeo Utils)!",
               params={"var": "CUSTOM_KEY1"})
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


@assert_throws(err_type=InvalidVars,
               message="vars property does not store an object: {vars}",
               params={"vars": "[{'CUSTOM_KEY1': 'value1', 'CuSTOM_KEY1': 'value2'}]"})
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
