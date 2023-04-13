from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.utils.renderer import VarsRenderer


def test_vars_str():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "custom-value-1"
        },
        "_templates_": []
    })
    with MimeoContextManager(config):
        value = VarsRenderer.render("{CUSTOM_VAR_1}")
        assert value == "custom-value-1"


def test_vars_int():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": 1
        },
        "_templates_": []
    })
    with MimeoContextManager(config):
        value = VarsRenderer.render("{CUSTOM_VAR_1}")
        assert value == 1


def test_vars_bool():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": True
        },
        "_templates_": []
    })
    with MimeoContextManager(config):
        value = VarsRenderer.render("{CUSTOM_VAR_1}")
        assert value is True
