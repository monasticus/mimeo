from datetime import date, timedelta

import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.context.exc import VarNotFoundError
from mimeo.utils import MimeoRenderer
from mimeo.utils.exc import InvalidValueError, NotASpecialFieldError
from tests.utils import assert_throws


@pytest.fixture(autouse=True)
def default_config():
    return MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": 2,
            "CUSTOM_VAR_2": "{CUSTOM_VAR_1}",
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
    })


def test_is_special_field_true():
    assert MimeoRenderer.is_special_field("{:SomeChild:}")
    assert MimeoRenderer.is_special_field("{:Some_Child:}")
    assert MimeoRenderer.is_special_field("{:Some-Child:}")
    assert MimeoRenderer.is_special_field("{:SomeChild1:}")
    assert MimeoRenderer.is_special_field("{:ns:SomeChild1:}")


def test_is_special_field_false():
    assert not MimeoRenderer.is_special_field(":SomeField:}")
    assert not MimeoRenderer.is_special_field("{:SomeField:")
    assert not MimeoRenderer.is_special_field("{SomeField:}")
    assert not MimeoRenderer.is_special_field("{:SomeField}")
    assert not MimeoRenderer.is_special_field("SomeField:}")
    assert not MimeoRenderer.is_special_field("{:SomeField")
    assert not MimeoRenderer.is_special_field("{SomeField}")
    assert not MimeoRenderer.is_special_field(":SomeField:")
    assert not MimeoRenderer.is_special_field("SomeField")
    assert not MimeoRenderer.is_special_field("{::}")
    assert not MimeoRenderer.is_special_field("{:Some Field:}")
    assert not MimeoRenderer.is_special_field("{:_:SomeField:}")


def test_get_special_field_name():
    assert MimeoRenderer.get_special_field_name("{:SomeField:}") == "SomeField"


def test_get_special_field_name_using_namespace():
    assert MimeoRenderer.get_special_field_name("{:ns:SomeField:}") == "ns:SomeField"


@assert_throws(err_type=NotASpecialFieldError,
               msg="Provided field [{:SomeField}] is not a special one (use {:NAME:})!")
def test_get_special_field_name_when_invalid():
    MimeoRenderer.get_special_field_name("{:SomeField}")


def test_is_raw_mimeo_util_true():
    assert MimeoRenderer.is_raw_mimeo_util("{random_str}")
    assert MimeoRenderer.is_raw_mimeo_util("{random_int}")
    assert MimeoRenderer.is_raw_mimeo_util("{random_item}")
    assert MimeoRenderer.is_raw_mimeo_util("{date}")
    assert MimeoRenderer.is_raw_mimeo_util("{date_time}")
    assert MimeoRenderer.is_raw_mimeo_util("{auto_increment}")
    assert MimeoRenderer.is_raw_mimeo_util("{curr_iter}")
    assert MimeoRenderer.is_raw_mimeo_util("{key}")
    assert MimeoRenderer.is_raw_mimeo_util("{city}")
    assert MimeoRenderer.is_raw_mimeo_util("{country}")


def test_is_raw_mimeo_util_false():
    assert not MimeoRenderer.is_raw_mimeo_util("random_str")
    assert not MimeoRenderer.is_raw_mimeo_util("{random}")


def test_is_parametrized_mimeo_util_true():
    assert MimeoRenderer.is_parametrized_mimeo_util({
        "_mimeo_util": {},
    })


def test_is_parametrized_mimeo_util_false():
    assert not MimeoRenderer.is_parametrized_mimeo_util({
        "_mimeo_util": {},
        "key": "value",
    })
    assert not MimeoRenderer.is_parametrized_mimeo_util({
        "_util": {},
    })
    assert not MimeoRenderer.is_parametrized_mimeo_util([
        {
            "_mimeo_util": {},
        },
    ])


def test_render_value_str_value(default_config):
    with MimeoContextManager(default_config):
        value = MimeoRenderer.render("str-value")
        assert value == "str-value"


def test_render_value_int_value(default_config):
    with MimeoContextManager(default_config):
        value = MimeoRenderer.render(1)
        assert value == 1


def test_render_value_bool_value(default_config):
    with MimeoContextManager(default_config):
        value = MimeoRenderer.render(True)
        assert value is True


def test_raw_mimeo_util():
    date_value = MimeoRenderer.render("{date}")
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_parametrized_mimeo_util_default():
    mimeo_util = {
        "_mimeo_util": {
            "_name": "date",
        },
    }
    date_value = MimeoRenderer.render(mimeo_util)
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_parametrized_mimeo_util_custom():
    mimeo_util = {
        "_mimeo_util": {
            "_name": "date",
            "days_delta": 5,
        },
    }
    date_value = MimeoRenderer.render(mimeo_util)
    expected_date_value = date.today() + timedelta(5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_parametrized_util_using_raw_mimeo_util(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeEntity")
        context2 = mimeo_manager.get_context("SomeOtherEntity")

        mimeo_manager.set_current_context(context1)
        context1.next_iteration()
        context1.next_iteration()
        key = MimeoRenderer.render("{key}")
        context1.next_iteration()

        mimeo_manager.set_current_context(context2)
        context2.next_iteration()
        context2.next_iteration()
        mimeo_util = {
            "_mimeo_util": {
                "_name": "key",
                "context": "SomeEntity",
                "iteration": "{curr_iter}",
            },
        }
        key_outside_context = MimeoRenderer.render(mimeo_util)
        assert key == key_outside_context


def test_parametrized_util_using_parametrized_mimeo_util(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeEntity")
        context2 = mimeo_manager.get_context("SomeOtherEntity")

        mimeo_manager.set_current_context(context1)
        context1.next_iteration()
        context1.next_iteration()
        key = MimeoRenderer.render("{key}")
        context1.next_iteration()

        mimeo_manager.set_current_context(context2)
        context2.next_iteration()
        context2.next_iteration()
        mimeo_util = {
            "_mimeo_util": {
                "_name": "key",
                "context": "SomeEntity",
                "iteration": {
                    "_mimeo_util": {
                        "_name": "curr_iter",
                    },
                },
            },
        }
        key_outside_context = MimeoRenderer.render(mimeo_util)
        assert key == key_outside_context


def test_util_parametrized_using_variable(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeEntity")
        context2 = mimeo_manager.get_context("SomeOtherEntity")

        mimeo_manager.set_current_context(context1)
        context1.next_iteration()
        context1.next_iteration()
        key = MimeoRenderer.render("{key}")
        context1.next_iteration()

        mimeo_manager.set_current_context(context2)
        context2.next_iteration()
        mimeo_util = {
            "_mimeo_util": {
                "_name": "key",
                "context": "SomeEntity",
                "iteration": "{CUSTOM_VAR_2}",
            },
        }
        key_outside_context = MimeoRenderer.render(mimeo_util)
        assert key == key_outside_context


def test_vars_str():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "custom-value-1",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("{CUSTOM_VAR_1}")
        assert value == "custom-value-1"


def test_vars_int():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": 1,
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("{CUSTOM_VAR_1}")
        assert value == 1


def test_vars_bool():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": True,
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("{CUSTOM_VAR_1}")
        assert value is True


def test_vars_pointing_to_var():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "custom-value-1",
            "CUSTOM_VAR_2": "{CUSTOM_VAR_1}",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("{CUSTOM_VAR_2}")
        assert value == "custom-value-1"


@assert_throws(err_type=VarNotFoundError,
               msg="Provided variable [{var}] is not defined!",
               params={"var": "NON_EXISTING_VAR"})
def test_vars_pointing_to_non_existing_var():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "{NON_EXISTING_VAR}",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        MimeoRenderer.render("{CUSTOM_VAR_1}")


def test_vars_pointing_to_funct():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": {
                "_mimeo_util": {
                    "_name": "auto_increment",
                    "pattern": "{}",
                },
            },
        },
        "_templates_": [],
    })
    with MimeoContextManager(config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        value = MimeoRenderer.render("{CUSTOM_VAR_1}")
        assert value == "1"


@assert_throws(err_type=InvalidValueError,
               msg="The auto_increment Mimeo Util require a string value "
                   "for the pattern parameter and was: [{pattern}].",
               params={"pattern": 1})
def test_vars_pointing_to_invalid_funct():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": {
                "_mimeo_util": {
                    "_name": "auto_increment",
                    "pattern": 1,
                },
            },
        },
        "_templates_": [],
    })
    with MimeoContextManager(config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        MimeoRenderer.render("{CUSTOM_VAR_1}")


def test_vars_as_partial_values_single_beginning():
    config = MimeoConfig({
        "vars": {
            "URI_PREFIX": "/data",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("{URI_PREFIX}/1.xml")
        assert value == "/data/1.xml"


def test_vars_as_partial_values_single_middle():
    config = MimeoConfig({
        "vars": {
            "FILE_NAME": "/1",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("/data{FILE_NAME}.xml")
        assert value == "/data/1.xml"


def test_vars_as_partial_values_single_end():
    config = MimeoConfig({
        "vars": {
            "URI_SUFFIX": ".xml",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("/data/1{URI_SUFFIX}")
        assert value == "/data/1.xml"


def test_vars_as_partial_values_repeated():
    config = MimeoConfig({
        "vars": {
            "FILE_NAME": "/1",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("/data{FILE_NAME}{FILE_NAME}.xml")
        assert value == "/data/1/1.xml"


def test_vars_as_partial_values_multiple():
    config = MimeoConfig({
        "vars": {
            "URI_PREFIX": "/data",
            "URI_SUFFIX": ".xml",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("{URI_PREFIX}/1{URI_SUFFIX}")
        assert value == "/data/1.xml"


def test_vars_as_partial_values_str():
    config = MimeoConfig({
        "vars": {
            "URI_PREFIX": "/data",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("{URI_PREFIX}/1.xml")
        assert value == "/data/1.xml"


def test_vars_as_partial_values_int():
    config = MimeoConfig({
        "vars": {
            "NUM": 1,
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("/data/{NUM}.xml")
        assert value == "/data/1.xml"


def test_vars_as_partial_values_bool():
    config = MimeoConfig({
        "vars": {
            "VALIDATED": True,
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = MimeoRenderer.render("/data/{VALIDATED}/1.xml")
        assert value == "/data/true/1.xml"


def test_special_fields_render_str(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", "custom-value")

        rendered_field = MimeoRenderer.render("{:ChildNode1:}")
        assert rendered_field == "custom-value"


def test_special_fields_render_int(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", 1)

        rendered_field = MimeoRenderer.render("{:ChildNode1:}")
        assert rendered_field == 1


def test_special_fields_render_bool(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", True)

        rendered_field = MimeoRenderer.render("{:ChildNode1:}")
        assert rendered_field is True


def test_special_fields_as_partial_values_single_beginning(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", "custom-value")

        rendered_field = MimeoRenderer.render("{:ChildNode1:}-1")
        assert rendered_field == "custom-value-1"


def test_special_fields_as_partial_values_single_middle(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", "custom-value")

        rendered_field = MimeoRenderer.render("_{:ChildNode1:}_")
        assert rendered_field == "_custom-value_"


def test_special_fields_as_partial_values_single_end(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", "custom-value")

        rendered_field = MimeoRenderer.render("my-{:ChildNode1:}")
        assert rendered_field == "my-custom-value"


def test_special_fields_as_partial_values_single_repeated(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", "custom-value")

        rendered_field = MimeoRenderer.render("{:ChildNode1:}-and-{:ChildNode1:}")
        assert rendered_field == "custom-value-and-custom-value"


def test_special_fields_as_partial_values_multiple(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", "prefix-to")
        context.curr_iteration().add_special_field("ChildNode2", "my-custom-value")

        rendered_field = MimeoRenderer.render("{:ChildNode1:}-{:ChildNode2:}")
        assert rendered_field == "prefix-to-my-custom-value"


def test_special_fields_as_partial_values_str(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", "custom-value")

        rendered_field = MimeoRenderer.render("{:ChildNode1:}-1")
        assert rendered_field == "custom-value-1"


def test_special_fields_as_partial_values_int(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", 1)

        rendered_field = MimeoRenderer.render("custom-value-{:ChildNode1:}")
        assert rendered_field == "custom-value-1"


def test_special_fields_as_partial_values_bool(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", True)

        rendered_field = MimeoRenderer.render("custom-{:ChildNode1:}-value")
        assert rendered_field == "custom-true-value"
