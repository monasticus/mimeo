"""The Mimeo XML Generator module.

It exports only one class:
    * XMLGenerator
        A Generator implementation producing data in the XML format.
"""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ElemTree
from typing import Iterator
from xml.dom import minidom

from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate
from mimeo.context import MimeoContext
from mimeo.context.decorators import (mimeo_clear_iterations, mimeo_context,
                                      mimeo_context_switch,
                                      mimeo_next_iteration)
from mimeo.generators import Generator
from mimeo.generators.exc import UnsupportedStructureError
from mimeo.utils import MimeoRenderer

logger = logging.getLogger(__name__)


class XMLGenerator(Generator):
    """A Generator implementation producing data in the XML format.

    This Generator is instantiated for the 'xml' output format
    and produces data using Mimeo Configuration.

    Methods
    -------
    generate(
        templates: list | Iterator[MimeoTemplate],
        parent: ElemTree.Element = None
    ) -> Iterator[ElemTree.Element]
        Generate XML data based on the Mimeo Configuration.
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
        """Initialize XMLGenerator class.

        Parameters
        ----------
        mimeo_config : MimeoConfig
            A Mimeo Configuration
        """
        self.__indent = mimeo_config.output.indent
        self.__xml_declaration = mimeo_config.output.xml_declaration

    @classmethod
    def generate(
            cls,
            templates: list | Iterator[MimeoTemplate],
            parent: ElemTree.Element = None,
    ) -> Iterator[ElemTree.Element]:
        """Generate XML data based on the Mimeo Configuration.

        This function is used recursively when a Mimeo Configuration
        contains nested templates.
        It iterates through all templates configured and yields data
        units.

        Parameters
        ----------
        templates : list | Iterator[MimeoTemplate]
            A collection of Mimeo Templates to process
        parent : ElemTree.Element, default None
            A parent XML node for the currently processed template.
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
            data_unit: ElemTree.Element,
    ) -> str:
        """Stringify XML data generated by the generate() method.

        Parameters
        ----------
        data_unit: ElemTree.Element
            A single data unit generated by the generate() method

        Returns
        -------
        str
            Stringified data unit
        """
        if self.__indent is None or self.__indent == 0:
            node_str = ElemTree.tostring(
                data_unit,
                encoding="utf-8",
                method="xml",
                xml_declaration=self.__xml_declaration)
        else:
            xml_string = ElemTree.tostring(data_unit)
            xml_minidom = minidom.parseString(xml_string)
            if self.__xml_declaration is False:
                xml_minidom = xml_minidom.childNodes[0]
            node_str = xml_minidom.toprettyxml(
                indent=" " * self.__indent,
                encoding="utf-8")
        return node_str.decode("ascii")

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

        This is a recursive function that traverses Mimeo Template and generates XML
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
                    parent if parent is None else parent.tag, element_meta)
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
        * the value property is being modified for dicts including '_attrs' key
          - the 'attrs' key is removed from the dict
        * the attrs property
          - takes the '_attrs' property value from dicts including '_attrs' key
          - takes the default value (an empty dict) when is None
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
        attrs = element_meta["attrs"]
        is_mimeo_util = MimeoRenderer.is_parametrized_mimeo_util(value)
        is_special_field = MimeoRenderer.is_special_field(tag)
        if is_special_field:
            tag = MimeoRenderer.get_special_field_name(tag)
        if isinstance(value, dict) and MimeoConfig.MODEL_ATTRIBUTES_KEY in value:
            value = dict(value)
            attrs = value.pop(MimeoConfig.MODEL_ATTRIBUTES_KEY)
            value = value.get(MimeoConfig.MODEL_VALUE_KEY, value)
        if attrs is None:
            attrs = {}

        return cls._element_meta(
            tag,
            value,
            attrs,
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
        if isinstance(element_meta["value"], dict):
            func = cls._process_dict_value
        elif (isinstance(element_meta["value"], list) and
              element_meta["tag"] != MimeoConfig.TEMPLATES_KEY):
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
        return element

    @classmethod
    def _process_list_value(
            cls,
            parent: ElemTree.Element,
            element_meta: dict,
    ) -> ElemTree.Element:
        """Process a node with a list value.

        The node is processed accordingly to its children types.

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
            If the list value elements are not atomic-only or dict-only.
        InvalidSpecialFieldValueError
            If the special field value is dict or list
        SpecialFieldNotFoundError
            If the special field does not exist.
        """
        has_only_atomic_values = all(
            not isinstance(child, (list, dict)) or
            MimeoRenderer.is_parametrized_mimeo_util(child)
            for child in element_meta["value"])
        if has_only_atomic_values:
            return cls._process_list_value_with_atomic_children(parent, element_meta)

        has_only_dict_values = all(
            isinstance(child, dict) and
            not MimeoRenderer.is_parametrized_mimeo_util(child)
            for child in element_meta["value"])
        if has_only_dict_values:
            return cls._process_list_value_with_complex_children(parent, element_meta)

        raise UnsupportedStructureError(element_meta["tag"], element_meta["value"])

    @classmethod
    def _process_list_value_with_atomic_children(
            cls,
            parent: ElemTree.Element,
            element_meta: dict,
    ) -> ElemTree.Element:
        """Process a node with a list value having atomic children.

        This method generates a child element for each atomic value as direct children
        of the parent.

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
            value=[],
        )
        cls._process_list_value_with_atomic_children(parent, element_meta)
        ->
        <Root>
            <SomeField>1</SomeField>
            <SomeField>2</SomeField>
        </Root>
        """
        for child in element_meta["value"]:
            element_meta = cls._element_meta(element_meta["tag"], child)
            cls._process_node(parent, element_meta)
        return parent

    @classmethod
    def _process_list_value_with_complex_children(
            cls,
            parent: ElemTree.Element,
            element_meta: dict,
    ) -> ElemTree.Element:
        """Process a node with a list value having complex children.

        It iterates through the list items and processes each of them.

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
            value=[{"SomeChild": {"SomeGrandChild1": 1, "SomeGrandChild2": 2}},
                   {"SomeChild": {"SomeGrandChild1": 'A', "SomeGrandChild2": 'B'}}],
        )
        cls._process_list_value_with_complex_children(parent, element_meta)
        ->
        <SomeField>
            <SomeChild>
                <SomeGrandChild1>1</SomeGrandChild1>
                <SomeGrandChild2>2</SomeGrandChild2>
            </SomeChild>
            <SomeChild>
                <SomeGrandChild1>A</SomeGrandChild1>
                <SomeGrandChild2>B</SomeGrandChild2>
            </SomeChild>
        </SomeField>
        """
        element = cls._create_xml_element(parent, element_meta)
        for child in element_meta["value"]:
            grand_child_tag = next(iter(child))
            grand_child_data = child[grand_child_tag]
            element_meta = cls._element_meta(grand_child_tag, grand_child_data)
            cls._process_node(element, element_meta)
        return element

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
        templates = (MimeoTemplate(template) for template in element_meta["value"])
        for _ in cls.generate(templates, parent):
            pass
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
        element = cls._create_xml_element(parent, element_meta)
        value = MimeoRenderer.render(element_meta["value"])
        if element_meta["special"]:
            context.curr_iteration().add_special_field(element_meta["tag"], value)
        val_str = str(value) if value is not None else ""
        element.text = val_str.lower() if isinstance(value, bool) else val_str
        logger.fine("Rendered value [%s]", element.text)
        return element

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
        """Create an XML element based on the `parent` existence.

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
        if parent is None:
            return ElemTree.Element(
                element_meta["tag"],
                attrib=element_meta["attrs"])
        return ElemTree.SubElement(
            parent,
            element_meta["tag"],
            attrib=element_meta["attrs"],
        )
