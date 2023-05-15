from pathlib import Path

from mimeo.database import CitiesDB
from mimeo.database.exc import InvalidIndexError
from tests.utils import assert_throws


def test_get_cities():
    cities = CitiesDB.get_cities()
    assert len(cities) == CitiesDB.NUM_OF_RECORDS

    cities.pop(0)
    assert len(cities) == CitiesDB.NUM_OF_RECORDS - 1

    cities = CitiesDB.get_cities()
    assert len(cities) == CitiesDB.NUM_OF_RECORDS


def test_get_city_at():
    with Path("src/mimeo/resources/cities.csv").open() as cities:
        next(cities)
        city_1_cols = next(cities).rstrip().split(",")
        city_2_cols = next(cities).rstrip().split(",")

    db = CitiesDB()

    city_1 = db.get_city_at(0)
    assert city_1.id == int(city_1_cols[0])
    assert city_1.name == city_1_cols[1]
    assert city_1.name_ascii == city_1_cols[2]
    assert city_1.country == city_1_cols[3]

    city_2 = db.get_city_at(1)
    assert city_2.id == int(city_2_cols[0])
    assert city_2.name == city_2_cols[1]
    assert city_2.name_ascii == city_2_cols[2]
    assert city_2.country == city_2_cols[3]


@assert_throws(err_type=InvalidIndexError,
               msg="Provided index [{i}] is out or the range: 0-42904!",
               params={"i": 999999})
def test_get_city_at_out_of_range():
    db = CitiesDB()
    db.get_city_at(999999)


def test_get_city_of():
    db = CitiesDB()
    gbr_cities = db.get_cities_of("GBR")

    for city in gbr_cities:
        assert city.country == "GBR"


def test_get_city_of_non_existing_country():
    db = CitiesDB()
    nec_cities = db.get_cities_of("NEC")

    assert len(nec_cities) == 0
