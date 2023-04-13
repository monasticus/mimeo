import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.utils.exc import NotASpecialField
from mimeo.utils.renderer import SpecialFieldsRenderer


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


def test_render_str(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", "custom-value")

        assert SpecialFieldsRenderer.render("ChildNode1") == "custom-value"


def test_render_int(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", 1)

        assert SpecialFieldsRenderer.render("ChildNode1") == 1


def test_render_bool(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        context.curr_iteration().add_special_field("ChildNode1", True)

        assert SpecialFieldsRenderer.render("ChildNode1") is True
