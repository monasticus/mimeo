import logging
import re

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContext, MimeoContextManager
from mimeo.context.annotations import mimeo_context
from mimeo.context.exc import VarNotFound
from mimeo.utils import (AutoIncrementUtil, CityUtil, CountryUtil,
                         CurrentIterationUtil, DateTimeUtil, DateUtil,
                         FirstNameUtil, KeyUtil, LastNameUtil, MimeoUtil,
                         RandomIntegerUtil, RandomItemUtil, RandomStringUtil)
from mimeo.utils.exc import InvalidMimeoUtil, InvalidValue, NotASpecialField

logger = logging.getLogger(__name__)


class UtilsRenderer:

    MIMEO_UTIL_NAME = "_name"
    MIMEO_UTILS = {
        RandomStringUtil.KEY: RandomStringUtil,
        RandomIntegerUtil.KEY: RandomIntegerUtil,
        RandomItemUtil.KEY: RandomItemUtil,
        DateUtil.KEY: DateUtil,
        DateTimeUtil.KEY: DateTimeUtil,
        AutoIncrementUtil.KEY: AutoIncrementUtil,
        CurrentIterationUtil.KEY: CurrentIterationUtil,
        KeyUtil.KEY: KeyUtil,
        CityUtil.KEY: CityUtil,
        CountryUtil.KEY: CountryUtil,
        FirstNameUtil.KEY: FirstNameUtil,
        LastNameUtil.KEY: LastNameUtil,
    }
    _INSTANCES = {}

    @classmethod
    def render_raw(cls, mimeo_util_key: str):
        return cls.render_parametrized({MimeoConfig.MODEL_MIMEO_UTIL_NAME_KEY: mimeo_util_key})

    @classmethod
    def render_parametrized(cls, mimeo_util_config: dict):
        logger.fine(f"Rendering a mimeo util [{mimeo_util_config}]")
        mimeo_util = cls._get_mimeo_util(mimeo_util_config)
        return mimeo_util.render()

    @classmethod
    def _get_mimeo_util(cls, mimeo_util_config: dict) -> MimeoUtil:
        mimeo_util_name = mimeo_util_config.get(MimeoConfig.MODEL_MIMEO_UTIL_NAME_KEY)
        if mimeo_util_name is None:
            raise InvalidMimeoUtil(f"Missing Mimeo Util name in configuration [{mimeo_util_config}]!")
        elif mimeo_util_name not in cls.MIMEO_UTILS:
            raise InvalidMimeoUtil(f"No such Mimeo Util [{mimeo_util_name}]!")

        mimeo_util_key = cls._generate_key(mimeo_util_config)
        if mimeo_util_key not in cls._INSTANCES:
            mimeo_util = cls._instantiate_mimeo_util(mimeo_util_name, mimeo_util_key, mimeo_util_config)
        else:
            mimeo_util = cls._INSTANCES.get(mimeo_util_key)

        return mimeo_util

    @staticmethod
    def _generate_key(mimeo_util_config: dict) -> str:
        return "-".join(":".join([key, str(val)]) for key, val in mimeo_util_config.items())

    @classmethod
    def _instantiate_mimeo_util(cls, name: str, key: str, config: dict) -> MimeoUtil:
        mimeo_util = cls.MIMEO_UTILS.get(name)(**config)
        cls._INSTANCES[key] = mimeo_util
        return mimeo_util


class VarsRenderer:

    @classmethod
    def render(cls, var: str):
        logger.fine(f"Rendering a variable [{var}]")
        return MimeoContextManager().get_var(var)


class SpecialFieldsRenderer:

    @classmethod
    @mimeo_context
    def render(cls, field_name: str, context: MimeoContext = None):
        logger.fine(f"Rendering a special field [{field_name}]")
        return context.curr_iteration().get_special_field(field_name)


class MimeoRenderer:

    _UTILS_PATTERN = re.compile("^{(.+)}$")
    _VARS_PATTERN = re.compile(".*({[A-Z_0-9]+})")
    _SPECIAL_FIELDS_PATTERN = re.compile(".*({:([a-zA-Z]+:)?[-_a-zA-Z0-9]+:})")

    @classmethod
    def get_special_field_name(cls, field_name: str) -> str:
        if not cls.is_special_field(field_name):
            raise NotASpecialField(f"Provided field [{field_name}] is not a special one (use {'{:NAME:}'})!")

        return field_name[2:][:-2]

    @classmethod
    def is_special_field(cls, field_name: str) -> bool:
        return bool(re.match(r"^{:([a-zA-Z]+:)?[-_a-zA-Z0-9]+:}$", field_name))

    @classmethod
    def is_raw_mimeo_util(cls, value: str):
        raw_mimeo_utils = UtilsRenderer.MIMEO_UTILS.keys()
        raw_mimeo_utils_re = "^{(" + "|".join(raw_mimeo_utils) + ")}$"
        return bool(re.match(raw_mimeo_utils_re, value))

    @classmethod
    def is_parametrized_mimeo_util(cls, value: dict):
        return isinstance(value, dict) and len(value) == 1 and MimeoConfig.MODEL_MIMEO_UTIL_KEY in value

    @classmethod
    def render(cls, value):
        logger.fine(f"Rendering a value [{value}]")
        try:
            if isinstance(value, str):
                return cls._render_string_value(value)
            elif cls.is_parametrized_mimeo_util(value):
                return cls._render_parametrized_mimeo_util(value)
            else:
                return value
        except (InvalidMimeoUtil, VarNotFound, InvalidValue) as err:
            error_name = type(err).__name__
            logger.error(f"The [{error_name}] error occurred during rendering a value [{value}]: [{err}].")
            raise err

    @classmethod
    def _render_string_value(cls, value: str):
        if cls._SPECIAL_FIELDS_PATTERN.match(value):
            return cls._render_special_field(value)
        elif cls._VARS_PATTERN.match(value):
            return cls._render_var(value)
        elif cls.is_raw_mimeo_util(value):
            return cls._render_raw_mimeo_util(value)
        else:
            return value

    @classmethod
    def _render_special_field(cls, value):
        match = next(cls._SPECIAL_FIELDS_PATTERN.finditer(value))
        wrapped_special_field = match.group(1)
        rendered_value = SpecialFieldsRenderer.render(wrapped_special_field[2:][:-2])
        logger.fine(f"Rendered special field value [{rendered_value}]")
        if len(wrapped_special_field) != len(value):
            rendered_value = str(rendered_value).lower() if isinstance(rendered_value, bool) else str(rendered_value)
            rendered_value = value.replace(wrapped_special_field, str(rendered_value))
        return cls.render(rendered_value)

    @classmethod
    def _render_var(cls, value):
        match = next(cls._VARS_PATTERN.finditer(value))
        wrapped_var = match.group(1)
        rendered_value = VarsRenderer.render(wrapped_var[1:][:-1])
        logger.fine(f"Rendered variable value [{rendered_value}]")
        if cls.is_parametrized_mimeo_util(rendered_value):
            rendered_value = cls._render_parametrized_mimeo_util(rendered_value)
        if len(wrapped_var) != len(value):
            rendered_value = str(rendered_value).lower() if isinstance(rendered_value, bool) else str(rendered_value)
            rendered_value = value.replace(wrapped_var, str(rendered_value))
        return cls.render(rendered_value)

    @classmethod
    def _render_raw_mimeo_util(cls, value):
        rendered_value = UtilsRenderer.render_raw(value[1:][:-1])
        return cls.render(rendered_value)

    @classmethod
    def _render_parametrized_mimeo_util(cls, value: dict):
        mimeo_util = value[MimeoConfig.MODEL_MIMEO_UTIL_KEY]
        mimeo_util = cls._render_mimeo_util_parameters(mimeo_util)
        logger.fine(f"Pre-rendered mimeo util [{mimeo_util}]")
        rendered_value = UtilsRenderer.render_parametrized(mimeo_util)
        return cls.render(rendered_value)

    @classmethod
    def _render_mimeo_util_parameters(cls, mimeo_util_config: dict) -> dict:
        logger.fine("Rendering mimeo util parameters")
        return {key: cls.render(value) if key != "_name" else value for key, value in mimeo_util_config.items()}
