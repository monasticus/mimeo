from mimeo.config import MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.utils.renderers import VarsRenderer


def test_vars_str():
    config = MimeoConfigFactory.parse({
        "vars": {
            "CUSTOM_VAR_1": "custom-value-1",
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = VarsRenderer.render("CUSTOM_VAR_1")
        assert value == "custom-value-1"


def test_vars_int():
    config = MimeoConfigFactory.parse({
        "vars": {
            "CUSTOM_VAR_1": 1,
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = VarsRenderer.render("CUSTOM_VAR_1")
        assert value == 1


def test_vars_bool():
    config = MimeoConfigFactory.parse({
        "vars": {
            "CUSTOM_VAR_1": True,
        },
        "_templates_": [],
    })
    with MimeoContextManager(config):
        value = VarsRenderer.render("CUSTOM_VAR_1")
        assert value is True
