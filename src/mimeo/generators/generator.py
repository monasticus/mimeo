import xml.etree.ElementTree as ElemTree
from abc import ABCMeta, abstractmethod
from typing import Any, Iterator, Union

from mimeo.config.mimeo_config import MimeoTemplate


class Generator(metaclass=ABCMeta):

    __GENERATOR_UTILS_CALL = "GeneratorUtils.get_for_context('{}').{}"

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'generate') and
                callable(subclass.generate) and
                hasattr(subclass, 'stringify') and
                callable(subclass.stringify) or
                NotImplemented)

    @abstractmethod
    def generate(self,
                 templates: Union[list, Iterator[MimeoTemplate]],
                 parent: Any = None) -> Iterator[ElemTree.Element]:
        raise NotImplementedError

    @abstractmethod
    def stringify(self, data, mimeo_config) -> str:
        raise NotImplementedError
