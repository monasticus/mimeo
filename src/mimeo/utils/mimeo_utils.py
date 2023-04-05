import random
import string
from abc import ABCMeta, abstractmethod
from datetime import date, datetime, timedelta


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
        self.__limit = kwargs.get("limit", 100)

    def render(self):
        return random.randrange(self.__limit)


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
