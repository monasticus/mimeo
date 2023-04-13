import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.utils.renderer import UtilsRenderer


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


def test_curr_iter_raw(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        context.next_iteration()
        curr_iter = UtilsRenderer.render_raw("curr_iter")
        assert curr_iter == 1

        context.next_iteration()
        curr_iter = UtilsRenderer.render_raw("curr_iter")
        assert curr_iter == 2


def test_curr_iter_parametrized_default(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        context.next_iteration()
        curr_iter = UtilsRenderer.render_parametrized({"_name": "curr_iter"})
        assert curr_iter == 1

        context.next_iteration()
        curr_iter = UtilsRenderer.render_parametrized({"_name": "curr_iter"})
        assert curr_iter == 2


def test_curr_iter_parametrized_with_context(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeEntity")
        context2 = mimeo_manager.get_context("SomeOtherEntity")

        mimeo_manager.set_current_context(context1)
        context1.next_iteration()
        curr_iter = UtilsRenderer.render_raw("curr_iter")
        assert curr_iter == 1
        context1.next_iteration()
        curr_iter = UtilsRenderer.render_raw("curr_iter")
        assert curr_iter == 2

        context2.next_iteration()
        curr_iter = UtilsRenderer.render_parametrized({"_name": "curr_iter", "context": "SomeOtherEntity"})
        assert curr_iter == 1
