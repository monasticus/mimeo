from __future__ import annotations
import datetime
import random
import re
import string
from datetime import date, datetime, timedelta

from mimeo.exceptions import NotAllowedInstantiation, InvalidMimeoUtil


class GeneratorUtils:

    __CREATE_KEY = object()
    __INSTANCES = {}

    @classmethod
    def get_for_context(cls, context: str) -> GeneratorUtils:
        if context not in GeneratorUtils.__INSTANCES:
            cls.__INSTANCES[context] = GeneratorUtils(cls.__CREATE_KEY)
        return cls.__INSTANCES[context]

    def __init__(self, create_key):
        GeneratorUtils.__validate_instantiation(create_key)
        self.__id = 0
        self.__curr_iter = 0

    def reset(self):
        self.__id = 0

    def auto_increment(self, pattern="{:05d}"):
        self.__id += 1
        return pattern.format(self.__id)

    def set_curr_iter(self, curr_iter: int):
        self.__curr_iter = curr_iter

    def curr_iter(self, context: str = None):
        if context is not None:
            return GeneratorUtils.get_for_context(context).curr_iter()
        return str(self.__curr_iter)

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
    def eval(context: str, funct: str):
        utils = GeneratorUtils.get_for_context(context)
        prepared_funct = funct
        prepared_funct = re.sub(r"auto_increment\((.*)\)", r"utils.auto_increment(\1)", prepared_funct)
        prepared_funct = re.sub(r"curr_iter\((.*)\)", r"utils.curr_iter(\1)", prepared_funct)
        prepared_funct = re.sub(r"random_str\((.*)\)", r"utils.random_str(\1)", prepared_funct)
        prepared_funct = re.sub(r"random_int\((.*)\)", r"utils.random_int(\1)", prepared_funct)
        prepared_funct = re.sub(r"date\((.*)\)", r"utils.date(\1)", prepared_funct)
        prepared_funct = re.sub(r"date_time\((.*)\)", r"utils.date_time(\1)", prepared_funct)
        if prepared_funct.startswith("utils"):
            return eval(prepared_funct)
        else:
            raise InvalidMimeoUtil(f"Provided function [{funct}] is invalid!")

    @staticmethod
    def __validate_instantiation(create_key: str):
        try:
            assert (create_key == GeneratorUtils.__CREATE_KEY)
        except AssertionError:
            raise NotAllowedInstantiation("GeneratorUtils cannot be instantiated directly! "
                                          "Please use GeneratorUtils.get_for_context(context)")
