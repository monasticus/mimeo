import pytest

from mimeo.config import MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.database import MimeoDB
from mimeo.database.exc import DataNotFoundError
from mimeo.utils.exc import InvalidValueError
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

        mimeo_util = {"_name": "country"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country in country_names


def test_country_parametrized_with_unique(default_config):
    mimeo_db = MimeoDB()
    country_names = [country.name for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "unique": False}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country in country_names


def test_country_parametrized_with_country_iso3(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "country": "GBR"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country == "United Kingdom"


def test_country_parametrized_with_country_iso2(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "country": "GB"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country == "United Kingdom"


@assert_throws(err_type=DataNotFoundError,
               msg="Mimeo database doesn't contain a country [{country}].",
               country="NEC")
def test_country_parametrized_with_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "country": "NEC"}
        UtilsRenderer.render_parametrized(mimeo_util)


def test_country_parametrized_with_value_iso3(default_config):
    mimeo_db = MimeoDB()
    countries_iso3 = [country.iso_3 for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso3"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country in countries_iso3


def test_country_parametrized_with_value_iso3_and_unique(default_config):
    mimeo_db = MimeoDB()
    countries_iso3 = [country.iso_3 for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso3", "unique": False}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country in countries_iso3


def test_country_parametrized_with_value_iso3_and_country_name(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso3", "country": "United Kingdom"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country == "GBR"


def test_country_parametrized_with_value_iso3_and_country_iso2(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso3", "country": "GB"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country == "GBR"


@assert_throws(err_type=DataNotFoundError,
               msg="Mimeo database doesn't contain a country [{country}].",
               country="NEC")
def test_country_parametrized_with_value_iso3_and_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso3", "country": "NEC"}
        UtilsRenderer.render_parametrized(mimeo_util)


def test_country_parametrized_with_value_iso2(default_config):
    mimeo_db = MimeoDB()
    countries_iso2 = [country.iso_2 for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso2"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country in countries_iso2


def test_country_parametrized_with_value_iso2_and_unique(default_config):
    mimeo_db = MimeoDB()
    countries_iso2 = [country.iso_2 for country in iter(mimeo_db.get_countries())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso2", "unique": False}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country in countries_iso2


def test_country_parametrized_with_value_iso2_and_country_name(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso2", "country": "United Kingdom"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country == "GB"


def test_country_parametrized_with_value_iso2_and_country_iso3(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso2", "country": "GBR"}
        country = UtilsRenderer.render_parametrized(mimeo_util)
        assert country == "GB"


@assert_throws(err_type=DataNotFoundError,
               msg="Mimeo database doesn't contain a country [{country}].",
               country="NEC")
def test_country_parametrized_with_value_iso2_and_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "iso2", "country": "NEC"}
        UtilsRenderer.render_parametrized(mimeo_util)


@assert_throws(err_type=InvalidValueError,
               msg="The country Mimeo Util does not support a value [{val}]. "
                   "Supported values are: name, iso3, iso2.",
               val="not_supported")
def test_country_parametrized_with_invalid_value(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "country", "value": "not_supported"}
        UtilsRenderer.render_parametrized(mimeo_util)
