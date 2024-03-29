import pytest

from mimeo.config import MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.utils.renderers import UtilsRenderer


@pytest.fixture(autouse=True)
def default_config():
    return MimeoConfigFactory.parse({
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


def test_key_raw(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        context.next_iteration()
        key1_1 = UtilsRenderer.render_raw("key")
        key1_2 = UtilsRenderer.render_raw("key")

        context.next_iteration()
        key2_1 = UtilsRenderer.render_raw("key")
        key2_2 = UtilsRenderer.render_raw("key")

        context.next_iteration()
        key3_1 = UtilsRenderer.render_raw("key")
        key3_2 = UtilsRenderer.render_raw("key")

        assert key1_1 == key1_2
        assert key2_1 == key2_2
        assert key3_1 == key3_2
        assert key1_1 != key2_1
        assert key2_1 != key3_1
        assert key3_1 != key1_1


def test_key_parametrized_default(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        mimeo_util = {"_name": "key"}

        context.next_iteration()
        key1_1 = UtilsRenderer.render_parametrized(mimeo_util)
        key1_2 = UtilsRenderer.render_parametrized(mimeo_util)

        context.next_iteration()
        key2_1 = UtilsRenderer.render_parametrized(mimeo_util)
        key2_2 = UtilsRenderer.render_parametrized(mimeo_util)

        context.next_iteration()
        key3_1 = UtilsRenderer.render_parametrized(mimeo_util)
        key3_2 = UtilsRenderer.render_parametrized(mimeo_util)

        assert key1_1 == key1_2
        assert key2_1 == key2_2
        assert key3_1 == key3_2
        assert key1_1 != key2_1
        assert key2_1 != key3_1
        assert key3_1 != key1_1


def test_key_parametrized_with_context(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeEntity")
        context2 = mimeo_manager.get_context("SomeOtherEntity")

        mimeo_manager.set_current_context(context1)
        context1.next_iteration()
        key_some_entity = UtilsRenderer.render_raw("key")

        mimeo_manager.set_current_context(context2)
        context2.next_iteration()
        mimeo_util = {"_name": "key", "context": "SomeEntity"}
        key_some_other_entity = UtilsRenderer.render_raw("key")
        key_some_entity_outside_context = UtilsRenderer.render_parametrized(mimeo_util)

        assert key_some_entity == key_some_entity_outside_context
        assert key_some_entity != key_some_other_entity


def test_key_parametrized_with_context_and_iteration(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeEntity")
        context2 = mimeo_manager.get_context("SomeOtherEntity")

        mimeo_manager.set_current_context(context1)
        context1.next_iteration()
        context1.next_iteration()
        key = UtilsRenderer.render_raw("key")
        context1.next_iteration()

        mimeo_manager.set_current_context(context2)
        mimeo_util = {
            "_name": "key",
            "context": "SomeEntity",
            "iteration": 2,
        }
        key_outside_context = UtilsRenderer.render_parametrized(mimeo_util)
        assert key == key_outside_context
