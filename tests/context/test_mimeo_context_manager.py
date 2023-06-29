import pytest

from mimeo.config import MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.context.exc import (InvalidReferenceValueError,
                               NonPopulatedReferenceError,
                               ReferenceNotFoundError, VarNotFoundError)
from mimeo.meta.exc import InstanceNotAliveError
from tests.utils import assert_throws


@pytest.fixture(autouse=True)
def default_config():
    return MimeoConfigFactory.parse({
        "vars": {
            "CUSTOM_VAR_1": 1,
            "CUSTOM_VAR_2": "custom-value",
            "CUSTOM_VAR_3": True,
        },
        "refs": {
            "custom_ref_any": {
                "context": "SomeContext",
                "field": "ChildNode",
                "type": "any",
            },
            "custom_ref_parallel": {
                "context": "SomeContext",
                "field": "ChildNode",
                "type": "parallel",
            },
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


def test_get_context_not_initialized(default_config):
    mimeo_manager = MimeoContextManager(default_config)
    with pytest.raises(InstanceNotAliveError) as err:
        mimeo_manager.get_context("SomeContext")

    assert err.value.args[0] == "The instance is not alive!"

    with MimeoContextManager(default_config) as mimeo_manager:
        mimeo_manager.get_context("SomeContext")

    with pytest.raises(InstanceNotAliveError) as err:
        mimeo_manager.get_context("SomeContext")

    assert err.value.args[0] == "The instance is not alive!"


def test_get_context(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        assert context.name == "SomeContext"
        assert context.curr_id() == 0

        context2 = mimeo_manager.get_context("SomeContext")
        assert context is context2

        mimeo_manager2 = MimeoContextManager()
        context3 = mimeo_manager2.get_context("SomeContext")
        assert context is context3


def test_current_context(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        assert mimeo_manager.get_current_context() is None

        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        assert mimeo_manager.get_current_context() is context


def test_get_var(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        assert mimeo_manager.get_var("CUSTOM_VAR_1") == 1
        assert mimeo_manager.get_var("CUSTOM_VAR_2") == "custom-value"
        assert mimeo_manager.get_var("CUSTOM_VAR_3") is True


@assert_throws(err_type=VarNotFoundError,
               msg="Provided variable [{var}] is not defined!",
               var="NON_EXISTING_VAR")
def test_get_non_existing_var(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        mimeo_manager.get_var("NON_EXISTING_VAR")


def test_ref_any(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("ChildNode", 1)
        mimeo_manager.cache_ref("ChildNode", 2)
        mimeo_manager.cache_ref("ChildNode", 3)
        assert mimeo_manager.get_ref("custom_ref_any") in [1, 2, 3]


def test_ref_parallel(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        mimeo_manager.cache_ref("ChildNode", 1)
        assert mimeo_manager.get_ref("custom_ref_parallel") == 1
        assert mimeo_manager.get_ref("custom_ref_parallel") == 1

        context.next_iteration()
        mimeo_manager.cache_ref("ChildNode", 2)
        assert mimeo_manager.get_ref("custom_ref_parallel") == 2
        assert mimeo_manager.get_ref("custom_ref_parallel") == 2

        context.next_iteration()
        mimeo_manager.cache_ref("ChildNode", 3)
        assert mimeo_manager.get_ref("custom_ref_parallel") == 3
        assert mimeo_manager.get_ref("custom_ref_parallel") == 3


def test_ref_str(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("ChildNode", "value")
        assert mimeo_manager.get_ref("custom_ref_any") == "value"


def test_ref_int(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("ChildNode", 1)
        assert mimeo_manager.get_ref("custom_ref_any") == 1


def test_ref_float(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("ChildNode", 1.5)
        assert mimeo_manager.get_ref("custom_ref_any") == 1.5


def test_ref_bool(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("ChildNode", False)
        assert mimeo_manager.get_ref("custom_ref_any") is False


@assert_throws(err_type=InvalidReferenceValueError,
               msg="Provided reference value [{v}] is invalid (use any atomic value)!",
               v="{}")
def test_cache_ref_dict(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("custom_ref", {})


@assert_throws(err_type=InvalidReferenceValueError,
               msg="Provided reference value [{v}] is invalid (use any atomic value)!",
               v="[]")
def test_cache_ref_list(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("custom_ref", [])


@assert_throws(err_type=ReferenceNotFoundError,
               msg="Reference [{ref}] has not been found!",
               ref="non_configured_ref")
def test_get_ref_not_found(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("non_configured_ref", "value")
        mimeo_manager.get_ref("non_configured_ref")


@assert_throws(err_type=NonPopulatedReferenceError,
               msg="Reference [{ref}] has not been populated with any value!",
               ref="custom_ref_any")
def test_get_ref_non_populated(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        mimeo_manager.get_ref("custom_ref_any")


