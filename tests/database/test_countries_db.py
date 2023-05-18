from pathlib import Path

from mimeo.database import CountriesDB
from mimeo.database.exc import InvalidIndexError
from tests.utils import assert_throws


def test_get_countries():
    db = CountriesDB()

    countries = db.get_countries()
    assert len(countries) == CountriesDB.NUM_OF_RECORDS

    countries.pop(0)
    assert len(countries) == CountriesDB.NUM_OF_RECORDS - 1

    countries = db.get_countries()
    assert len(countries) == CountriesDB.NUM_OF_RECORDS


def test_get_country_at():
    with Path("src/mimeo/resources/countries.csv").open() as countries:
        next(countries)
        country_1_cols = next(countries).rstrip().split(",")
        country_2_cols = next(countries).rstrip().split(",")

    db = CountriesDB()

    country_1 = db.get_country_at(0)
    assert country_1.iso_3 == country_1_cols[0]
    assert country_1.iso_2 == country_1_cols[1]
    assert country_1.name == country_1_cols[2]

    country_2 = db.get_country_at(1)
    assert country_2.iso_3 == country_2_cols[0]
    assert country_2.iso_2 == country_2_cols[1]
    assert country_2.name == country_2_cols[2]


@assert_throws(err_type=InvalidIndexError,
               msg="Provided index [{i}] is out or the range: 0-238!",
               i=999)
def test_get_country_at_out_of_range():
    db = CountriesDB()
    db.get_country_at(999)


def test_get_country_by_iso_3():
    db = CountriesDB()
    country = db.get_country_by_iso_3("GBR")
    assert country.iso_3 == "GBR"
    assert country.iso_2 == "GB"
    assert country.name == "United Kingdom"


def test_get_country_by_iso_2():
    db = CountriesDB()
    country = db.get_country_by_iso_2("GB")
    assert country.iso_3 == "GBR"
    assert country.iso_2 == "GB"
    assert country.name == "United Kingdom"


def test_get_country_by_name():
    db = CountriesDB()
    country = db.get_country_by_name("United Kingdom")
    assert country.iso_3 == "GBR"
    assert country.iso_2 == "GB"
    assert country.name == "United Kingdom"


def test_get_non_existing_country():
    db = CountriesDB()
    country = db.get_country_by_iso_3("NEC")
    assert country is None

    country = db.get_country_by_iso_2("NN")
    assert country is None

    country = db.get_country_by_name("Non Existing Country")
    assert country is None
