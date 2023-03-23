import pandas

from mimeo.database.exc import InvalidIndex


class City:

    def __init__(self, identifier: str, name: str, name_ascii: str, country: str):
        self.id = int(identifier)
        self.name = name
        self.name_ascii = name_ascii
        self.country = country

    def __str__(self) -> str:
        return str({
            "id": self.id,
            "name": self.name,
            "name_ascii": self.name_ascii,
            "country": self.country
        })

    def __repr__(self) -> str:
        return f"City('{self.id}', '{self.name}', '{self.name_ascii}', '{self.country}')"


class CitiesDB:

    __CITIES_DB = "src/resources/cities.csv"
    __CITIES_DF = None
    __CITIES = None

    def get_city_at(self, index: int) -> City:
        cities = self.__get_cities()
        try:
            return cities[index]
        except IndexError:
            raise InvalidIndex(f"Provided index [{index}] is out or the range: 0-{len(cities)-1}!")

    def get_cities_of(self, country: str) -> list:
        cities = self.__get_cities()
        return list(filter(lambda city: city.country == country, cities))

    @classmethod
    def __get_cities(cls) -> pandas.DataFrame:
        if cls.__CITIES is None:
            cls.__CITIES = [City(row.ID, row.CITY, row.CITY_ASCII, row.COUNTRY)
                            for row in cls.__get_cities_df().itertuples()]
        return cls.__CITIES

    @classmethod
    def __get_cities_df(cls) -> pandas.DataFrame:
        if cls.__CITIES_DF is None:
            cls.__CITIES_DF = pandas.read_csv(cls.__CITIES_DB)
        return cls.__CITIES_DF
