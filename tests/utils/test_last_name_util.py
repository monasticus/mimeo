import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.database import MimeoDB
from mimeo.utils.renderers import UtilsRenderer


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


def test_last_name_raw(default_config):
    mimeo_db = MimeoDB()
    last_names = mimeo_db.get_last_names()
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        last_name = UtilsRenderer.render_raw("last_name")
        assert last_name in last_names


def test_last_name_parametrized_default(default_config):
    mimeo_db = MimeoDB()
    last_names = mimeo_db.get_last_names()
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        last_name = UtilsRenderer.render_parametrized({"_name": "last_name"})
        assert last_name in last_names


def test_last_name_parametrized_with_unique(default_config):
    mimeo_db = MimeoDB()
    last_names = mimeo_db.get_last_names()
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        last_name = UtilsRenderer.render_parametrized({"_name": "last_name", "unique": False})
        assert last_name in last_names
