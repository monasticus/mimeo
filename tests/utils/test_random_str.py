from mimeo.utils import MimeoUtilRenderer


def test_random_str_raw():
    random_str = MimeoUtilRenderer.render_raw("random_str")
    assert isinstance(random_str, str)
    assert len(random_str) == 20


def test_random_str_parametrized_default():
    random_str = MimeoUtilRenderer.render_parametrized({"_name": "random_str"})
    assert isinstance(random_str, str)
    assert len(random_str) == 20


def test_random_str_parametrized_custom():
    random_str = MimeoUtilRenderer.render_parametrized({"_name": "random_str", "length": 3})
    assert isinstance(random_str, str)
    assert len(random_str) == 3
