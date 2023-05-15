from pathlib import Path

from mimeo.database import CurrenciesDB
from mimeo.database.exc import InvalidIndexError
from tests.utils import assert_throws


def test_get_currencies():
    db = CurrenciesDB()

    currencies = db.get_currencies()
    assert len(currencies) == CurrenciesDB.NUM_OF_RECORDS

    currencies.pop(0)
    assert len(currencies) == CurrenciesDB.NUM_OF_RECORDS - 1

    currencies = db.get_currencies()
    assert len(currencies) == CurrenciesDB.NUM_OF_RECORDS


def test_get_currency_at():
    with Path("src/mimeo/resources/currencies.csv").open() as currencies:
        next(currencies)
        currency_1_cols = next(currencies).rstrip().split(",")
        currency_2_cols = next(currencies).rstrip().split(",")

    db = CurrenciesDB()

    currency_1 = db.get_currency_at(0)
    assert currency_1.code == currency_1_cols[0]
    assert currency_1.name == currency_1_cols[1]
    assert currency_1_cols[2] in currency_1.countries

    currency_2 = db.get_currency_at(1)
    assert currency_2.code == currency_2_cols[0]
    assert currency_2.name == currency_2_cols[1]
    assert currency_2_cols[2] in currency_2.countries


@assert_throws(err_type=InvalidIndexError,
               msg="Provided index [{i}] is out or the range: 0-168!",
               params={"i": 300})
def test_get_currency_at_out_of_range():
    db = CurrenciesDB()
    db.get_currency_at(300)


def test_get_currency_of():
    db = CurrenciesDB()
    india_currency = db.get_currency_of("India")

    assert india_currency.code == "INR"
    assert "India" in india_currency.countries


def test_get_currency_of_non_existing_country():
    db = CurrenciesDB()
    nec_currency = db.get_currency_of("NEC")

    assert nec_currency is None
