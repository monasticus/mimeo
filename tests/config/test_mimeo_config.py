import pytest

from mimeo.config.mimeo_config import MimeoConfig
from mimeo.exceptions import (IncorrectMimeoConfig, InvalidIndent, InvalidVars,
                              UnsupportedOutputFormat)


def test_str():
    config = {
        "output_format": "xml",
        "output_details": {
            "direction": "stdout"
        },
        "xml_declaration": True,
        "indent": 4,
        "vars": {
            "CUSTOM_KEY1": "custom value"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    mimeo_config = MimeoConfig(config)
    assert str(mimeo_config) == str(config)


def test_parsing_config():
    config = {
        "output_format": "xml",
        "output_details": {
            "direction": "stdout"
        },
        "xml_declaration": True,
        "indent": 4,
        "vars": {
            "CUSTOM_KEY1": "custom value"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    mimeo_config = MimeoConfig(config)
    assert mimeo_config.output_format == "xml"
    assert mimeo_config.output_details.direction == "stdout"
    assert mimeo_config.xml_declaration is True
    assert mimeo_config.indent == 4
    assert mimeo_config.vars == {
        "CUSTOM_KEY1": "custom value"
    }


def test_parsing_config_default():
    config = {
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    mimeo_config = MimeoConfig(config)
    assert mimeo_config.output_format == "xml"
    assert mimeo_config.output_details.direction == "file"
    assert mimeo_config.output_details.directory_path == "mimeo-output"
    assert mimeo_config.output_details.file_name_tmplt == "mimeo-output-{}.xml"
    assert mimeo_config.xml_declaration is False
    assert mimeo_config.indent == 0


def test_parsing_config_with_invalid_indent():
    config = {
        "indent": -1,
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    with pytest.raises(InvalidIndent) as err:
        MimeoConfig(config)

    assert err.value.args[0] == "Provided indent [-1] is negative!"


def test_parsing_config_with_unsupported_format():
    config = {
        "output_format": "unsupported_format",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    with pytest.raises(UnsupportedOutputFormat) as err:
        MimeoConfig(config)

    assert err.value.args[0] == "Provided format [unsupported_format] is not supported!"


def test_parsing_config_without_templates():
    config = {
        "output_format": "xml",
        "output_details": {
            "direction": "stdout"
        },
        "xml_declaration": True,
        "indent": 4
    }

    with pytest.raises(IncorrectMimeoConfig) as err:
        MimeoConfig(config)

    assert err.value.args[0] == "No templates in the Mimeo Config: " \
                                "{'output_format': 'xml', 'output_details': {'direction': 'stdout'}, " \
                                "'xml_declaration': True, 'indent': 4}"


def test_parsing_config_with_templates_object():
    config = {
        "_templates_": {
            "count": 5,
            "model": {
                "SomeEntity": {
                    "ChildNode": "value"
                }
            }
        }
    }

    with pytest.raises(IncorrectMimeoConfig) as err:
        MimeoConfig(config)

    assert err.value.args[0] == "_templates_ property does not store an array: " \
                                "{'_templates_': {'count': 5, 'model': {'SomeEntity': {'ChildNode': 'value'}}}}"


def test_parsing_config_with_invalid_vars_forbidden_character():
    config = {
        "vars": {
            "CUSTOM_KEY1": "value1",
            "CuSTOM_KEY2": "value2"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    with pytest.raises(InvalidVars) as err:
        MimeoConfig(config)

    assert err.value.args[0] == "Provided var [CuSTOM_KEY2] is invalid " \
                                "(you can use upper-cased name with underscore and digits, starting with a letter)!"


def test_parsing_config_with_invalid_vars_starting_with_digit():
    config = {
        "vars": {
            "CUSTOM_KEY1": "value1",
            "2CUSTOM_KEY": "value2"
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    with pytest.raises(InvalidVars) as err:
        MimeoConfig(config)

    assert err.value.args[0] == "Provided var [2CUSTOM_KEY] is invalid " \
                                "(you can use upper-cased name with underscore and digits, starting with a letter)!"


def test_parsing_config_with_invalid_vars_using_non_atomic_value():
    config = {
        "vars": {
            "CUSTOM_KEY1": {}
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    with pytest.raises(InvalidVars) as err:
        MimeoConfig(config)

    assert err.value.args[0] == "Provided var [CUSTOM_KEY1] is invalid (you can use ony atomic values)!"


def test_parsing_config_invalid_vars_not_being_object():
    config = {
        "vars": [
            {
                "CUSTOM_KEY1": "value1",
                "CuSTOM_KEY1": "value2"
            }
        ],
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    }

    with pytest.raises(InvalidVars) as err:
        MimeoConfig(config)

    assert err.value.args[0] == "vars property does not store an object: " \
                                "[{'CUSTOM_KEY1': 'value1', 'CuSTOM_KEY1': 'value2'}]"
