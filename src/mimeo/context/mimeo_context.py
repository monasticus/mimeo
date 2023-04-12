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

        if len(self.__countries_indexes) == 0:
            raise OutOfStock(f"No more unique values, database contain only {MimeoDB.NUM_OF_COUNTRIES} countries.")

        return self.__countries_indexes.pop()

    def next_city_index(self, country: str = None):
        if not country:
            country = MimeoContext.__ALL
        self.__initialize_cities_indexes(country)
        self.__validate_cities(country)

        return self.__cities_indexes[country][MimeoContext.__INDEXES].pop()

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

    def __validate_cities(self, country: str) -> None:
        if len(self.__cities_indexes[country][MimeoContext.__INDEXES]) == 0:
            init_count = self.__cities_indexes[country][MimeoContext.__INITIAL_COUNT]
            if country == MimeoContext.__ALL:
                raise OutOfStock(f"No more unique values, database contain only {init_count} cities.")
            else:
                raise OutOfStock(f"No more unique values, database contain only {init_count} cities of {country}.")
