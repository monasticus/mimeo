import pytest

from mimeo.meta import Alive, OnlyOneAlive
from mimeo.meta.exc import InstanceNotAlive


class SomeClass(Alive, metaclass=OnlyOneAlive):
    pass


def test_only_one_alive_nested_with():

    with SomeClass() as instance1:
        assert instance1 is not None
        assert instance1.is_alive()
        with SomeClass() as instance2:
            assert instance2.is_alive()
            assert instance1 is instance2


def test_only_one_alive_separated_with():
    with SomeClass() as instance3:
        pass
    with SomeClass() as instance4:
        pass

    assert instance3 is not instance4


def test_only_one_alive_outside_with():
    instance1 = SomeClass()
    instance2 = SomeClass()

    assert instance1 is not instance2


def test_only_one_alive_regular_within_with():
    with SomeClass() as instance1:
        instance2 = SomeClass()
        assert instance1 is instance2


def test_assert_alive_true():
    with SomeClass() as instance:
        assert instance.assert_alive()


def test_assert_alive_false():
    instance = SomeClass()
    with pytest.raises(InstanceNotAlive) as err:
        instance.assert_alive()
    assert err.value.args[0] == "The instance is not alive!"
