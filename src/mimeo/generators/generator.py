"""The Mimeo Generator module.

It exports only one class:
    * Generator
        An abstract class for data generators in Mimeo.
"""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Iterator

from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate


class Generator(metaclass=ABCMeta):
    """An abstract class for data generators in Mimeo.

    Its subclasses are meant to be used in the Mimeo processing.
    Every supported output format has a Generator representation.

    Methods
    -------
    generate(
        templates: Union[list, Iterator[MimeoTemplate]],
        parent: Any = None
    ) -> Iterator[Any]
        Generate data based on the Mimeo Configuration.
    stringify(
        data: Any,
        mimeo_config: MimeoConfig
    ) -> str
        Stringify data generated by the generate() method.
    """

    @classmethod
    def __subclasshook__(
            cls,
            subclass: Generator,
    ):
        """Verify if a subclass implements all abstract methods.

        Parameters
        ----------
        subclass : Generator
            A Generator subclass

        Returns
        -------
        bool
            True if the subclass includes the generate and stringify
            methods
        """
        return ("generate" in subclass.__dict__ and callable(subclass.generate) and
                "stringify" in subclass.__dict__ and callable(subclass.stringify))

    @abstractmethod
    def generate(
            self,
            templates: list | Iterator[MimeoTemplate],
            parent: Any = None,
    ) -> Iterator[Any]:
        """Generate data based on the Mimeo Configuration.

        It is an abstract method to implement in subclasses

        Parameters
        ----------
        templates : Union[list, Iterator[MimeoTemplate]]
            A collection of Mimeo Templates to process
        parent : Any, default None
            A parent node for the currently processed template.
            It is passed only when a Mimeo Config contain nested
            templates.

        Returns
        -------
        Iterator[Any]
            Iterator for generated nodes
        """
        raise NotImplementedError

    @abstractmethod
    def stringify(
            self,
            data_unit: Any,
            mimeo_config: MimeoConfig,
    ) -> str:
        """Stringify data generated by the generate() method.

        It is an abstract method to implement in subclasses

        Parameters
        ----------
        data_unit: Any
            A single data unit generated by the generate() method
        mimeo_config: MimeoConfig
            A Mimeo Configuration providing output details

        Returns
        -------
        str
            Stringified data unit
        """
        raise NotImplementedError
