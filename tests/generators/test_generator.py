import xml.etree.ElementTree as ElemTree
from typing import Any, Iterator, Union

import pytest

import tests.utils as test_utils
from mimeo.config import MimeoConfig
from mimeo.config.mimeo_config import MimeoTemplate
from mimeo.generators import Generator


class ValidGenerator(Generator):
    def generate(self,
                 templates: Union[list, Iterator[MimeoTemplate]],
                 parent: Any = None) -> Iterator[ElemTree.Element]:
        pass

    def stringify(self, data: ElemTree.Element, mimeo_config: MimeoConfig) -> str:
        pass


class InvalidGenerator1(Generator):
    def generate(self,
                 templates: Union[list, Iterator[MimeoTemplate]],
                 parent: Any = None) -> Iterator[ElemTree.Element]:
        pass


class InvalidGenerator2(Generator):
    def stringify(self, data: ElemTree.Element, mimeo_config: MimeoConfig) -> str:
        pass


class InvalidGenerator3(Generator):
    pass


def test_issubclass_true():
    assert issubclass(ValidGenerator, Generator)


def test_issubclass_false():
    assert not issubclass(InvalidGenerator1, Generator)
    assert not issubclass(InvalidGenerator2, Generator)
    assert not issubclass(InvalidGenerator3, Generator)


def test_valid_class_instantiation():
    try:
        ValidGenerator()
        assert True
    except TypeError:
        assert False


def test_invalid_class_instantiation():
    with pytest.raises(TypeError) as err:
        InvalidGenerator1()

    assert err.value.args[0] == test_utils.get_class_impl_error_msg("InvalidGenerator1", ["stringify"])

    with pytest.raises(TypeError) as err:
        InvalidGenerator2()

    assert err.value.args[0] == test_utils.get_class_impl_error_msg("InvalidGenerator2", ["generate"])

    with pytest.raises(TypeError) as err:
        InvalidGenerator3()

    assert err.value.args[0] == test_utils.get_class_impl_error_msg("InvalidGenerator3", ["generate", "stringify"])
