from mimeo.utils.exc import InvalidValueError
from mimeo.utils.renderers import UtilsRenderer
from tests.utils import assert_throws


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
    mimeo_util = {"_name": "random_int"}
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized(mimeo_util)
        assert isinstance(random_int, int)
        assert random_int >= 1
        assert random_int <= 100
        random_integers.add(random_int)
    assert len(random_integers) > 1


def test_random_int_parametrized_with_start_only():
    random_integers = set()
    mimeo_util = {"_name": "random_int", "start": 0}
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized(mimeo_util)
        assert isinstance(random_int, int)
        assert random_int >= 0
        assert random_int <= 100
        random_integers.add(random_int)
    assert len(random_integers) > 1


def test_random_int_parametrized_with_limit_only():
    random_integers = set()
    mimeo_util = {"_name": "random_int", "limit": 10}
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized(mimeo_util)
        assert isinstance(random_int, int)
        assert random_int >= 1
        assert random_int <= 10
        random_integers.add(random_int)
    assert len(random_integers) > 1


def test_random_int_parametrized_with_limit_and_start():
    mimeo_util = {"_name": "random_int", "start": 8, "limit": 10}
    random_integers = set()
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized(mimeo_util)
        assert isinstance(random_int, int)
        assert random_int >= 8
        assert random_int <= 10
        random_integers.add(random_int)
    assert len(random_integers) > 1


def test_random_int_parametrized_with_limit_same_as_start():
    mimeo_util = {"_name": "random_int", "start": 1, "limit": 1}
    for _ in range(100):
        random_int = UtilsRenderer.render_parametrized(mimeo_util)
        assert isinstance(random_int, int)
        assert random_int == 1


@assert_throws(err_type=InvalidValueError,
               msg=("The random_int Mimeo Util cannot be parametrized with limit "
                    "[{limit}] lower than start [{start}]"),
               start=2, limit=1)
def test_random_int_parametrized_with_limit_lower_than_start():
    mimeo_util = {"_name": "random_int", "start": 2, "limit": 1}
    UtilsRenderer.render_parametrized(mimeo_util)
