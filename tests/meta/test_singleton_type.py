from mimeo.meta import Singleton


class SomeClass(metaclass=Singleton):
    pass


class SomeParametrizedClass(metaclass=Singleton):

    def __init__(self, name: str = "Tom"):
        self.name = name


def test_singleton():
    instance1 = SomeClass()
    instance2 = SomeClass()

    assert instance1 is instance2


def test_singleton_parametrized():
    instance1 = SomeParametrizedClass("Jerry")
    instance2 = SomeParametrizedClass()

    assert instance1.name == "Jerry"
    assert instance2.name == "Jerry"
