import pytest

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


def test_does_not_throw_error():
    try:
        ValidConsumer().consume("")
        assert True
    except TypeError:
        assert False


def test_throws_error():
    with pytest.raises(TypeError) as err:
        InvalidConsumer().consume("")

    assert err.value.args[0] == "Can't instantiate abstract class InvalidConsumer with abstract methods consume"
