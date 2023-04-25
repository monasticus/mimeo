import random
import string
from abc import ABCMeta, abstractmethod
from datetime import date, datetime, timedelta

from mimeo.context import MimeoContext, MimeoContextManager
from mimeo.context.annotations import mimeo_context
from mimeo.database import Country, MimeoDB
from mimeo.database.exc import CountryNotFound, InvalidSex
from mimeo.utils.exc import InvalidValue


class MimeoUtil(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'KEY') and
                hasattr(subclass, 'render') and
                callable(subclass.render) and
                NotImplemented)

    @abstractmethod
    def render(self):
        raise NotImplementedError


class RandomStringUtil(MimeoUtil):

    KEY = "random_str"

    def __init__(self, **kwargs):
        self.__length = kwargs.get("length", 20)

    def render(self):
        return "".join(random.choice(string.ascii_letters) for _ in range(self.__length))


class RandomIntegerUtil(MimeoUtil):

    KEY = "random_int"

    def __init__(self, **kwargs):
        self.__start = kwargs.get("start", 1)
        self.__limit = kwargs.get("limit", 100)

    def render(self):
        return random.randrange(self.__start, self.__limit + 1)


class RandomItemUtil(MimeoUtil):

    KEY = "random_item"

    def __init__(self, **kwargs):
        self.__items = kwargs.get("items", [])

    def render(self):
        length = len(self.__items)
        return "" if length == 0 else self.__items[random.randrange(0, length)]


class DateUtil(MimeoUtil):

    KEY = "date"

    def __init__(self, **kwargs):
        self.__days_delta = kwargs.get("days_delta", 0)

    def render(self):
        date_value = date.today() if self.__days_delta == 0 else date.today() + timedelta(days=self.__days_delta)
        return date_value.strftime("%Y-%m-%d")


class DateTimeUtil(MimeoUtil):

    KEY = "date_time"

    def __init__(self, **kwargs):
        self.__days_delta = kwargs.get("days_delta", 0)
        self.__hours_delta = kwargs.get("hours_delta", 0)
        self.__minutes_delta = kwargs.get("minutes_delta", 0)
        self.__seconds_delta = kwargs.get("seconds_delta", 0)

    def render(self):
        time_value = datetime.now() + timedelta(days=self.__days_delta,
                                                hours=self.__hours_delta,
                                                minutes=self.__minutes_delta,
                                                seconds=self.__seconds_delta)
        return time_value.strftime("%Y-%m-%dT%H:%M:%S")


class AutoIncrementUtil(MimeoUtil):

    KEY = "auto_increment"

    def __init__(self, **kwargs):
        self.__pattern = kwargs.get("pattern", "{:05d}")

    @mimeo_context
    def render(self, context: MimeoContext = None):
        try:
            identifier = context.next_id()
            return self.__pattern.format(identifier)
        except AttributeError:
            context.prev_id()
            raise InvalidValue(f"The {self.KEY} Mimeo Util require a string value for the pattern parameter "
                               f"and was: [{self.__pattern}].")


class CurrentIterationUtil(MimeoUtil):

    KEY = "curr_iter"

    def __init__(self, **kwargs):
        self.__context_name = kwargs.get("context")

    @mimeo_context
    def render(self, context: MimeoContext = None):
        context = context if self.__context_name is None else MimeoContextManager().get_context(self.__context_name)
        return context.curr_iteration().id


class KeyUtil(MimeoUtil):

    KEY = "key"

    def __init__(self, **kwargs):
        self.__context_name = kwargs.get("context")
        self.__iteration = kwargs.get("iteration")

    @mimeo_context
    def render(self, context: MimeoContext = None):
        context = context if self.__context_name is None else MimeoContextManager().get_context(self.__context_name)
        iteration = context.curr_iteration() if self.__iteration is None else context.get_iteration(self.__iteration)
        return iteration.key


class CityUtil(MimeoUtil):

    KEY = "city"
    __MIMEO_DB = MimeoDB()

    def __init__(self, **kwargs):
        self.__unique = kwargs.get("unique", True)
        self.__country = kwargs.get("country", None)

    @mimeo_context
    def render(self, context: MimeoContext = None):
        if self.__country is None:
            if self.__unique:
                index = context.next_city_index()
            else:
                index = random.randrange(MimeoDB.NUM_OF_CITIES)
            city = self.__MIMEO_DB.get_city_at(index)
        else:
            country_cities = self.__MIMEO_DB.get_cities_of(self.__country)
            country_cities_count = len(country_cities)
            if country_cities_count == 0:
                raise CountryNotFound(f"Mimeo database does not contain any cities of provided country [{self.__country}].")

            if self.__unique:
                index = context.next_city_index(self.__country)
            else:
                index = random.randrange(country_cities_count)
            city = country_cities[index]

        return city.name_ascii


class CountryUtil(MimeoUtil):

    KEY = "country"

    __VALUE_NAME = "name"
    __VALUE_ISO3 = "iso3"
    __VALUE_ISO2 = "iso2"
    __MIMEO_DB = MimeoDB()

    def __init__(self, **kwargs):
        self.__value = kwargs.get("value", self.__VALUE_NAME)
        self.__unique = kwargs.get("unique", True)
        self.__country = kwargs.get("country", None)

    @mimeo_context
    def render(self, context: MimeoContext = None):
        if self.__value == self.__VALUE_NAME:
            return self.__get_country(context).name
        elif self.__value == self.__VALUE_ISO3:
            return self.__get_country(context).iso_3
        elif self.__value == self.__VALUE_ISO2:
            return self.__get_country(context).iso_2
        else:
            raise InvalidValue(f"The `country` Mimeo Util does not support such value [{self.__value}]. "
                               f"Supported values are: "
                               f"{self.__VALUE_NAME} (default), {self.__VALUE_ISO3}, {self.__VALUE_ISO2}.")

    def __get_country(self, context: MimeoContext) -> Country:
        if self.__country is not None:
            countries = self.__MIMEO_DB.get_countries()
            country_found = next(filter(lambda c: self.__country in [c.name, c.iso_3, c.iso_2], countries), None)
            if country_found is not None:
                return country_found
            else:
                raise CountryNotFound(f"Mimeo database does not contain such a country [{self.__country}].")
        else:
            if self.__unique:
                index = context.next_country_index()
            else:
                index = random.randrange(MimeoDB.NUM_OF_COUNTRIES)

            country = self.__MIMEO_DB.get_country_at(index)
            return country


class FirstNameUtil(MimeoUtil):

    KEY = "first_name"
    __MIMEO_DB = MimeoDB()

    def __init__(self, **kwargs):
        self.__unique = kwargs.get("unique", True)
        self.__sex = self._standardize_sex(kwargs.get("sex"))

    @mimeo_context
    def render(self, context: MimeoContext = None):
        if self.__sex is None:
            if self.__unique:
                index = context.next_first_name_index()
            else:
                index = random.randrange(MimeoDB.NUM_OF_FIRST_NAMES)
            first_name = self.__MIMEO_DB.get_first_name_at(index)
        else:
            first_name_for_sex = self.__MIMEO_DB.get_first_names_by_sex(self.__sex)
            first_name_for_sex_count = len(first_name_for_sex)

            if self.__unique:
                index = context.next_first_name_index(self.__sex)
            else:
                index = random.randrange(first_name_for_sex_count)
            first_name = first_name_for_sex[index]

        return first_name.name

    @classmethod
    def _standardize_sex(cls, sex: str):
        if sex is None:
            return sex
        elif sex.upper() in ["M", "MALE"]:
            return "M"
        elif sex.upper() in ["F", "FEMALE"]:
            return "F"
        else:
            raise InvalidSex("Invalid sex (use M, F, Male or Female)!")


class LastNameUtil(MimeoUtil):

    KEY = "last_name"
    __MIMEO_DB = MimeoDB()

    def __init__(self, **kwargs):
        self.__unique = kwargs.get("unique", True)

    @mimeo_context
    def render(self, context: MimeoContext = None):
        if self.__unique:
            index = context.next_first_name_index()
        else:
            index = random.randrange(MimeoDB.NUM_OF_FIRST_NAMES)
        last_name = self.__MIMEO_DB.get_last_name_at(index)

        return last_name
