import pytest

from mimeo.utils import MimeoUtilRenderer
from mimeo.utils.exc import InvalidMimeoUtil


def test_missing_mimeo_util_name():
    with pytest.raises(InvalidMimeoUtil) as err:
        MimeoUtilRenderer.render_parametrized({})

    assert err.value.args[0] == "Missing Mimeo Util name in configuration [{}]!"


def test_no_such_mimeo_util_raw():
    with pytest.raises(InvalidMimeoUtil) as err:
        MimeoUtilRenderer.render_raw("non-existing-util")

    assert err.value.args[0] == "No such Mimeo Util [non-existing-util]!"


def test_no_such_mimeo_util_parametrized():
    with pytest.raises(InvalidMimeoUtil) as err:
        MimeoUtilRenderer.render_parametrized({"_name": "non-existing-util"})

    assert err.value.args[0] == "No such Mimeo Util [non-existing-util]!"


def test_is_raw_mimeo_util_true():
    assert MimeoUtilRenderer.is_raw_mimeo_util("{random_str}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{random_int}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{random_item}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{date}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{date_time}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{auto_increment}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{curr_iter}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{key}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{city}")
    assert MimeoUtilRenderer.is_raw_mimeo_util("{country}")


def test_is_raw_mimeo_util_false():
    assert not MimeoUtilRenderer.is_raw_mimeo_util("random_str")
    assert not MimeoUtilRenderer.is_raw_mimeo_util("{random}")


def test_is_parametrized_mimeo_util_true():
    assert MimeoUtilRenderer.is_parametrized_mimeo_util({
        "_mimeo_util": {}
    })


def test_is_parametrized_mimeo_util_false():
    assert not MimeoUtilRenderer.is_parametrized_mimeo_util({
        "_mimeo_util": {},
        "key": "value"
    })
    assert not MimeoUtilRenderer.is_parametrized_mimeo_util({
        "_util": {}
    })
    assert not MimeoUtilRenderer.is_parametrized_mimeo_util([
        {
            "_mimeo_util": {}
        }
    ])
