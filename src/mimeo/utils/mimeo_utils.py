from __future__ import annotations

import random
import string
from abc import ABCMeta, abstractmethod
from datetime import date, datetime, timedelta
from typing import Any

from mimeo.context import MimeoContext, MimeoContextManager
from mimeo.context.decorators import mimeo_context
from mimeo.database import Country, MimeoDB
from mimeo.database.exc import DataNotFound, InvalidSex
from mimeo.utils.exc import InvalidValue


class MimeoUtil(metaclass=ABCMeta):
    """A superclass for all Mimeo Utils.

    It defines abstract methods to be implemented in each subclass.

    Methods
    -------
    render
        Render a value.
    """

    @classmethod
    def __subclasshook__(cls, subclass: MimeoUtil):
        """Verify if a subclass implements all abstract methods.

        Parameters
        ----------
        subclass : MimeoUtil
            A MimeoUtil subclass

        Returns
        -------
        bool
            True if the subclass includes the render method and KEY
            attribute
        """
        return ('KEY' in subclass.__dict__ and
                not callable(subclass.KEY) and
                'render' in subclass.__dict__ and
                callable(subclass.render))

    @abstractmethod
    def render(self) -> Any:
        """Render a value.

        It is an abstract method to implement in subclasses
        """
        raise NotImplementedError


class RandomStringUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a random string value.

    Methods
    -------
    render
        Render a random string value.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY = "random_str"

    def __init__(self, length: int = 20, **kwargs):
        """Initialize RandomStringUtil class with parameters.

        Parameters
        ----------
        length : int, default 20
            A length of a string to render
        kwargs : dict
            Arbitrary keyword arguments (ignored).
        """
        self._length = length

    def render(self) -> str:
        """Render a random string value.

        Returns
        -------
        str
            A random string value
        """
        return "".join(random.choice(string.ascii_letters) for _ in range(self._length))


class RandomIntegerUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a random integer value.

    Methods
    -------
    render
        Render a random integer value.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY = "random_int"

    def __init__(self, start: int = 1, limit: int = 100, **kwargs):
        """Initialize RandomIntegerUtil class with parameters.

        Parameters
        ----------
        start : int, default 1
            A lower bound for integers (inclusive)
        limit : int, default 100
            An upper bound for integers (inclusive)
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._start = start
        self._limit = limit

    def render(self) -> int:
        """Render a random integer value.

        Returns
        -------
        int
            A random integer value
        """
        return random.randrange(self._start, self._limit + 1)


class RandomItemUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a random item.

    Methods
    -------
    render
        Render a random item.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY = "random_item"

    def __init__(self, items: list = None, **kwargs):
        """Initialize RandomItemUtil class with parameters.

        Parameters
        ----------
        items : int, default ['']
            A list of items from which a value will be picked up
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._items = items if items is not None and len(items) != 0 else [""]

    def render(self) -> Any:
        """Render a random item.

        Returns
        -------
        Any
            A random item
        """
        length = len(self._items)
        return self._items[random.randrange(0, length)]


class DateUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a stringified date value.

    Methods
    -------
    render
        Render a stringified date value.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY = "date"

    def __init__(self, days_delta: int = 0, **kwargs):
        """Initialize DateUtil class with parameters.

        Parameters
        ----------
        days_delta : int, default 0
            An integer value of days to add or subtract from today
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._days_delta = days_delta

    def render(self) -> str:
        """Render a stringified date value.

        Returns
        -------
        str
            A stringified date value in format %Y-%m-%d
        """
        date_value = date.today() if self._days_delta == 0 else date.today() + timedelta(days=self._days_delta)
        return date_value.strftime("%Y-%m-%d")


class DateTimeUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a stringified date time value.

    Methods
    -------
    render
        Render a stringified date time value.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY = "date_time"

    def __init__(self,
                 days_delta: int = 0,
                 hours_delta: int = 0,
                 minutes_delta: int = 0,
                 seconds_delta: int = 0,
                 **kwargs):
        """Initialize DateTimeUtil class with parameters.

        Parameters
        ----------
        days_delta : int, default 0
            An integer value of days to add or subtract from now
        hours_delta : int, default 0
            An integer value of hours to add or subtract from now
        minutes_delta : int, default 0
            An integer value of minutes to add or subtract from now
        seconds_delta : int, default 0
            An integer value of seconds to add or subtract from now
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._days_delta = days_delta
        self._hours_delta = hours_delta
        self._minutes_delta = minutes_delta
        self._seconds_delta = seconds_delta

    def render(self) -> str:
        """Render a stringified date time value.

        Returns
        -------
        str
            A stringified date time value in format %Y-%m-%dT%H:%M:%S
        """
        time_value = datetime.now() + timedelta(days=self._days_delta,
                                                hours=self._hours_delta,
                                                minutes=self._minutes_delta,
                                                seconds=self._seconds_delta)
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
                raise DataNotFound(f"Mimeo database does not contain any cities of provided country [{self.__country}].")

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
                raise DataNotFound(f"Mimeo database does not contain such a country [{self.__country}].")
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
            raise InvalidSex(("M", "F", "Male", "Female"))


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
