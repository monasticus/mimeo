import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.database import MimeoDB
from mimeo.database.exc import DataNotFound
from mimeo.utils.exc import InvalidValue
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
                        "ChildNode3": True,
                    },
                },
            },
        ],
    })


def test_country_raw(default_config):
    mimeo_db = MimeoDB()
    countries = [country.name for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_raw("country")
        assert country in countries


def test_country_parametrized_default(default_config):
    mimeo_db = MimeoDB()
    country_names = [country.name for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country"})
        assert country in country_names


def test_country_parametrized_with_unique(default_config):
    mimeo_db = MimeoDB()
    country_names = [country.name for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "unique": False})
        assert country in country_names


def test_country_parametrized_with_country_iso3(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "country": "GBR"})
        assert country == "United Kingdom"


def test_country_parametrized_with_country_iso2(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "country": "GB"})
        assert country == "United Kingdom"


def test_country_parametrized_with_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(DataNotFound) as err:
            UtilsRenderer.render_parametrized({"_name": "country", "country": "NEC"})

        assert err.value.args[0] == "Mimeo database does not contain such a country [NEC]."


def test_country_parametrized_with_value_iso3(default_config):
    mimeo_db = MimeoDB()
    countries_iso3 = [country.iso_3 for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "value": "iso3"})
        assert country in countries_iso3


def test_country_parametrized_with_value_iso3_and_unique(default_config):
    mimeo_db = MimeoDB()
    countries_iso3 = [country.iso_3 for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "value": "iso3", "unique": False})
        assert country in countries_iso3


def test_country_parametrized_with_value_iso3_and_country_name(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "value": "iso3", "country": "United Kingdom"})
        assert country == "GBR"


def test_country_parametrized_with_value_iso3_and_country_iso2(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "value": "iso3", "country": "GB"})
        assert country == "GBR"


def test_country_parametrized_with_value_iso3_and_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(DataNotFound) as err:
            UtilsRenderer.render_parametrized({"_name": "country", "value": "iso3", "country": "NEC"})

        assert err.value.args[0] == "Mimeo database does not contain such a country [NEC]."


def test_country_parametrized_with_value_iso2(default_config):
    mimeo_db = MimeoDB()
    countries_iso2 = [country.iso_2 for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "value": "iso2"})
        assert country in countries_iso2


def test_country_parametrized_with_value_iso2_and_unique(default_config):
    mimeo_db = MimeoDB()
    countries_iso2 = [country.iso_2 for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "value": "iso2", "unique": False})
        assert country in countries_iso2


def test_country_parametrized_with_value_iso2_and_country_name(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "value": "iso2", "country": "United Kingdom"})
        assert country == "GB"


def test_country_parametrized_with_value_iso2_and_country_iso3(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        country = UtilsRenderer.render_parametrized({"_name": "country", "value": "iso2", "country": "GBR"})
        assert country == "GB"


def test_country_parametrized_with_value_iso2_and_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(DataNotFound) as err:
            UtilsRenderer.render_parametrized({"_name": "country", "value": "iso2", "country": "NEC"})

        assert err.value.args[0] == "Mimeo database does not contain such a country [NEC]."


def test_country_parametrized_with_invalid_value(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        with pytest.raises(InvalidValue) as err:
            UtilsRenderer.render_parametrized({"_name": "country", "value": "not_supported"})

        assert err.value.args[0] == ("The `country` Mimeo Util does not support such value [not_supported]. "
                                     "Supported values are: name (default), iso3, iso2.")
