from mimeo.utils import MimeoUtilRenderer


def test_random_int_raw():
    for _ in range(100):
        random_int = MimeoUtilRenderer.render_raw("random_int")
        assert isinstance(random_int, int)
        assert random_int >= 0
        assert random_int < 100


def test_random_int_parametrized_default():
    for _ in range(100):
        random_int = MimeoUtilRenderer.render_parametrized({"name": "random_int"})
        assert isinstance(random_int, int)
        assert random_int >= 0
        assert random_int < 100


def test_random_int_parametrized_custom():
    for _ in range(100):
        random_int = MimeoUtilRenderer.render_parametrized({"name": "random_int", "limit": 10})
        assert isinstance(random_int, int)
        assert random_int >= 0
        assert random_int < 10