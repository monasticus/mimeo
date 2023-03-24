from mimeo.database import CitiesDB, CountriesDB, MimeoDB


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


def test_get_city_of():
    mimeo_db = MimeoDB()
    cities_db = CitiesDB()
    cities_from_cities_db = cities_db.get_cities_of('GBR')
    cities_from_mimeo_db = mimeo_db.get_cities_of('GBR')
    mimeo_db_count = len(cities_from_mimeo_db)
    assert mimeo_db_count > 0
    assert mimeo_db_count == len(cities_from_cities_db)
    for i in range(mimeo_db_count):
        assert cities_from_mimeo_db[i] is cities_from_cities_db[i]


def test_get_country_at():
    mimeo_db = MimeoDB()
    countries_db = CountriesDB()
    country_from_cities_db = countries_db.get_country_at(0)
    country_from_mimeo_db = mimeo_db.get_country_at(0)
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_cities_db

    country_from_cities_db = countries_db.get_country_at(1)
    country_from_mimeo_db = mimeo_db.get_country_at(1)
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_cities_db


def test_get_country_by_iso_3():
    mimeo_db = MimeoDB()
    countries_db = CountriesDB()
    country_from_cities_db = countries_db.get_country_by_iso_3('GBR')
    country_from_mimeo_db = mimeo_db.get_country_by_iso_3('GBR')
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_cities_db


def test_get_country_by_iso_2():
    mimeo_db = MimeoDB()
    countries_db = CountriesDB()
    country_from_cities_db = countries_db.get_country_by_iso_2('GB')
    country_from_mimeo_db = mimeo_db.get_country_by_iso_2('GB')
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_cities_db


def test_get_country_by_name():
    mimeo_db = MimeoDB()
    countries_db = CountriesDB()
    country_from_cities_db = countries_db.get_country_by_name('United Kingdom')
    country_from_mimeo_db = mimeo_db.get_country_by_name('United Kingdom')
    assert country_from_mimeo_db is not None
    assert country_from_mimeo_db is country_from_cities_db
