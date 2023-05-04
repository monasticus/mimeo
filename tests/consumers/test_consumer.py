import pytest

import tests.utils as test_utils
from mimeo.consumers import Consumer


class ValidConsumer(Consumer):
    def consume(self, data: str):
        pass


class InvalidConsumer(Consumer):
    pass


def test_issubclass_true():
    assert issubclass(ValidConsumer, Consumer)


def test_issubclass_false():
    assert not issubclass(InvalidConsumer, Consumer)


def test_valid_class_instantiation():
    try:
        ValidConsumer()
        assert True
    except TypeError:
        assert False


def test_invalid_class_instantiation():
    with pytest.raises(TypeError) as err:
        InvalidConsumer()

    assert err.value.args[0] == test_utils.get_class_impl_error_msg("InvalidConsumer", ["consume"])
