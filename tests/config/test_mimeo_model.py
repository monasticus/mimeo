
from mimeo.config.exc import InvalidMimeoModelError
from mimeo.config.mimeo_config import MimeoModel
from tests.utils import assert_throws


def test_str():
    model = {
        "context": "My Context",
        "SomeEntity": {
            "ChildNode": "value",
        },
    }

    mimeo_model = MimeoModel(model)
    assert str(mimeo_model) == str(model)


def test_parsing_model_with_context_name():
    model = {
        "context": "My Context",
        "SomeEntity": {
            "ChildNode": "value",
        },
    }

    mimeo_model = MimeoModel(model)
    assert mimeo_model.context_name == "My Context"
    assert mimeo_model.root_name == "SomeEntity"
    assert mimeo_model.root_data == {
        "ChildNode": "value",
    }


def test_parsing_raw_model():
    model = {
        "SomeEntity": {
            "ChildNode": "value",
        },
    }

    mimeo_model = MimeoModel(model)
    assert mimeo_model.context_name == "SomeEntity"
    assert mimeo_model.root_name == "SomeEntity"
    assert mimeo_model.root_data == {
        "ChildNode": "value",
    }


@assert_throws(err_type=InvalidMimeoModelError,
               msg="No root data in Mimeo Model: {model}",
               model="{'context': 'My Context'}")
def test_parsing_model_without_root():
    model = {
        "context": "My Context",
    }
    MimeoModel(model)


@assert_throws(err_type=InvalidMimeoModelError,
               msg="Multiple root data in Mimeo Model: {model}",
               model="{'SomeEntity': {'ChildNode': 'value'},"
                     " 'SomeEntity2': {'ChildNode': 'value'}}")
def test_parsing_model_with_multiple_roots():
    model = {
        "SomeEntity": {
            "ChildNode": "value",
        },
        "SomeEntity2": {
            "ChildNode": "value",
        },
    }
    MimeoModel(model)


@assert_throws(err_type=InvalidMimeoModelError,
               msg="Invalid context name in Mimeo Model (not a string value): {model}",
               model="{'context': 1, 'SomeEntity': {'ChildNode': 'value'}}")
def test_parsing_model_with_non_str_context():
    model = {
        "context": 1,
        "SomeEntity": {
            "ChildNode": "value",
        },
    }
    MimeoModel(model)
