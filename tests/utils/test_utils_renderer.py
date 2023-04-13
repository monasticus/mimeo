import pytest

from mimeo.utils.exc import InvalidMimeoUtil
from mimeo.utils.renderer import UtilsRenderer


def test_missing_mimeo_util_name():
    with pytest.raises(InvalidMimeoUtil) as err:
        UtilsRenderer.render_parametrized({})

    assert err.value.args[0] == "Missing Mimeo Util name in configuration [{}]!"


def test_no_such_mimeo_util_raw():
    with pytest.raises(InvalidMimeoUtil) as err:
        UtilsRenderer.render_raw("non-existing-util")

    assert err.value.args[0] == "No such Mimeo Util [non-existing-util]!"


def test_no_such_mimeo_util_parametrized():
    with pytest.raises(InvalidMimeoUtil) as err:
        UtilsRenderer.render_parametrized({"_name": "non-existing-util"})

    assert err.value.args[0] == "No such Mimeo Util [non-existing-util]!"