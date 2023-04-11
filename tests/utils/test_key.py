from datetime import date, timedelta

import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.utils import MimeoUtilRenderer


@pytest.fixture(autouse=True)
def default_config():
    return MimeoConfig({
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True
                    }
                }
            }
        ]
    })


def test_key_raw(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        context.next_iteration()
        key1_1 = MimeoUtilRenderer.render_raw("key")
        key1_2 = MimeoUtilRenderer.render_raw("key")

        context.next_iteration()
        key2_1 = MimeoUtilRenderer.render_raw("key")
        key2_2 = MimeoUtilRenderer.render_raw("key")

        context.next_iteration()
        key3_1 = MimeoUtilRenderer.render_raw("key")
        key3_2 = MimeoUtilRenderer.render_raw("key")

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

        context.next_iteration()
        key1_1 = MimeoUtilRenderer.render_parametrized({"_name": "key"})
        key1_2 = MimeoUtilRenderer.render_parametrized({"_name": "key"})

        context.next_iteration()
        key2_1 = MimeoUtilRenderer.render_parametrized({"_name": "key"})
        key2_2 = MimeoUtilRenderer.render_parametrized({"_name": "key"})

        context.next_iteration()
        key3_1 = MimeoUtilRenderer.render_parametrized({"_name": "key"})
        key3_2 = MimeoUtilRenderer.render_parametrized({"_name": "key"})

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
        key_some_entity = MimeoUtilRenderer.render_raw("key")

        mimeo_manager.set_current_context(context2)
        context2.next_iteration()
        key_some_other_entity = MimeoUtilRenderer.render_raw("key")
        key_some_entity_outside_context = MimeoUtilRenderer.render_parametrized({
            "_name": "key",
            "context": "SomeEntity"
        })

        assert key_some_entity == key_some_entity_outside_context
        assert key_some_entity != key_some_other_entity


def test_key_parametrized_with_context_and_iteration(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeEntity")
        context2 = mimeo_manager.get_context("SomeOtherEntity")

        mimeo_manager.set_current_context(context1)
        context1.next_iteration()
        context1.next_iteration()
        key = MimeoUtilRenderer.render_raw("key")
        context1.next_iteration()

        mimeo_manager.set_current_context(context2)
        key_outside_context = MimeoUtilRenderer.render_parametrized({
            "_name": "key",
            "context": "SomeEntity",
            "iteration": 2
        })
        assert key == key_outside_context
