from mimeo.database import (CitiesDB, CountriesDB, FirstNamesDB, LastNamesDB,
                            MimeoDB)


def test_get_cities():
    mimeo_db = MimeoDB()
    cities_from_cities_db = CitiesDB.get_cities()
    cities_from_mimeo_db = mimeo_db.get_cities()
    mimeo_db_count = len(cities_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(cities_from_cities_db)
    for i in range(mimeo_db_count):
        assert cities_from_mimeo_db[i] is cities_from_cities_db[i]


def test_get_city_at():
    mimeo_db = MimeoDB()
    cities_db = CitiesDB()
    city_from_cities_db = cities_db.get_city_at(0)
    city_from_mimeo_db = mimeo_db.get_city_at(0)
    assert city_from_mimeo_db is not None
    assert city_from_mimeo_db is city_from_cities_db

    city_from_cities_db = cities_db.get_city_at(1)
    city_from_mimeo_db = mimeo_db.get_city_at(1)
    assert city_from_mimeo_db is not None
    assert city_from_mimeo_db is city_from_cities_db


def test_get_city_of_using_country_iso3():
    mimeo_db = MimeoDB()
    cities_db = CitiesDB()
    cities_from_cities_db = cities_db.get_cities_of("GBR")
    cities_from_mimeo_db = mimeo_db.get_cities_of("GBR")
    mimeo_db_count = len(cities_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(cities_from_cities_db)
    for i in range(mimeo_db_count):
        assert cities_from_mimeo_db[i] is cities_from_cities_db[i]


def test_get_city_of_using_country_iso2():
    mimeo_db = MimeoDB()
    cities_db = CitiesDB()
    cities_from_cities_db = cities_db.get_cities_of("GBR")
    cities_from_mimeo_db = mimeo_db.get_cities_of("GB")
    mimeo_db_count = len(cities_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(cities_from_cities_db)
    for i in range(mimeo_db_count):
        assert cities_from_mimeo_db[i] is cities_from_cities_db[i]


def test_get_city_of_using_country_name():
    mimeo_db = MimeoDB()
    cities_db = CitiesDB()
    cities_from_cities_db = cities_db.get_cities_of("GBR")
    cities_from_mimeo_db = mimeo_db.get_cities_of("United Kingdom")
    mimeo_db_count = len(cities_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(cities_from_cities_db)
    for i in range(mimeo_db_count):
        assert cities_from_mimeo_db[i] is cities_from_cities_db[i]


def test_get_city_of_non_existing_country():
    mimeo_db = MimeoDB()
    cities = mimeo_db.get_cities_of("NEC")

    assert len(cities) == 0


def test_get_countries():
    mimeo_db = MimeoDB()
    countries_from_countries_db = CountriesDB.get_countries()
    countries_from_mimeo_db = mimeo_db.get_countries()
    mimeo_db_count = len(countries_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(countries_from_countries_db)
    for i in range(mimeo_db_count):
        assert countries_from_mimeo_db[i] is countries_from_countries_db[i]


def test_get_country_at():
    mimeo_db = MimeoDB()
    countries_db = CountriesDB()
    country_from_countries_db = countries_db.get_country_at(0)
    country_from_mimeo_db = mimeo_db.get_country_at(0)
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_countries_db

    country_from_countries_db = countries_db.get_country_at(1)
    country_from_mimeo_db = mimeo_db.get_country_at(1)
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_countries_db


def test_get_country_by_iso_3():
    mimeo_db = MimeoDB()
    countries_db = CountriesDB()
    country_from_cities_db = countries_db.get_country_by_iso_3("GBR")
    country_from_mimeo_db = mimeo_db.get_country_by_iso_3("GBR")
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_cities_db


def test_get_country_by_iso_2():
    mimeo_db = MimeoDB()
    countries_db = CountriesDB()
    country_from_cities_db = countries_db.get_country_by_iso_2("GB")
    country_from_mimeo_db = mimeo_db.get_country_by_iso_2("GB")
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_cities_db


def test_get_country_by_name():
    mimeo_db = MimeoDB()
    countries_db = CountriesDB()
    country_from_cities_db = countries_db.get_country_by_name("United Kingdom")
    country_from_mimeo_db = mimeo_db.get_country_by_name("United Kingdom")
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_cities_db


def test_get_first_names():
    mimeo_db = MimeoDB()
    first_names_form_first_names_db = FirstNamesDB.get_first_names()
    first_names_from_mimeo_db = mimeo_db.get_first_names()
    mimeo_db_count = len(first_names_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(first_names_form_first_names_db)
    for i in range(mimeo_db_count):
        assert first_names_from_mimeo_db[i] is first_names_form_first_names_db[i]


def test_get_first_name_at():
    mimeo_db = MimeoDB()
    first_names_db = FirstNamesDB()
    first_name_from_first_names_db = first_names_db.get_first_name_at(0)
    first_name_from_mimeo_db = mimeo_db.get_first_name_at(0)
    assert first_name_from_mimeo_db is not None
    assert first_name_from_mimeo_db is first_name_from_first_names_db

    first_name_from_first_names_db = first_names_db.get_first_name_at(1)
    first_name_from_mimeo_db = mimeo_db.get_first_name_at(1)
    assert first_name_from_mimeo_db is not None
    assert first_name_from_mimeo_db is first_name_from_first_names_db


def test_get_first_names_by_sex():
    mimeo_db = MimeoDB()
    first_names_db = FirstNamesDB()
    first_names_from_first_names_db = first_names_db.get_first_names_by_sex("M")
    first_names_from_mimeo_db = mimeo_db.get_first_names_by_sex("M")
    mimeo_db_count = len(first_names_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(first_names_from_first_names_db)
    for i in range(mimeo_db_count):
        assert first_names_from_mimeo_db[i] is first_names_from_first_names_db[i]


def test_get_last_names():
    mimeo_db = MimeoDB()
    last_names_form_last_names_db = LastNamesDB.get_last_names()
    last_names_from_mimeo_db = mimeo_db.get_last_names()
    mimeo_db_count = len(last_names_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(last_names_form_last_names_db)
    for i in range(mimeo_db_count):
        assert last_names_from_mimeo_db[i] is last_names_form_last_names_db[i]


def test_get_last_name_at():
    mimeo_db = MimeoDB()
    last_names_db = LastNamesDB()
    last_name_from_last_names_db = last_names_db.get_last_name_at(0)
    last_name_from_mimeo_db = mimeo_db.get_last_name_at(0)
    assert last_name_from_mimeo_db is not None
    assert last_name_from_mimeo_db is last_name_from_last_names_db

    last_name_from_last_names_db = last_names_db.get_last_name_at(1)
    last_name_from_mimeo_db = mimeo_db.get_last_name_at(1)
    assert last_name_from_mimeo_db is not None
    assert last_name_from_mimeo_db is last_name_from_last_names_db
