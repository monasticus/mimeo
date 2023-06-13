"""The Mimeo JSON Generator module.

It exports only one class:
    * JSONGenerator
        A Generator implementation producing data in the JSON format.
"""
from __future__ import annotations

import json
import logging
import xml.etree.ElementTree as ElemTree
from typing import Iterator

from mimeo.config import constants as cc
from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate
from mimeo.context import MimeoContext
from mimeo.context.decorators import (mimeo_clear_iterations, mimeo_context,
                                      mimeo_context_switch,
                                      mimeo_next_iteration)
from mimeo.generators import Generator
from mimeo.utils import MimeoRenderer

logger = logging.getLogger(__name__)


class JSONGenerator(Generator):
    """A Generator implementation producing data in the JSON format.

    This Generator is instantiated for the 'json' output format
    and produces data using Mimeo Configuration.

    Methods
    -------
    generate(
        templates: list | Iterator[MimeoTemplate],
        parent: dict | list = None
    ) -> Iterator[dict]
        Generate JSON data based on the Mimeo Configuration.
    stringify(
        data: Any,
        mimeo_config: MimeoConfig
    ) -> str
        Stringify data generated by the generate() method.
    """

    def __init__(
            self,
            mimeo_config: MimeoConfig,
    ):
        """Initialize JSONGenerator class.

        Parameters
        ----------
        mimeo_config : MimeoConfig
            A Mimeo Configuration
        """
        self.__indent = mimeo_config.output.indent

    @classmethod
    def generate(
            cls,
            templates: list | Iterator[MimeoTemplate],
            parent: dict | list = None,
    ) -> Iterator[dict]:
        """Generate JSON data based on the Mimeo Configuration.

        This function is used recursively when a Mimeo Configuration
        contains nested templates.
        It iterates through all templates configured and yields data
        units.

        Parameters
        ----------
        templates : list | Iterator[MimeoTemplate]
            A collection of Mimeo Templates to process
        parent : ElemTree.Element, default None
            A parent JSON node for the currently processed template.
            It is passed only when a Mimeo Config contain nested
            templates.

        Returns
        -------
        Iterator[ElemTree.Element]
            Iterator for generated nodes
        """
        for template in templates:
            for data_unit in cls._process_single_template(template, parent):
                yield data_unit

    def stringify(
            self,
            data_unit: dict,
    ) -> str:
        """Stringify JSON data generated by the generate() method.

        Parameters
        ----------
        data_unit: dict
            A single data unit generated by the generate() method

        Returns
        -------
        str
            Stringified data unit
        """
        if self.__indent is not None and self.__indent != 0:
            return json.dumps(data_unit, indent=self.__indent)

        return json.dumps(data_unit)

    @classmethod
    @mimeo_context_switch
    @mimeo_clear_iterations
    def _process_single_template(
            cls,
            template: MimeoTemplate,
            parent: ElemTree.Element = None,
    ) -> list[ElemTree.Element]:
        """Process a single Mimeo Template.

        This function is used recursively when a Mimeo Configuration
        contains nested templates.
        It repeats same processing operation so many times as it is
        configured in the `count` property of a Mimeo Configuration.
        Before the template execution it switches context managed by
        MimeoContextManager and also clears iterations as nested
        templates would collect iterations from previous parent's
        iterations.

        Parameters
        ----------
        template : MimeoTemplate
            A single Mimeo Template to process
        parent : ElemTree.Element, default None
            A parent node for processing nested templates

        Returns
        -------
        list[ElemTree.Element]
            A list of generated data units
        """
        logger.debug("Reading template [%s]", template)
        return [cls._process_single_data_unit(template, parent)
                for _ in iter(range(template.count))]

    @classmethod
    @mimeo_next_iteration
    def _process_single_data_unit(
            cls,
            template: MimeoTemplate,
            parent: ElemTree.Element = None,
    ) -> ElemTree.Element:
        """Process a single data unit from the template.

        This function is used recursively when a Mimeo Configuration
        contains nested templates.
        It processes a single data unit. The reason why it is separated
        from the _process_node() function is the @mimeo_next_iteration
        decorator. The _process_node() function is recursively called
        by itself, and it produces data for a single iteration.
        The purpose of this function is to increment iteration before
        processing node.

        Parameters
        ----------
        template : MimeoTemplate
            A single Mimeo Template to process
        parent : ElemTree.Element, default None
            A parent node for processing nested templates

        Returns
        -------
        ElemTree.Element
            A single data unit generated within a single template
            iteration. If the `parent` is not None it will not return
            any value.
        """
        parent = parent if parent is not None else {}
        element_meta = cls._element_meta(
            template.model.root_name,
            template.model.root_data)
        return cls._process_node(parent, element_meta)

    @classmethod
    @mimeo_context
    def _process_node(
            cls,
            parent: ElemTree.Element | None,
            element_meta: dict,
            context: MimeoContext = None,
    ) -> ElemTree.Element:
        """Process a single template's node.

        This is a recursive function that traverses Mimeo Template and generates JSON
        nodes based on element's metadata. First, element is pre-processed, in meaning
        of metadata being adjusted. Then, element is processed accordingly to its value
        type.

        Parameters
        ----------
        parent : ElemTree.Element | None
            A parent node
        element_meta : dict
            Element's metadata
        context : MimeoContext, default None
            The current Mimeo Context (injected by MimeoContextManager)

        Returns
        -------
        ElemTree.Element
            A single data unit generated within a single template iteration.

        Raises
        ------
        UnsupportedStructureError
            If a list value elements are not atomic-only or dict-only.
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.
        """
        logger.fine("Rendering element - parent [%s], element_meta [%s]",
                    parent, element_meta)
        element_meta = cls._pre_process_node(element_meta)

        if cls._is_complex(element_meta):
            return cls._process_complex_value(parent, element_meta)
        return cls._process_atomic_value(parent, element_meta, context)

    @classmethod
    def _pre_process_node(
            cls,
            element_meta: dict,
    ) -> dict:
        """Pre-process element's metadata.

        This function adjusts existing element's metadata and completes it with custom
        properties:
        * the tag property is changed only for special fields
          - field name is extracted
        * the value property is being modified for dicts including attributes
          - properties starting with '@' are being removed from the dict
        * the attrs property
          - is being populated by all properties starting with '@'
          - takes the default value (an empty dict) when there's no such properties
        * the mimeo_util property is being initialized
          - True if element's value is a parametrized mimeo_util. Otherwise, False.
        * the special property is being initialized
          - True, when a field is special. Otherwise, False.

        Parameters
        ----------
        element_meta : dict
            Initial element's metadata

        Returns
        -------
        dict
            Complete element's metadata
        """
        tag = element_meta["tag"]
        value = element_meta["value"]
        is_mimeo_util = MimeoRenderer.is_parametrized_mimeo_util(value)
        is_special_field = MimeoRenderer.is_special_field(tag)
        if is_special_field:
            tag = MimeoRenderer.get_special_field_name(tag)

        return cls._element_meta(
            tag,
            value,
            None,
            is_mimeo_util,
            is_special_field)

    @staticmethod
    def _is_complex(
            element_meta: dict,
    ) -> bool:
        """Verify if an element is complex.

        Parameters
        ----------
        element_meta : dict
            Element's metadata

        Returns
        -------
        bool
            True if element's value is a list or a dict not being a parametrized
            Mimeo Util. Otherwise, False.
        """
        return (isinstance(element_meta["value"], (list, dict)) and
                not element_meta["mimeo_util"])

    @classmethod
    def _process_complex_value(
            cls,
            parent: ElemTree.Element | None,
            element_meta: dict,
    ) -> ElemTree.Element | None:
        """Process a node with a complex value.

        The node is processed accordingly to its value type.
        When the type is list and tag is _templates_, node is processed
        in a special way.

        Parameters
        ----------
        parent : ElemTree.Element | None
            A parent node
        element_meta : dict
            Element's metadata

        Returns
        -------
        ElemTree.Element
            A processed node

        Raises
        ------
        UnsupportedStructureError
            If a list value elements are not atomic-only or dict-only.
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.
        """
        if (isinstance(element_meta["value"], dict) and
                cc.TEMPLATES_KEY not in element_meta["value"]):
            func = cls._process_dict_value
        elif (isinstance(element_meta["value"], list) and
              element_meta["tag"] != cc.TEMPLATES_KEY):
            func = cls._process_list_value
        else:
            func = cls._process_templates_value
        return func(parent, element_meta)

    @classmethod
    def _process_dict_value(
            cls,
            parent: ElemTree.Element | None,
            element_meta: dict,
    ) -> ElemTree.Element:
        """Process a node with a dictionary value.

        It iterates through the dictionary items and processes each of them.

        Parameters
        ----------
        parent : ElemTree.Element | None
            A parent node
        element_meta : dict
            Element's metadata

        Returns
        -------
        ElemTree.Element
            A processed node

        Raises
        ------
        UnsupportedStructureError
            If a list value elements are not atomic-only or dict-only.
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.

        Examples
        --------
        parent = ElemTree.Element("Root")
        element_meta = cls._element_meta(
            tag="SomeField",
            value={"SomeChild1": 1, "SomeChild2": 2},
        )
        cls._process_dict_value(parent, element_meta)
        ->
        <SomeField>
            <SomeChild1>1</SomeChild1>
            <SomeChild2>2</SomeChild2>
        </SomeField>
        """
        element = cls._create_xml_element(parent, element_meta)
        for child_tag, child_value in element_meta["value"].items():
            cls._process_node(element, cls._element_meta(child_tag, child_value))
        return parent

    @classmethod
    def _process_list_value(
            cls,
            parent: ElemTree.Element,
            element_meta: dict,
    ) -> ElemTree.Element:
        """Process a node with a list value.

        It iterates through the list items and processes each of them: generates
        a child element for each value as direct children of the parent.

        Parameters
        ----------
        parent : ElemTree.Element | None
            A parent node
        element_meta : dict
            Element's metadata

        Returns
        -------
        ElemTree.Element
            A processed node

        Raises
        ------
        UnsupportedStructureError
            If any of the list value element is a list.
        InvalidSpecialFieldValueError
            If the special field value is dict or list
        SpecialFieldNotFoundError
            If the special field does not exist.

        Examples
        --------
        parent = ElemTree.Element("Root")
        element_meta = cls._element_meta(
            tag="SomeField",
            value=[
                'value-1',
                {'SomeChild1': True, 'SomeChild2': False},
                {'_mimeo_util': {'_name': 'auto_increment', 'pattern': '{}'}}
            ],
        )
        cls._process_list_value_with_atomic_children(parent, element_meta)
        ->
        <Root>
            <SomeField>value-1</SomeField>
            <SomeField>
                <SomeChild1>true</SomeChild1>
                <SomeChild2>false</SomeChild2>
            </SomeField>
            <SomeField>1</SomeField>
        </Root>
        """
        element = cls._create_xml_element(parent, element_meta)
        for child in element_meta["value"]:
            element_meta = cls._element_meta(element_meta["tag"], child)
            cls._process_node(element, element_meta)
        return parent

    @classmethod
    def _process_templates_value(
            cls,
            parent: ElemTree.Element,
            element_meta: dict,
    ) -> ElemTree.Element:
        """Process a node with a dictionary value storing templates.

        It iterates through the templates and generates data based on them.

        Parameters
        ----------
        parent : ElemTree.Element | None
            A parent node
        element_meta : dict
            Element's metadata

        Returns
        -------
        ElemTree.Element
            A processed node

        Raises
        ------
        UnsupportedStructureError
            If a list value elements are not atomic-only or dict-only.
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.

        Examples
        --------
        parent = ElemTree.Element("Root")
        element_meta = cls._element_meta(
            tag="SomeField",
            value={"_templates_": [
                {
                  "count": 10,
                  "model": {
                    "SomeChild": {
                      "Node1": 1,
                      "Node2": "value-2",
                      "Node3": true
                    }
                  }
                }
            ]},
        )
        cls._process_templates_value(parent, element_meta)
        ->
        <Root>
            <SomeField>
                <SomeChild><Node1>1</Node1><Node2>value-2</Node2><Node3>true</Node3></SomeChild>
                <SomeChild><Node1>1</Node1><Node2>value-2</Node2><Node3>true</Node3></SomeChild>
                ... x10
            </SomeField>
        </Root>
        """
        templates = (MimeoTemplate(template)
                     for template in element_meta["value"][cc.TEMPLATES_KEY])
        target = parent
        if isinstance(parent, dict):
            parent[element_meta["tag"]] = []
            target = parent[element_meta["tag"]]

        for child in cls.generate(templates):
            target.append(child)
        return parent

    @classmethod
    def _process_atomic_value(
            cls,
            parent: ElemTree.Element,
            element_meta: dict,
            context: MimeoContext,
    ) -> ElemTree.Element:
        """Process a node with an atomic value.

        A parametrized Mimeo Util is considered as an atomic value as representing one.
        It renders a value for the node.

        Parameters
        ----------
        parent : ElemTree.Element | None
            A parent node
        element_meta : dict
            Element's metadata
        context : MimeoContext, default None
            The current Mimeo Context (injected by MimeoContextManager)

        Returns
        -------
        ElemTree.Element
            A processed node

        Raises
        ------
        UnsupportedStructureError
            If a list value elements are not atomic-only or dict-only.
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.

        Examples
        --------
        context = MimeoContextManager().get_current_context()
        parent = ElemTree.Element("Root")
        element_meta = cls._element_meta(
            tag="SomeField",
            value="value-1",
        )
        cls._process_atomic_value(parent, element_meta, context)
        ->
        <SomeField>value-1</SomeField>
        """
        value = MimeoRenderer.render(element_meta["value"])
        if element_meta["special"]:
            context.curr_iteration().add_special_field(element_meta["tag"], value)
        if isinstance(parent, dict):
            parent[element_meta["tag"]] = value
        elif isinstance(parent, list):
            parent.append(value)
        logger.fine("Rendered value [%s]", value)
        return parent

    @staticmethod
    def _element_meta(
            tag: str,
            value: dict | list | str | int | float | bool,
            attrs: dict | None = None,
            is_mimeo_util: bool | None = None,
            is_special_field: bool | None = None,
    ) -> dict:
        """Build element's metadata.

        Parameters
        ----------
        tag : str
            An element's tag
        value : dict | list | str | int | float | bool
            An element's value
        attrs : dict | None, default None
            An element's attributes
        is_mimeo_util : bool | None, default None
            A is-mimeo-util flag
        is_special_field : bool | None, default None
            A is-special-field flag

        Returns
        -------
        dict
            Element's metadata
        """
        return {
            "tag": tag,
            "value": value,
            "attrs": attrs,
            "mimeo_util": is_mimeo_util,
            "special": is_special_field,
        }

    @staticmethod
    def _create_xml_element(
            parent: ElemTree.Element,
            element_meta: dict,
    ) -> ElemTree.Element | ElemTree.SubElement:
        """Create an JSON element based on the `parent` existence.

        Parameters
        ----------
        parent : ElemTree.Element
            A parent node
        element_meta : dict
            Element's metadata

        Returns
        -------
        ElemTree.Element | ElemTree.SubElement
            If the `parent` is None, returns ElemTree.Element.
            Otherwise, returns ElemTree.SubElement
        """
        if isinstance(parent, dict):
            if isinstance(element_meta["value"], dict):
                parent[element_meta["tag"]] = {}
            elif isinstance(element_meta["value"], list):
                parent[element_meta["tag"]] = []
            return parent[element_meta["tag"]]
        if isinstance(parent, list):
            if isinstance(element_meta["value"], dict):
                parent.append({})
            elif isinstance(element_meta["value"], list):
                parent.append([])
            return parent[-1]
