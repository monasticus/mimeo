from __future__ import annotations

import datetime
import random
import re
import string
import uuid
from datetime import date, datetime, timedelta

from mimeo.config import MimeoConfig
from mimeo.exceptions import InvalidMimeoUtil, NotAllowedInstantiation


class GeneratorUtils:

    __CREATE_KEY = object()
    __INSTANCES = {}
    __VARS = {}

    @classmethod
    def setup(cls, mimeo_config: MimeoConfig) -> None:
        cls.__VARS = mimeo_config.vars

    @classmethod
    def get_for_context(cls, context: str) -> GeneratorUtils:
        if context not in GeneratorUtils.__INSTANCES:
            cls.__INSTANCES[context] = GeneratorUtils(cls.__CREATE_KEY)
        return cls.__INSTANCES[context]

    def __init__(self, create_key):
        GeneratorUtils.__validate_instantiation(create_key)
        self.__id = 0
        self.__curr_iter = 0
        self.__keys = []

    def reset(self) -> None:
        self.__id = 0

    def setup_iteration(self, curr_iter: int) -> None:
        self.__curr_iter = curr_iter
        self.__keys.append(str(uuid.uuid4()))

    def auto_increment(self, pattern="{:05d}") -> str:
        try:
            self.__id += 1
            return pattern.format(self.__id)
        except AttributeError as err:
            self.__id -= 1
            raise err

    def curr_iter(self, context: str = None) -> int:
        if context is not None:
            return GeneratorUtils.get_for_context(context).curr_iter()
        return self.__curr_iter

    def key(self) -> str:
        return self.__keys[-1]

    @staticmethod
    def get_key(context: str, iteration: int = 0) -> str:
        return GeneratorUtils.get_for_context(context).__keys[iteration - 1]

    @staticmethod
    def random_str(length=20) -> str:
        return "".join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def random_int(limit: int = 100) -> int:
        return random.randrange(limit)

    @staticmethod
    def date(days_delta=0) -> str:
        date_value = date.today() if days_delta == 0 else date.today() + timedelta(days=days_delta)
        return date_value.strftime("%Y-%m-%d")

    @staticmethod
    def date_time(days_delta=0, hours_delta=0, minutes_delta=0, seconds_delta=0) -> str:
        time_value = datetime.now() + timedelta(days=days_delta,
                                                hours=hours_delta,
                                                minutes=minutes_delta,
                                                seconds=seconds_delta)
        return time_value.strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def render_value(context: str, value):
        value_str = str(value)
        if isinstance(value, bool):
            return value_str.lower()

        pattern = re.compile("^{(.+)}$")
        if pattern.match(value_str):
            try:
                match = next(pattern.finditer(value_str))
                mimeo_util = match.group(1)
                if GeneratorUtils.__is_var(mimeo_util):
                    rendered_value = GeneratorUtils.__render_var(context, mimeo_util)
                else:
                    rendered_value = GeneratorUtils.__eval_funct(context, mimeo_util)
                return str(rendered_value)
            except InvalidMimeoUtil:
                pass
        return value_str

    @staticmethod
    def __is_var(mimeo_util: str) -> bool:
        return bool(re.match(r"^[A-Z_0-9]+$", mimeo_util))

    @staticmethod
    def __render_var(context: str, mimeo_util: str):
        value = GeneratorUtils.__VARS.get(mimeo_util)
        if value is not None:
            return GeneratorUtils.render_value(context, value)
        else:
            raise InvalidMimeoUtil(f"Provided variable [{mimeo_util}] is not defined!")

    @staticmethod
    def __eval_funct(context: str, funct: str):
        utils = GeneratorUtils.get_for_context(context)
        prepared_funct = funct
        prepared_funct = re.sub(r"auto_increment\((.*)\)", r"utils.auto_increment(\1)", prepared_funct)
        prepared_funct = re.sub(r"curr_iter\((.*)\)", r"utils.curr_iter(\1)", prepared_funct)
        if "get_key" in prepared_funct:
            prepared_funct = re.sub(r"get_key\((.*)\)", r"utils.get_key(\1)", prepared_funct)
        elif "key" in prepared_funct:
            prepared_funct = re.sub(r"key\((.*)\)", r"utils.key(\1)", prepared_funct)
        prepared_funct = re.sub(r"random_str\((.*)\)", r"utils.random_str(\1)", prepared_funct)
        prepared_funct = re.sub(r"random_int\((.*)\)", r"utils.random_int(\1)", prepared_funct)
        prepared_funct = re.sub(r"date\((.*)\)", r"utils.date(\1)", prepared_funct)
        prepared_funct = re.sub(r"date_time\((.*)\)", r"utils.date_time(\1)", prepared_funct)
        if prepared_funct.startswith("utils"):
            try:
                return eval(prepared_funct)
            except (TypeError, AttributeError, SyntaxError) as e:
                pass
        raise InvalidMimeoUtil(f"Provided function [{funct}] is invalid!")

    @staticmethod
    def __validate_instantiation(create_key: str) -> None:
        try:
            assert (create_key == GeneratorUtils.__CREATE_KEY)
        except AssertionError:
            raise NotAllowedInstantiation("GeneratorUtils cannot be instantiated directly! "
                                          "Please use GeneratorUtils.get_for_context(context)")
