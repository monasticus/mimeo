"""The Mimeo XML Generator module.

It exports only one class:
    * XMLGenerator
        A Generator implementation producing data in the XML format.
"""
import logging
import xml.etree.ElementTree as ElemTree
from typing import Iterator, List, Union, Optional
from xml.dom import minidom

from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate
from mimeo.context import MimeoContext
from mimeo.context.decorators import (mimeo_clear_iterations, mimeo_context,
                                      mimeo_context_switch,
                                      mimeo_next_iteration)
from mimeo.generators import Generator
from mimeo.utils import MimeoRenderer

logger = logging.getLogger(__name__)


class XMLGenerator(Generator):
    """A Generator implementation producing data in the XML format.

    This Generator is instantiated for the 'xml' output format
    and produces data using Mimeo Configuration.

    Methods
    -------
    generate(
        templates: Union[list, Iterator[MimeoTemplate]],
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
            templates: Union[list, Iterator[MimeoTemplate]],
            parent: ElemTree.Element = None,
    ) -> Iterator[ElemTree.Element]:
        """Generate XML data based on the Mimeo Configuration.

        This function is used recursively when a Mimeo Configuration
        contains nested templates.
        It iterates through all templates configured and yields data
        units.

        Parameters
        ----------
        templates : Union[list, Iterator[MimeoTemplate]]
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
        mimeo_config: MimeoConfig
            A Mimeo Configuration providing output details

        Returns
        -------
        str
            Stringified data unit
        """
        if self.__indent is None or self.__indent == 0:
            node_str = ElemTree.tostring(data_unit,
                                         encoding="utf-8",
                                         method="xml",
                                         xml_declaration=self.__xml_declaration)
        else:
            xml_string = ElemTree.tostring(data_unit)
            xml_minidom = minidom.parseString(xml_string)

            if self.__xml_declaration is False:
                xml_minidom = xml_minidom.childNodes[0]
            node_str = xml_minidom.toprettyxml(indent=" " * self.__indent,
                                               encoding="utf-8")
        return node_str.decode("ascii")

    @classmethod
    @mimeo_context_switch
    @mimeo_clear_iterations
    def _process_single_template(
            cls,
            template: MimeoTemplate,
            parent: ElemTree.Element = None,
    ) -> List[ElemTree.Element]:
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
        List[ElemTree.Element]
            A list of generated data units
        """
        logger.debug("Reading template [{tmplt}]", extra={"tmplt": template})
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
        return cls._process_node(parent,
                                 template.model.root_name,
                                 template.model.root_data)

    @classmethod
    @mimeo_context
    def _process_node(
            cls,
            parent: ElemTree.Element,
            element_tag: str,
            element_value: Union[dict, list, str, int, float, bool],
            attributes: dict = None,
            context: MimeoContext = None,
    ) -> Optional[ElemTree.Element]:
        """Process a single template's node.

        This is a recursive function that traverses Mimeo Template
        and generates XML nodes based on `element_value` type.

        Parameters
        ----------
        parent : ElemTree.Element
            A parent node
        element_tag : str
            An element tag
        element_value : Union[dict, list, str, int, float, bool]
            An element value
        attributes : dict, default None
            Element's attributes
        context : MimeoContext, default None
            The current Mimeo Context (injected by MimeoContextManager)

        Returns
        -------
        ElemTree.Element
            Returned only when `parent` is None. A single data unit
            generated within a single template iteration.

        Raises
        ------
        InvalidSpecialFieldValueError
            If the special field value is dict or list
        SpecialFieldNotFoundError
            If the special field does not exist.
        """
        logger.fine("Rendering element - "
                    "parent [{parent}], element_tag [{tag}], "
                    "element_value [{val}], attributes [{attrs}]",
                    extra={
                        "parent": parent if parent is None else parent.tag,
                        "tag": element_tag,
                        "val": element_value,
                        "attrs": attributes,
                    })
        attributes = attributes if attributes is not None else {}
        if element_tag == MimeoConfig.TEMPLATES_KEY:
            templates = (MimeoTemplate(template) for template in element_value)
            for _ in cls.generate(templates, parent):
                pass
        else:
            is_special_field = MimeoRenderer.is_special_field(element_tag)
            if is_special_field:
                element_tag = MimeoRenderer.get_special_field_name(element_tag)

            element = cls._create_xml_element(parent, element_tag, attributes)

            if (isinstance(element_value, dict) and
                    not MimeoRenderer.is_parametrized_mimeo_util(element_value)):
                if MimeoConfig.MODEL_ATTRIBUTES_KEY in element_value:
                    element_value = dict(element_value)
                    attrs = element_value.pop(MimeoConfig.MODEL_ATTRIBUTES_KEY)
                    value = element_value.get(MimeoConfig.MODEL_VALUE_KEY,
                                              element_value)
                    if parent is not None:
                        parent.remove(element)
                        cls._process_node(parent, element_tag, value, attrs)
                    else:
                        return cls._process_node(parent, element_tag, value, attrs)
                else:
                    for child_tag, child_value in element_value.items():
                        cls._process_node(element, child_tag, child_value)
            elif isinstance(element_value, list):
                has_only_atomic_values = all(not isinstance(child, (list, dict))
                                             for child in element_value)
                if has_only_atomic_values:
                    parent.remove(element)
                    for child in element_value:
                        cls._process_node(parent, element_tag, child)
                else:
                    for child in element_value:
                        grand_child_tag = next(iter(child))
                        grand_child_data = child[grand_child_tag]
                        cls._process_node(element, grand_child_tag, grand_child_data)
            else:
                value = MimeoRenderer.render(element_value)
                if is_special_field:
                    context.curr_iteration().add_special_field(element_tag, value)

                val_str = str(value) if value is not None else ""
                element.text = val_str.lower() if isinstance(value, bool) else val_str
                logger.fine("Rendered value [{txt}]", extra={"txt": element.text})

            if parent is None:
                return element
        return None

    @classmethod
    def _create_xml_element(
            cls,
            parent: ElemTree.Element,
            element_tag: str,
            attributes: dict,
    ) -> Union[ElemTree.Element, ElemTree.SubElement]:
        """Create an XML element based on the `parent` existence.

        Parameters
        ----------
        parent : ElemTree.Element
            A parent node
        element_tag : str
            An element tag
        attributes : dict
            Element's attributes

        Returns
        -------
        Union[ElemTree.Element, ElemTree.SubElement]
            If the `parent` is None, returns ElemTree.Element.
            Otherwise, returns ElemTree.SubElement
        """
        if parent is None:
            return ElemTree.Element(element_tag, attrib=attributes)
        return ElemTree.SubElement(parent, element_tag, attrib=attributes)
