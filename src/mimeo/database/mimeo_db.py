from mimeo.database import CitiesDB, City, CountriesDB, Country


class MimeoDB:

    NUM_OF_CITIES = CitiesDB.NUM_OF_RECORDS
    NUM_OF_COUNTRIES = CountriesDB.NUM_OF_RECORDS

    def __init__(self):
        self.__cities_db = CitiesDB()
        self.__countries_db = CountriesDB()

    def get_cities(self) -> list:
        return self.__cities_db.get_cities()

    def get_city_at(self, index: int) -> City:
        return self.__cities_db.get_city_at(index)

    def get_cities_of(self, country: str) -> list:
        return self.__cities_db.get_cities_of(country)

    def get_countries(self) -> list:
        return self.__countries_db.get_countries()

    def get_country_at(self, index: int) -> Country:
        return self.__countries_db.get_country_at(index)

    def get_country_by_iso_3(self, iso_3: str) -> Country:
        return self.__countries_db.get_country_by_iso_3(iso_3)

    def get_country_by_iso_2(self, iso_2: str) -> Country:
        return self.__countries_db.get_country_by_iso_2(iso_2)

    def get_country_by_name(self, name: str) -> Country:
        return self.__countries_db.get_country_by_name(name)
