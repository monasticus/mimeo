import re
import xml.etree.ElementTree as ElemTree
from abc import ABCMeta, abstractmethod
from typing import Any, Iterator, Union

from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate
from mimeo.exceptions import InvalidMimeoUtil
from mimeo.generators import GeneratorUtils


class Generator(metaclass=ABCMeta):

    __GENERATOR_UTILS_CALL = "GeneratorUtils.get_for_context('{}').{}"

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'generate') and
                callable(subclass.generate) and
                hasattr(subclass, 'stringify') and
                callable(subclass.stringify) or
                NotImplemented)

    def __init__(self, mimeo_config: MimeoConfig):
        GeneratorUtils.setup(mimeo_config)

    @abstractmethod
    def generate(self,
                 templates: Union[list, Iterator[MimeoTemplate]],
                 parent: Any = None) -> Iterator[ElemTree.Element]:
        raise NotImplementedError

    @abstractmethod
    def stringify(self, data, mimeo_config) -> str:
        raise NotImplementedError

    @staticmethod
    def _get_value(literal_value, template):
        literal_value_str = str(literal_value)
        pattern = re.compile("^{(.+)}$")
        if pattern.match(literal_value_str):
            try:
                match = next(pattern.finditer(literal_value))
                funct = match.group(1)
                value = GeneratorUtils.eval(template.model.root_name, funct)
                return str(value)
            except InvalidMimeoUtil:
                pass

        return literal_value_str if not isinstance(literal_value, bool) else literal_value_str.lower()
