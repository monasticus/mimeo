from mimeo.utils import RandomStringUtil, RandomIntegerUtil, RandomItemUtil
from mimeo.utils.exc import InvalidMimeoUtil


class MimeoUtilRenderer:

    __MIMEO_UTIL_NAME = "name"
    __MIMEO_UTILS = {
        RandomStringUtil.KEY: RandomStringUtil,
        RandomIntegerUtil.KEY: RandomIntegerUtil,
        RandomItemUtil.KEY: RandomItemUtil,
    }

    @classmethod
    def render_raw(cls, mimeo_util_key: str):
        return cls.render_parametrized({"name": mimeo_util_key})

    @classmethod
    def render_parametrized(cls, mimeo_util_config: dict):
        mimeo_util = cls._get_mimeo_util(mimeo_util_config)
        return mimeo_util(**mimeo_util_config).render()

    @classmethod
    def _get_mimeo_util(cls, mimeo_util_config: dict):
        mimeo_util_key = mimeo_util_config.get(cls.__MIMEO_UTIL_NAME)
        if mimeo_util_key is None:
            raise InvalidMimeoUtil(f"Missing Mimeo Util name in configuration [{mimeo_util_config}]!")

        mimeo_util = cls.__MIMEO_UTILS.get(mimeo_util_key)
        if mimeo_util is None:
            raise InvalidMimeoUtil(f"No such Mimeo Util [{mimeo_util_key}]!")

        return mimeo_util
