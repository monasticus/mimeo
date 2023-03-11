import re
from abc import ABCMeta, abstractmethod
from typing import Any, Iterator, Union

from mimeo.generators import GeneratorUtils
from mimeo.model.mimeo_config import MimeoTemplate


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
    def generate(self, templates: Union[list, Iterator[MimeoTemplate]], parent: Any = None) -> Iterator[Any]:
        raise NotImplementedError

    @abstractmethod
    def stringify(self, data, mimeo_config) -> str:
        raise NotImplementedError

    @staticmethod
    def _get_value(literal_value, template):
        literal_value_str = str(literal_value)
        pattern = re.compile("^\{(.*)\}$")
        if pattern.match(literal_value_str):
            match = next(pattern.finditer(literal_value))
            funct = match.group(1)
            return eval(Generator.__GENERATOR_UTILS_CALL.format(template.model.root_name, funct))
        else:
            return literal_value_str if not isinstance(literal_value, bool) else literal_value_str.lower()
