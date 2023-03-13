import pytest

from mimeo.model.exceptions import IncorrectMimeoConfig, UnsupportedOutputFormat
from mimeo.model.mimeo_config import MimeoConfig


def test_parsing_config():
    config = {
        "output_format": "xml",
        "output_details": {
            "direction": "stdout"
        },
        "xml_declaration": True,
        "indent": 4,
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

    mimeo_template = MimeoConfig(config)
    assert mimeo_template.output_format == "xml"
    assert mimeo_template.output_details.direction == "stdout"
    assert mimeo_template.xml_declaration is True
    assert mimeo_template.indent == 4


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

    mimeo_template = MimeoConfig(config)
    assert mimeo_template.output_format == "xml"
    assert mimeo_template.output_details.direction == "file"
    assert mimeo_template.output_details.directory_path == "mimeo-output"
    assert mimeo_template.output_details.file_name_tmplt == "mimeo-output-{}.xml"
    assert mimeo_template.xml_declaration is False
    assert mimeo_template.indent is None


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
