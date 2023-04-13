import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.utils import UtilsRenderer


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


def test_auto_increment_raw(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        identifier = UtilsRenderer.render_raw("auto_increment")
        assert identifier == "00001"
        identifier = UtilsRenderer.render_raw("auto_increment")
        assert identifier == "00002"


def test_auto_increment_parametrized_default(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        identifier = UtilsRenderer.render_parametrized({"_name": "auto_increment"})
        assert identifier == "00001"
        identifier = UtilsRenderer.render_parametrized({"_name": "auto_increment"})
        assert identifier == "00002"


def test_auto_increment_parametrized_with_pattern(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        identifier = UtilsRenderer.render_parametrized({"_name": "auto_increment", "pattern": "{}"})
        assert identifier == "1"
        identifier = UtilsRenderer.render_parametrized({"_name": "auto_increment", "pattern": "MYID/{}"})
        assert identifier == "MYID/2"
        identifier = UtilsRenderer.render_parametrized({"_name": "auto_increment", "pattern": "MYID_{:010d}"})
        assert identifier == "MYID_0000000003"


def test_auto_increment_parametrized_with_non_str_pattern(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(AttributeError) as err:
            UtilsRenderer.render_parametrized({"_name": "auto_increment", "pattern": 1})

        assert err.value.args[0] == "'int' object has no attribute 'format'"


def test_auto_increment_for_different_context(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeEntity")
        context2 = mimeo_manager.get_context("SomeOtherEntity")

        mimeo_manager.set_current_context(context1)
        identifier = UtilsRenderer.render_raw("auto_increment")
        assert identifier == "00001"
        identifier = UtilsRenderer.render_raw("auto_increment")
        assert identifier == "00002"

        mimeo_manager.set_current_context(context2)
        identifier = UtilsRenderer.render_raw("auto_increment")
        assert identifier == "00001"

        mimeo_manager.set_current_context(context1)
        identifier = UtilsRenderer.render_raw("auto_increment")
        assert identifier == "00003"
