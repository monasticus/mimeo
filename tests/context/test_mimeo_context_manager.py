import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.context.exc import VarNotFound
from mimeo.meta.exc import InstanceNotAlive


@pytest.fixture(autouse=True)
def default_config():
    return MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": 1,
            "CUSTOM_VAR_2": "custom-value",
            "CUSTOM_VAR_3": True,
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
    with pytest.raises(InstanceNotAlive) as err:
        mimeo_manager.get_context("SomeContext")

    assert err.value.args[0] == "The instance is not alive!"

    with MimeoContextManager(default_config) as mimeo_manager:
        mimeo_manager.get_context("SomeContext")

    with pytest.raises(InstanceNotAlive) as err:
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


def test_get_non_existing_var(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        with pytest.raises(VarNotFound) as err:
            mimeo_manager.get_var("NON_EXISTING_VAR")

    assert err.value.args[0] == "Provided variable [NON_EXISTING_VAR] is not defined!"


