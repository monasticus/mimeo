import xml.etree.ElementTree as ElemTree
from typing import Any, Iterator, Union

import tests.utils as test_utils
from mimeo.config.mimeo_config import MimeoTemplate
from mimeo.generators import Generator
from tests.utils import assert_throws


class ValidGenerator(Generator):
    def generate(self,
                 templates: Union[list, Iterator[MimeoTemplate]],
                 parent: Any = None) -> Iterator[ElemTree.Element]:
        pass

    def stringify(self, data: ElemTree.Element) -> str:
        pass


class InvalidGenerator1(Generator):
    def generate(self,
                 templates: Union[list, Iterator[MimeoTemplate]],
                 parent: Any = None) -> Iterator[ElemTree.Element]:
        pass


class InvalidGenerator2(Generator):
    def stringify(self, data: ElemTree.Element) -> str:
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
        raise AssertionError from TypeError


@assert_throws(err_type=TypeError,
               msg=test_utils.get_class_impl_error_msg(
                   "InvalidGenerator1",
                   ["stringify"],
               ))
def test_invalid_class_instantiation_1():
    InvalidGenerator1()


@assert_throws(err_type=TypeError,
               msg=test_utils.get_class_impl_error_msg(
                   "InvalidGenerator2",
                   ["generate"],
               ))
def test_invalid_class_instantiation_2():
    InvalidGenerator2()


@assert_throws(err_type=TypeError,
               msg=test_utils.get_class_impl_error_msg(
                   "InvalidGenerator3",
                   ["generate", "stringify"],
               ))
def test_invalid_class_instantiation_3():
    InvalidGenerator3()
