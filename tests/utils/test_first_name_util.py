import pytest

from mimeo.config import MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.database import MimeoDB
from mimeo.database.exc import InvalidSexError
from mimeo.utils.renderers import UtilsRenderer
from tests.utils import assert_throws


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


def test_first_name_raw(default_config):
    mimeo_db = MimeoDB()
    first_names = [n.name for n in mimeo_db.get_first_names()]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_raw("first_name")
        assert first_name in first_names


def test_first_name_parametrized_default(default_config):
    mimeo_db = MimeoDB()
    first_names = [n.name for n in mimeo_db.get_first_names()]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name"}
        first_name = UtilsRenderer.render_parametrized(mimeo_util)
        assert first_name in first_names


def test_first_name_parametrized_with_unique(default_config):
    mimeo_db = MimeoDB()
    first_names = [n.name for n in mimeo_db.get_first_names()]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name", "unique": False}
        first_name = UtilsRenderer.render_parametrized(mimeo_util)
        assert first_name in first_names


@assert_throws(err_type=InvalidSexError,
               msg="Invalid sex (use M / F / Male / Female)!")
def test_first_name_parametrized_with_unique_and_invalid_sex(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name", "unique": False, "sex": "N"}
        UtilsRenderer.render_parametrized(mimeo_util)


def test_first_name_parametrized_with_unique_and_sex_m(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [n.name for n in mimeo_db.get_first_names_by_sex("M")]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name", "unique": False, "sex": "M"}
        first_name = UtilsRenderer.render_parametrized(mimeo_util)
        assert first_name in gbr_first_names


def test_first_name_parametrized_with_unique_and_sex_f(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [n.name for n in mimeo_db.get_first_names_by_sex("F")]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name", "unique": False, "sex": "F"}
        first_name = UtilsRenderer.render_parametrized(mimeo_util)
        assert first_name in gbr_first_names


def test_first_name_parametrized_with_unique_and_sex_male(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [n.name for n in mimeo_db.get_first_names_by_sex("M")]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name", "unique": False, "sex": "Male"}
        first_name = UtilsRenderer.render_parametrized(mimeo_util)
        assert first_name in gbr_first_names


def test_first_name_parametrized_with_unique_and_sex_female(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [n.name for n in mimeo_db.get_first_names_by_sex("F")]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name", "unique": False, "sex": "Female"}
        first_name = UtilsRenderer.render_parametrized(mimeo_util)
        assert first_name in gbr_first_names


@assert_throws(err_type=InvalidSexError,
               msg="Invalid sex (use M / F / Male / Female)!")
def test_first_name_parametrized_with_invalid_sex(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name", "sex": "N"}
        UtilsRenderer.render_parametrized(mimeo_util)


def test_first_name_parametrized_with_sex(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [n.name for n in mimeo_db.get_first_names_by_sex("M")]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "first_name", "sex": "M"}
        first_name = UtilsRenderer.render_parametrized(mimeo_util)
        assert first_name in gbr_first_names
