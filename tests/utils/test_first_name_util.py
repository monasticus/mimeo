import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.database import MimeoDB
from mimeo.database.exc import InvalidSex
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


def test_first_name_raw(default_config):
    mimeo_db = MimeoDB()
    first_names = [first_name.name for first_name in iter(mimeo_db.get_first_names())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_raw("first_name")
        assert first_name in first_names


def test_first_name_parametrized_default(default_config):
    mimeo_db = MimeoDB()
    first_names = [first_name.name for first_name in iter(mimeo_db.get_first_names())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_parametrized({"_name": "first_name"})
        assert first_name in first_names


def test_first_name_parametrized_with_unique(default_config):
    mimeo_db = MimeoDB()
    first_names = [first_name.name for first_name in iter(mimeo_db.get_first_names())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_parametrized({"_name": "first_name", "unique": False})
        assert first_name in first_names


def test_first_name_parametrized_with_unique_and_invalid_sex(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(InvalidSex) as err:
            UtilsRenderer.render_parametrized({"_name": "first_name", "unique": False, "sex": "N"})

        assert err.value.args[0] == "Invalid sex (use M, F, Male or Female)!"


def test_first_name_parametrized_with_unique_and_sex_m(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [first_name.name for first_name in iter(mimeo_db.get_first_names_by_sex('M'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_parametrized({"_name": "first_name", "unique": False, "sex": "M"})
        assert first_name in gbr_first_names


def test_first_name_parametrized_with_unique_and_sex_f(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [first_name.name for first_name in iter(mimeo_db.get_first_names_by_sex('F'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_parametrized({"_name": "first_name", "unique": False, "sex": "F"})
        assert first_name in gbr_first_names


def test_first_name_parametrized_with_unique_and_sex_male(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [first_name.name for first_name in iter(mimeo_db.get_first_names_by_sex('M'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_parametrized({"_name": "first_name", "unique": False, "sex": "Male"})
        assert first_name in gbr_first_names


def test_first_name_parametrized_with_unique_and_sex_female(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [first_name.name for first_name in iter(mimeo_db.get_first_names_by_sex('F'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_parametrized({"_name": "first_name", "unique": False, "sex": "Female"})
        assert first_name in gbr_first_names


def test_first_name_parametrized_with_invalid_sex(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(InvalidSex) as err:
            UtilsRenderer.render_parametrized({"_name": "first_name", "sex": "N"})

        assert err.value.args[0] == "Invalid sex (use M, F, Male or Female)!"


def test_first_name_parametrized_with_sex(default_config):
    mimeo_db = MimeoDB()
    gbr_first_names = [first_name.name for first_name in iter(mimeo_db.get_first_names_by_sex('M'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        first_name = UtilsRenderer.render_parametrized({"_name": "first_name", "sex": "M"})
        assert first_name in gbr_first_names
