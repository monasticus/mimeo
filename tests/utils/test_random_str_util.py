from mimeo.utils.renderers import UtilsRenderer


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
