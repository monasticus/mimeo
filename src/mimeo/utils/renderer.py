from mimeo.utils import (DateTimeUtil, DateUtil, RandomIntegerUtil,
                         RandomItemUtil, RandomStringUtil)
from mimeo.utils.exc import InvalidMimeoUtil
from mimeo.utils.mimeo_utils import MimeoUtil


class MimeoUtilRenderer:

    _MIMEO_UTIL_NAME = "_name"
    _MIMEO_UTILS = {
        RandomStringUtil.KEY: RandomStringUtil,
        RandomIntegerUtil.KEY: RandomIntegerUtil,
        RandomItemUtil.KEY: RandomItemUtil,
        DateUtil.KEY: DateUtil,
        DateTimeUtil.KEY: DateTimeUtil,
    }
    _INSTANCES = {}

    @classmethod
    def render_raw(cls, mimeo_util_key: str):
        return cls.render_parametrized({cls._MIMEO_UTIL_NAME: mimeo_util_key})

    @classmethod
    def render_parametrized(cls, mimeo_util_config: dict):
        mimeo_util = cls._get_mimeo_util(mimeo_util_config)
        return mimeo_util.render()

    @classmethod
    def _get_mimeo_util(cls, mimeo_util_config: dict) -> MimeoUtil:
        mimeo_util_name = mimeo_util_config.get(cls._MIMEO_UTIL_NAME)
        if mimeo_util_name is None:
            raise InvalidMimeoUtil(f"Missing Mimeo Util name in configuration [{mimeo_util_config}]!")
        elif mimeo_util_name not in cls._MIMEO_UTILS:
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
        mimeo_util = cls._MIMEO_UTILS.get(name)(**config)
        cls._INSTANCES[key] = mimeo_util
        return mimeo_util
