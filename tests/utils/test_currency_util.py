import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.database import MimeoDB
from mimeo.database.exc import DataNotFoundError
from mimeo.utils.exc import InvalidValueError
from mimeo.utils.renderers import UtilsRenderer
from tests.utils import assert_throws


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


def test_currency_raw(default_config):
    mimeo_db = MimeoDB()
    currencies = [currency.code for currency in iter(mimeo_db.get_currencies())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        currency = UtilsRenderer.render_raw("currency")
        assert currency in currencies


def test_currency_parametrized_default(default_config):
    mimeo_db = MimeoDB()
    currencies = [currency.code for currency in iter(mimeo_db.get_currencies())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency in currencies


def test_currency_parametrized_with_unique(default_config):
    mimeo_db = MimeoDB()
    currencies = [currency.code for currency in iter(mimeo_db.get_currencies())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "unique": True}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency in currencies


def test_currency_parametrized_with_unique_and_country(default_config):
    mimeo_db = MimeoDB()
    gbr_currency = mimeo_db.get_currency_of("GBR").code
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "unique": True, "country": "GBR"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency
        # The unique param is ignored when a country is provided
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency


def test_currency_parametrized_country_iso3(default_config):
    mimeo_db = MimeoDB()
    gbr_currency = mimeo_db.get_currency_of("GBR").code
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "country": "GBR"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency


def test_currency_parametrized_country_iso2(default_config):
    mimeo_db = MimeoDB()
    gbr_currency = mimeo_db.get_currency_of("GBR").code
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "country": "GB"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency


def test_currency_parametrized_country_name(default_config):
    mimeo_db = MimeoDB()
    gbr_currency = mimeo_db.get_currency_of("GBR").code
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "country": "United Kingdom"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency


@assert_throws(err_type=DataNotFoundError,
               msg="Mimeo database doesn't contain a currency of the provided "
                   "country [{country}].",
               params={"country": "NEC"})
def test_currency_parametrized_with_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "country": "NEC"}
        UtilsRenderer.render_parametrized(mimeo_util)


def test_currency_parametrized_with_value(default_config):
    mimeo_db = MimeoDB()
    currencies = [currency.name for currency in iter(mimeo_db.get_currencies())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "value": "name"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency in currencies


def test_currency_parametrized_with_value_and_unique(default_config):
    mimeo_db = MimeoDB()
    currencies = [currency.name for currency in iter(mimeo_db.get_currencies())]
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "value": "name", "unique": True}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency in currencies


def test_currency_parametrized_with_value_and_country_iso3(default_config):
    mimeo_db = MimeoDB()
    gbr_currency = mimeo_db.get_currency_of("GBR").name
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "value": "name", "country": "GBR"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency


def test_currency_parametrized_with_value_and_country_iso2(default_config):
    mimeo_db = MimeoDB()
    gbr_currency = mimeo_db.get_currency_of("GBR").name
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "value": "name", "country": "GB"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency


def test_currency_parametrized_with_value_and_country_name(default_config):
    mimeo_db = MimeoDB()
    gbr_currency = mimeo_db.get_currency_of("GBR").name
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "value": "name", "country": "United Kingdom"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency


@assert_throws(err_type=DataNotFoundError,
               msg="Mimeo database doesn't contain a currency of the provided "
                   "country [{country}].",
               params={"country": "NEC"})
def test_currency_parametrized_with_value_and_non_existing_country(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "value": "name", "country": "NEC"}
        UtilsRenderer.render_parametrized(mimeo_util)


def test_currency_parametrized_with_value_unique_and_country(default_config):
    mimeo_db = MimeoDB()
    gbr_currency = mimeo_db.get_currency_of("GBR").name
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency",
                      "value": "name",
                      "unique": True,
                      "country": "GBR"}
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency
        # The unique param is ignored when a country is provided
        currency = UtilsRenderer.render_parametrized(mimeo_util)
        assert currency == gbr_currency


@assert_throws(err_type=InvalidValueError,
               msg="The currency Mimeo Util does not support a value [{val}]. "
                   "Supported values are: code, name.",
               params={"val": "not_supported"})
def test_currency_parametrized_with_invalid_value(default_config):
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeEntity")
        mimeo_manager.set_current_context(context)

        mimeo_util = {"_name": "currency", "value": "not_supported"}
        UtilsRenderer.render_parametrized(mimeo_util)
