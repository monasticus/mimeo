import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.utils.exc import InvalidValue
from mimeo.utils.renderers import UtilsRenderer
from tests.test_tools import assert_throws


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
                        "ChildNode3": True,
                    },
                },
            },
        ],
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

        mimeo_util = {"_name": "auto_increment"}
        identifier = UtilsRenderer.render_parametrized(mimeo_util)
        assert identifier == "00001"
        identifier = UtilsRenderer.render_parametrized(mimeo_util)
        assert identifier == "00002"


def test_auto_increment_parametrized_with_pattern(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "auto_increment", "pattern": "{}"}
        identifier = UtilsRenderer.render_parametrized(mimeo_util)
        assert identifier == "1"
        mimeo_util = {"_name": "auto_increment", "pattern": "MYID/{}"}
        identifier = UtilsRenderer.render_parametrized(mimeo_util)
        assert identifier == "MYID/2"
        mimeo_util = {"_name": "auto_increment", "pattern": "MYID_{:010d}"}
        identifier = UtilsRenderer.render_parametrized(mimeo_util)
        assert identifier == "MYID_0000000003"


@assert_throws(err_type=InvalidValue,
               message="The auto_increment Mimeo Util require a string value for "
                       "the pattern parameter and was: [{pattern}].",
               params={"pattern": 1})
def test_auto_increment_parametrized_with_non_str_pattern(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "auto_increment", "pattern": 1}
        UtilsRenderer.render_parametrized(mimeo_util)


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
