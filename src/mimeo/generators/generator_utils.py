import datetime
import random
import string
from datetime import date, datetime, timedelta

from mimeo.exceptions import NotAllowedInstantiation


class GeneratorUtils:

    __CREATE_KEY = object()
    __INSTANCES = {}

    @classmethod
    def get_for_context(cls, context: str):
        if context not in GeneratorUtils.__INSTANCES:
            cls.__INSTANCES[context] = GeneratorUtils(cls.__CREATE_KEY)
        return cls.__INSTANCES[context]

    def __init__(self, create_key):
        GeneratorUtils.__validate_instantiation(create_key)
        self.__id = 0

    def reset(self):
        self.__id = 0

    def auto_increment(self, pattern="{:05d}"):
        self.__id += 1
        return pattern.format(self.__id)

    @staticmethod
    def random_str(length=20):
        return "".join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def random_int(length=1):
        return "".join(random.choice(string.digits) for _ in range(length))

    @staticmethod
    def date(days_delta=0):
        date_value = date.today() if days_delta == 0 else date.today() + timedelta(days=days_delta)
        return date_value.strftime("%Y-%m-%d")

    @staticmethod
    def date_time(days_delta=0, hours_delta=0, minutes_delta=0, seconds_delta=0):
        time_value = datetime.now() + timedelta(days=days_delta,
                                                hours=hours_delta,
                                                minutes=minutes_delta,
                                                seconds=seconds_delta)
        return time_value.strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def __validate_instantiation(create_key: str):
        try:
            assert (create_key == GeneratorUtils.__CREATE_KEY)
        except AssertionError:
            raise NotAllowedInstantiation("GeneratorUtils cannot be instantiated directly! "
                                          "Please use GeneratorUtils.get_for_context(context)")
