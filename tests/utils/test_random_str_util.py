from mimeo.utils.exc import InvalidValueError
from mimeo.utils.renderers import UtilsRenderer
from tests.utils import assert_throws


def test_random_str_raw():
    random_str = UtilsRenderer.render_raw("random_str")
    assert isinstance(random_str, str)
    assert len(random_str) == 20


def test_random_str_parametrized_default():
    mimeo_util = {"_name": "random_str"}
    random_str = UtilsRenderer.render_parametrized(mimeo_util)
    assert isinstance(random_str, str)
    assert len(random_str) == 20


def test_random_str_parametrized_custom():
    mimeo_util = {"_name": "random_str", "length": 3}
    random_str = UtilsRenderer.render_parametrized(mimeo_util)
    assert isinstance(random_str, str)
    assert len(random_str) == 3


def test_random_str_parametrized_with_length_zero():
    mimeo_util = {"_name": "random_str", "length": 0}
    random_str = UtilsRenderer.render_parametrized(mimeo_util)
    assert isinstance(random_str, str)
    assert random_str == ""


@assert_throws(err_type=InvalidValueError,
               msg=("The random_str Mimeo Util cannot be parametrized with negative "
                    "length [{length}] value"),
               length=-1)
def test_random_str_parametrized_with_negative_length():
    mimeo_util = {"_name": "random_str", "length": -1}
    UtilsRenderer.render_parametrized(mimeo_util)
