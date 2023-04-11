import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.database import MimeoDB
from mimeo.database.exc import CountryNotFound
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


def test_city_raw(default_config):
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in iter(mimeo_db.get_cities())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        city = MimeoUtilRenderer.render_raw("city")
        assert city in cities


def test_city_parametrized_default(default_config):
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in iter(mimeo_db.get_cities())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        city = MimeoUtilRenderer.render_parametrized({"_name": "city"})
        assert city in cities


def test_city_parametrized_with_allow_duplicates(default_config):
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in iter(mimeo_db.get_cities())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        city = MimeoUtilRenderer.render_parametrized({"_name": "city", "allow_duplicates": True})
        assert city in cities


def test_city_parametrized_with_allow_duplicates_and_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(CountryNotFound) as err:
            MimeoUtilRenderer.render_parametrized({"_name": "city", "allow_duplicates": True, "country": "NEC"})

        assert err.value.args[0] == "Mimeo database does not contain any cities of provided country [NEC]."


def test_city_parametrized_with_allow_duplicates_and_country(default_config):
    mimeo_db = MimeoDB()
    gbr_cities = [city.name_ascii for city in iter(mimeo_db.get_cities_of('GBR'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        city = MimeoUtilRenderer.render_parametrized({"_name": "city", "allow_duplicates": True, "country": "GBR"})
        assert city in gbr_cities


def test_city_parametrized_with_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(CountryNotFound) as err:
            MimeoUtilRenderer.render_parametrized({"_name": "city", "country": "NEC"})

        assert err.value.args[0] == "Mimeo database does not contain any cities of provided country [NEC]."


def test_city_parametrized_with_country(default_config):
    mimeo_db = MimeoDB()
    gbr_cities = [city.name_ascii for city in iter(mimeo_db.get_cities_of('GBR'))]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        city = MimeoUtilRenderer.render_parametrized({"_name": "city", "country": "GBR"})
        assert city in gbr_cities
