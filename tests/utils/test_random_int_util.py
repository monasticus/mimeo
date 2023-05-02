from mimeo.utils.renderers import UtilsRenderer


def test_random_int_raw():
    random_integers = set()
    for _ in range(100):
        random_int = UtilsRenderer.render_raw("random_int")
        assert isinstance(random_int, int)
        assert random_int >= 1
        assert random_int <= 100
        random_integers.add(random_int)
    assert len(random_integers) > 1


def test_random_int_parametrized_default():
    random_integers = set()
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized({"_name": "random_int"})
        assert isinstance(random_int, int)
        assert random_int >= 1
        assert random_int <= 100
        random_integers.add(random_int)
    assert len(random_integers) > 1


def test_random_int_parametrized_with_start_only():
    random_integers = set()
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized({"_name": "random_int", "start": 0})
        assert isinstance(random_int, int)
        assert random_int >= 0
        assert random_int <= 100
        random_integers.add(random_int)
    assert len(random_integers) > 1


def test_random_int_parametrized_with_limit_only():
    random_integers = set()
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized({"_name": "random_int", "limit": 10})
        assert isinstance(random_int, int)
        assert random_int >= 1
        assert random_int <= 10
        random_integers.add(random_int)
    assert len(random_integers) > 1


def test_random_int_parametrized_with_limit_and_start():
    random_integers = set()
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized({"_name": "random_int", "start": 8, "limit": 10})
        assert isinstance(random_int, int)
        assert random_int >= 8
        assert random_int <= 10
        random_integers.add(random_int)
    assert len(random_integers) > 1
