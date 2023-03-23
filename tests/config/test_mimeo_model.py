import pytest

from mimeo.config.mimeo_config import MimeoModel
from mimeo.exceptions import IncorrectMimeoModel


def test_parsing_model_with_attributes():
    model = {
        "attributes": {
          "xmlns": "http://mimeo.arch.com/default-namespace"
        },
        "SomeEntity": {
            "ChildNode": "value"
        }
    }

    mimeo_model = MimeoModel(model)
    assert mimeo_model.attributes == {
        "xmlns": "http://mimeo.arch.com/default-namespace"
    }
    assert mimeo_model.context_name == "SomeEntity"
    assert mimeo_model.root_name == "SomeEntity"
    assert mimeo_model.root_data == {
        "ChildNode": "value"
    }


def test_parsing_model_with_context_name():
    model = {
        "context": "My Context",
        "SomeEntity": {
            "ChildNode": "value"
        }
    }

    mimeo_model = MimeoModel(model)
    assert mimeo_model.attributes == {}
    assert mimeo_model.context_name == "My Context"
    assert mimeo_model.root_name == "SomeEntity"
    assert mimeo_model.root_data == {
        "ChildNode": "value"
    }


def test_parsing_model_with_attributes_and_context_name():
    model = {
        "attributes": {
          "xmlns": "http://mimeo.arch.com/default-namespace"
        },
        "context": "My Context",
        "SomeEntity": {
            "ChildNode": "value"
        }
    }

    mimeo_model = MimeoModel(model)
    assert mimeo_model.attributes == {
        "xmlns": "http://mimeo.arch.com/default-namespace"
    }
    assert mimeo_model.context_name == "My Context"
    assert mimeo_model.root_name == "SomeEntity"
    assert mimeo_model.root_data == {
        "ChildNode": "value"
    }


def test_parsing_raw_model():
    model = {
        "SomeEntity": {
            "ChildNode": "value"
        }
    }

    mimeo_model = MimeoModel(model)
    assert mimeo_model.attributes == {}
    assert mimeo_model.context_name == "SomeEntity"
    assert mimeo_model.root_name == "SomeEntity"
    assert mimeo_model.root_data == {
        "ChildNode": "value"
    }


def test_parsing_model_without_root():
    model = {
        "attributes": {
          "xmlns": "http://mimeo.arch.com/default-namespace"
        }
    }

    with pytest.raises(IncorrectMimeoModel) as err:
        MimeoModel(model)

    assert err.value.args[0] == "No root data in Mimeo Model: " \
                                "{'attributes': {'xmlns': 'http://mimeo.arch.com/default-namespace'}}"


def test_parsing_model_with_multiple_roots():
    model = {
        "SomeEntity": {
            "ChildNode": "value"
        },
        "SomeEntity2": {
            "ChildNode": "value"
        }
    }

    with pytest.raises(IncorrectMimeoModel) as err:
        MimeoModel(model)

    assert err.value.args[0] == "Multiple root data in Mimeo Model: " \
                                "{'SomeEntity': {'ChildNode': 'value'}, 'SomeEntity2': {'ChildNode': 'value'}}"


def test_parsing_model_with_non_str_context():
    model = {
        "context": 1,
        "SomeEntity": {
            "ChildNode": "value"
        }
    }

    with pytest.raises(IncorrectMimeoModel) as err:
        MimeoModel(model)

    assert err.value.args[0] == "Invalid context name in Mimeo Model (not a string value): " \
                                "{'context': 1, 'SomeEntity': {'ChildNode': 'value'}}"
