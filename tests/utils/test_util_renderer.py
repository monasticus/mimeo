import pytest

from mimeo.utils import UtilsRenderer
from mimeo.utils.exc import InvalidMimeoUtil


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


def test_is_raw_mimeo_util_true():
    assert UtilsRenderer.is_raw_mimeo_util("{random_str}")
    assert UtilsRenderer.is_raw_mimeo_util("{random_int}")
    assert UtilsRenderer.is_raw_mimeo_util("{random_item}")
    assert UtilsRenderer.is_raw_mimeo_util("{date}")
    assert UtilsRenderer.is_raw_mimeo_util("{date_time}")
    assert UtilsRenderer.is_raw_mimeo_util("{auto_increment}")
    assert UtilsRenderer.is_raw_mimeo_util("{curr_iter}")
    assert UtilsRenderer.is_raw_mimeo_util("{key}")
    assert UtilsRenderer.is_raw_mimeo_util("{city}")
    assert UtilsRenderer.is_raw_mimeo_util("{country}")


def test_is_raw_mimeo_util_false():
    assert not UtilsRenderer.is_raw_mimeo_util("random_str")
    assert not UtilsRenderer.is_raw_mimeo_util("{random}")


def test_is_parametrized_mimeo_util_true():
    assert UtilsRenderer.is_parametrized_mimeo_util({
        "_mimeo_util": {}
    })


def test_is_parametrized_mimeo_util_false():
    assert not UtilsRenderer.is_parametrized_mimeo_util({
        "_mimeo_util": {},
        "key": "value"
    })
    assert not UtilsRenderer.is_parametrized_mimeo_util({
        "_util": {}
    })
    assert not UtilsRenderer.is_parametrized_mimeo_util([
        {
            "_mimeo_util": {}
        }
    ])
