import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.database import MimeoDB
from mimeo.database.exc import DataNotFound
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


def test_city_raw(default_config):
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in iter(mimeo_db.get_cities())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        city = UtilsRenderer.render_raw("city")
        assert city in cities


def test_city_parametrized_default(default_config):
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in iter(mimeo_db.get_cities())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "city"}
        city = UtilsRenderer.render_parametrized(mimeo_util)
        assert city in cities


def test_city_parametrized_with_unique(default_config):
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in iter(mimeo_db.get_cities())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "city", "unique": False}
        city = UtilsRenderer.render_parametrized(mimeo_util)
        assert city in cities


@assert_throws(err_type=DataNotFound,
               message="Mimeo database does not contain any cities of provided country [{country}].",
               params={"country": "NEC"})
def test_city_parametrized_with_unique_and_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "city", "unique": False, "country": "NEC"}
        UtilsRenderer.render_parametrized(mimeo_util)


def test_city_parametrized_with_unique_and_country(default_config):
    mimeo_db = MimeoDB()
    gbr_cities = [city.name_ascii for city in iter(mimeo_db.get_cities_of('GBR'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "city", "unique": False, "country": "GBR"}
        city = UtilsRenderer.render_parametrized(mimeo_util)
        assert city in gbr_cities


@assert_throws(err_type=DataNotFound,
               message="Mimeo database does not contain any cities of provided country [{country}].",
               params={"country": "NEC"})
def test_city_parametrized_with_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "city", "country": "NEC"}
        UtilsRenderer.render_parametrized(mimeo_util)


def test_city_parametrized_with_country(default_config):
    mimeo_db = MimeoDB()
    gbr_cities = [city.name_ascii for city in iter(mimeo_db.get_cities_of('GBR'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "city", "country": "GBR"}
        city = UtilsRenderer.render_parametrized(mimeo_util)
        assert city in gbr_cities
