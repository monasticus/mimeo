import random

from mimeo.context import MimeoIteration
from mimeo.context.exc import (ContextIterationNotFound,
                               MinimumIdentifierReached,
                               UninitializedContextIteration)
from mimeo.database import MimeoDB
from mimeo.database.exc import CountryNotFound, OutOfStock


class MimeoContext:

    __ALL = "_ALL_"
    __INITIAL_COUNT = "init-count"
    __INDEXES = "indexes"

    def __init__(self, name: str):
        self.name = name
        self.__id = 0
        self.__iterations = []
        self.__countries_indexes = None
        self.__cities_indexes = {}
        self.__first_names_indexes = {}
        self.__last_names_indexes = None

    def next_id(self) -> int:
        self.__id += 1
        return self.__id

    def curr_id(self) -> int:
        return self.__id

    def prev_id(self) -> int:
        if self.__id > 0:
            self.__id -= 1
            return self.__id
        else:
            raise MinimumIdentifierReached("There's no previous ID!")

    def next_iteration(self) -> MimeoIteration:
        next_iteration_id = 1 if len(self.__iterations) == 0 else self.__iterations[-1].id + 1
        next_iteration = MimeoIteration(next_iteration_id)
        self.__iterations.append(next_iteration)
        return next_iteration

    def curr_iteration(self) -> MimeoIteration:
        if len(self.__iterations) > 0:
            return self.__iterations[-1]
        else:
            raise UninitializedContextIteration(f"No iteration has been initialized for the current context [{self.name}]")

    def get_iteration(self, iteration_id: int) -> MimeoIteration:
        iteration = next(filter(lambda i: i.id == iteration_id, self.__iterations), None)
        if iteration is not None:
            return iteration
        else:
            raise ContextIterationNotFound(f"No iteration with id [{iteration_id}] "
                                           f"has been initialized for the current context [{self.name}]")

    def clear_iterations(self) -> None:
        self.__iterations = []

    def next_country_index(self):
        self.__initialize_countries_indexes()
        self.__validate_countries()

        return self.__countries_indexes.pop()

    def next_city_index(self, country: str = None):
        country = country if country is not None else MimeoContext.__ALL
        self.__initialize_cities_indexes(country)
        self.__validate_cities(country)

        return self.__cities_indexes[country][MimeoContext.__INDEXES].pop()

    def next_first_name_index(self, sex: str = None):
        sex = sex if sex is not None else MimeoContext.__ALL
        self.__initialize_first_names_indexes(sex)
        self.__validate_first_names(sex)

        return self.__first_names_indexes[sex][MimeoContext.__INDEXES].pop()

    def next_last_name_index(self):
        self.__initialize_last_names_indexes()
        self.__validate_last_names()

        return self.__last_names_indexes.pop()

    def __initialize_countries_indexes(self):
        if self.__countries_indexes is None:
            countries_indexes = random.sample(range(MimeoDB.NUM_OF_COUNTRIES), MimeoDB.NUM_OF_COUNTRIES)
            self.__countries_indexes = countries_indexes

    def __initialize_cities_indexes(self, country: str):
        if country not in self.__cities_indexes:
            if country == MimeoContext.__ALL:
                num_of_entries = MimeoDB.NUM_OF_CITIES
            else:
                country_cities = MimeoDB().get_cities_of(country)
                num_of_entries = len(country_cities)
                if num_of_entries == 0:
                    raise CountryNotFound(f"Mimeo database does not contain any cities of provided country [{country}].")

            cities_indexes = random.sample(range(num_of_entries), num_of_entries)
            self.__cities_indexes[country] = {
                MimeoContext.__INITIAL_COUNT: num_of_entries,
                MimeoContext.__INDEXES: cities_indexes
            }

    def __initialize_first_names_indexes(self, sex: str):
        if sex not in self.__first_names_indexes:
            if sex == MimeoContext.__ALL:
                num_of_entries = MimeoDB.NUM_OF_FIRST_NAMES
            else:
                first_names_for_sex = MimeoDB().get_first_names_by_sex(sex)
                num_of_entries = len(first_names_for_sex)

            first_names_indexes = random.sample(range(num_of_entries), num_of_entries)
            self.__first_names_indexes[sex] = {
                MimeoContext.__INITIAL_COUNT: num_of_entries,
                MimeoContext.__INDEXES: first_names_indexes
            }

    def __initialize_last_names_indexes(self):
        if self.__last_names_indexes is None:
            last_names_indexes = random.sample(range(MimeoDB.NUM_OF_LAST_NAMES), MimeoDB.NUM_OF_LAST_NAMES)
            self.__last_names_indexes = last_names_indexes

    def __validate_countries(self) -> None:
        if len(self.__countries_indexes) == 0:
            raise OutOfStock(f"No more unique values, database contain only {MimeoDB.NUM_OF_COUNTRIES} countries.")

    def __validate_cities(self, country: str) -> None:
        if len(self.__cities_indexes[country][MimeoContext.__INDEXES]) == 0:
            init_count = self.__cities_indexes[country][MimeoContext.__INITIAL_COUNT]
            if country == MimeoContext.__ALL:
                raise OutOfStock(f"No more unique values, database contain only {init_count} cities.")
            else:
                raise OutOfStock(f"No more unique values, database contain only {init_count} cities of {country}.")

    def __validate_first_names(self, sex: str) -> None:
        if len(self.__first_names_indexes[sex][MimeoContext.__INDEXES]) == 0:
            init_count = self.__first_names_indexes[sex][MimeoContext.__INITIAL_COUNT]
            if sex == MimeoContext.__ALL:
                raise OutOfStock(f"No more unique values, database contain only {init_count} first names.")
            else:
                raise OutOfStock(f"No more unique values, database contain only {init_count} "
                                 f"{'male' if sex == 'M' else 'female'} first names.")

    def __validate_last_names(self) -> None:
        if len(self.__last_names_indexes) == 0:
            raise OutOfStock(f"No more unique values, database contain only {MimeoDB.NUM_OF_LAST_NAMES} last names.")
