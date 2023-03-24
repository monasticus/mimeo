from __future__ import annotations

import datetime
import random
import re
import string
import uuid
from datetime import date, datetime, timedelta

from mimeo.config import MimeoConfig
from mimeo.database import MimeoDB
from mimeo.generators.exc import (InvalidMimeoUtil, InvalidSpecialFieldValue,
                                  NotAllowedInstantiation, NotASpecialField,
                                  OutOfStock)


class GeneratorUtils:

    __CREATE_KEY = object()
    __MIMEO_DB = MimeoDB()
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
        self.__special_fields = {}
        self.__cities_indexes = []
        self.__cities = set()

    def reset(self) -> None:
        self.__id = 0

    def setup_iteration(self, curr_iter: int) -> None:
        self.__curr_iter = curr_iter
        self.__keys.append(str(uuid.uuid4()))
        self.__special_fields = {}

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

    def city(self, allow_duplicates: bool = False) -> str:
        if allow_duplicates:
            return self.__MIMEO_DB.get_city_at(self.random_int(MimeoDB.NUM_OF_CITIES)).name_ascii
        else:
            self.__initialize_cities_indexes()

            if len(self.__cities_indexes) == 0:
                raise OutOfStock(f"No more unique values, database contain only {len(self.__cities)} cities.")
            else:
                index = self.__cities_indexes.pop()
                city = self.__MIMEO_DB.get_city_at(index)
                self.__cities.add(city)
                return city.name_ascii

    def provide(self, field_name: str, field_value) -> None:
        if not GeneratorUtils.is_special_field(field_name):
            raise NotASpecialField(f"Provided field [{field_name}] is not a special one (use {'{:NAME:}'})!")
        if isinstance(field_value, dict) or isinstance(field_value, list):
            raise InvalidSpecialFieldValue(f"Provided field value [{field_value}] is invalid (use any atomic value)!")

        self.__special_fields[field_name] = field_value

    def inject(self, field_name: str):
        if field_name not in self.__special_fields:
            raise NotASpecialField(f"There's no such a special field [{field_name[2:][:-2]}]!")
        return self.__special_fields.get(field_name)

    def __initialize_cities_indexes(self):
        if len(self.__cities) == 0:
            self.__cities_indexes = random.sample(range(MimeoDB.NUM_OF_CITIES), MimeoDB.NUM_OF_CITIES)

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
    def random(items: list = None):
        items = items if items is not None else []
        length = len(items)
        return "" if length == 0 else items[random.randrange(0, len(items))]

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
    def get_special_field_name(field_name: str) -> str:
        if not GeneratorUtils.is_special_field(field_name):
            raise NotASpecialField(f"Provided field [{field_name}] is not a special one (use {'{:NAME:}'})!")

        return field_name[2:][:-2]

    @staticmethod
    def is_special_field(field_name: str) -> bool:
        return bool(re.match(r"^{:([a-zA-Z]+:)?[-_a-zA-Z0-9]+:}$", field_name))

    @staticmethod
    def render_value(context: str, value):
        value_str = str(value)
        if isinstance(value, bool):
            return value_str.lower()

        special_fields_pattern = re.compile(".*({:([a-zA-Z]+:)?[-_a-zA-Z0-9]+:})")
        vars_pattern = re.compile(".*({[A-Z_0-9]+})")
        funct_pattern = re.compile("^{(.+)}$")
        try:
            if special_fields_pattern.match(value_str):
                match = next(special_fields_pattern.finditer(value_str))
                mimeo_util = match.group(1)
                rendered_value = GeneratorUtils.get_for_context(context).inject(mimeo_util)
                final_rendered_value = value_str.replace(mimeo_util, str(rendered_value))
                return GeneratorUtils.render_value(context, final_rendered_value)
            elif vars_pattern.match(value_str):
                match = next(vars_pattern.finditer(value_str))
                mimeo_util = match.group(1)
                rendered_value = GeneratorUtils.__render_var(context, mimeo_util[1:][:-1])
                final_rendered_value = value_str.replace(mimeo_util, str(rendered_value))
                return GeneratorUtils.render_value(context, final_rendered_value)
            elif funct_pattern.match(value_str):
                match = next(funct_pattern.finditer(value_str))
                mimeo_util = match.group(1)
                rendered_value = GeneratorUtils.__eval_funct(context, mimeo_util)
                rendered_value_str = str(rendered_value)
                if isinstance(rendered_value, bool):
                    return rendered_value_str.lower()
                return rendered_value_str
        except InvalidMimeoUtil:
            pass
        return value_str

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
        prepared_funct = re.sub(r"random\((.*)\)", r"utils.random(\1)", prepared_funct)
        prepared_funct = re.sub(r"date\((.*)\)", r"utils.date(\1)", prepared_funct)
        prepared_funct = re.sub(r"date_time\((.*)\)", r"utils.date_time(\1)", prepared_funct)
        prepared_funct = re.sub(r"city\((.*)\)", r"utils.city(\1)", prepared_funct)
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
