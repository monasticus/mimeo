from mimeo.config import MimeoConfigFactory
from mimeo.config.exc import (InvalidMimeoConfigError, InvalidRefsError,
                              InvalidVarsError, UnsupportedPropertyValueError)
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


@assert_throws(err_type=InvalidRefsError,
               msg="refs property does not store an object: {refs}",
               refs="[{'context': 'SomeEntity', 'field': 'Child', 'type': 'any'}, "
                    "{'context': 'SomeEntity', 'field': 'Child', 'type': 'parallel'}]")
def test_parsing_config_invalid_refs_not_being_object():
    config = {
        "refs": [
            {
                "context": "SomeEntity",
                "field": "Child",
                "type": "any",
            },
            {
                "context": "SomeEntity",
                "field": "Child",
                "type": "parallel",
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


@assert_throws(err_type=InvalidRefsError,
               msg="The following ref does not store an object: {ref}",
               ref="custom_ref_1")
def test_parsing_config_invalid_refs_ref_not_being_object():
    config = {
        "refs": {
            "custom_ref_1": "not-a-dict",
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


@assert_throws(err_type=InvalidRefsError,
               msg="Missing required details [context, field, type] in the following "
                   "refs [{refs}]",
               refs="custom_ref_1, custom_ref_2, custom_ref_3")
def test_parsing_config_invalid_refs_missing_details():
    config = {
        "refs": {
            "custom_ref_1": {
                "field": "ChildNode",
                "type": "any",
            },
            "custom_ref_2": {
                "context": "SomeEntity",
                "type": "parallel",
            },
            "custom_ref_3": {
                "context": "SomeEntity",
                "field": "ChildNode",
            },
            "custom_ref_4": {
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
    MimeoConfigFactory.parse(config)


@assert_throws(err_type=InvalidRefsError,
               msg="A reference can't be configured using name of Mimeo Utils "
                   "or existing Vars. Please rename following refs: [{refs}]",
               refs="key, random_item")
def test_parsing_config_invalid_refs_forbidden_mimeo_utils_name():
    config = {
        "refs": {
            "key": {
                "context": "SomeEntity",
                "field": "ChildNode",
                "type": "any",
            },
            "random_item": {
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
    MimeoConfigFactory.parse(config)


@assert_throws(err_type=InvalidRefsError,
               msg="A reference can't be configured using name of Mimeo Utils "
                   "or existing Vars. Please rename following refs: [{refs}]",
               refs="VAR_1, VAR_2")
def test_parsing_config_invalid_refs_forbidden_vars_name():
    config = {
        "vars": {
            "VAR_1": "value-1",
            "VAR_2": "value-2",
        },
        "refs": {
            "VAR_1": {
                "context": "SomeEntity",
                "field": "ChildNode",
                "type": "any",
            },
            "VAR_2": {
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
    MimeoConfigFactory.parse(config)


@assert_throws(err_type=UnsupportedPropertyValueError,
               msg="Provided type [{type}] is not supported! "
                   "Supported values: [{values}].",
               type="unsupported_type", values="any, parallel")
def test_parsing_config_invalid_refs_unsupported_type():
    config = {
        "refs": {
            "custom_ref_4": {
                "context": "SomeEntity",
                "field": "ChildNode",
                "type": "unsupported_type",
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
    MimeoConfigFactory.parse(config)
