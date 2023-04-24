from mimeo.database import (CitiesDB, City, CountriesDB, Country, FirstName,
                            FirstNamesDB, LastNamesDB)


class MimeoDB:

    NUM_OF_CITIES = CitiesDB.NUM_OF_RECORDS
    NUM_OF_COUNTRIES = CountriesDB.NUM_OF_RECORDS
    NUM_OF_FIRST_NAMES = FirstNamesDB.NUM_OF_RECORDS
    NUM_OF_LAST_NAMES = LastNamesDB.NUM_OF_RECORDS

    def __init__(self):
        self.__cities_db = CitiesDB()
        self.__countries_db = CountriesDB()
        self.__first_names_db = FirstNamesDB()
        self.__last_names_db = LastNamesDB()

    def get_cities(self) -> list:
        return self.__cities_db.get_cities()

    def get_city_at(self, index: int) -> City:
        return self.__cities_db.get_city_at(index)

    def get_cities_of(self, country: str) -> list:
        country = next(filter(lambda c: country in [c.iso_3, c.iso_2, c.name], self.get_countries()), None)
        if country is None:
            return []
        else:
            return self.__cities_db.get_cities_of(country.iso_3)

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

    def get_first_names(self) -> list:
        return self.__first_names_db.get_first_names()

    def get_first_name_at(self, index: int) -> FirstName:
        return self.__first_names_db.get_first_name_at(index)

    def get_first_names_by_sex(self, sex: str) -> list:
        return self.__first_names_db.get_first_names_by_sex(sex)

    def get_last_names(self) -> list:
        return self.__last_names_db.get_last_names()

    def get_last_name_at(self, index: int) -> FirstName:
        return self.__last_names_db.get_last_name_at(index)
