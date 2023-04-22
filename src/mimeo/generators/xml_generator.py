import logging
import xml.etree.ElementTree as ElemTree
from typing import Iterator, List, Union
from xml.dom import minidom

from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate
from mimeo.context import MimeoContext
from mimeo.context.annotations import (mimeo_clear_iterations, mimeo_context,
                                       mimeo_context_switch,
                                       mimeo_next_iteration)
from mimeo.generators import Generator
from mimeo.utils import MimeoRenderer

logger = logging.getLogger(__name__)


class XMLGenerator(Generator):

    def __init__(self, mimeo_config: MimeoConfig):
        super().__init__()
        self.__indent = mimeo_config.indent
        self.__xml_declaration = mimeo_config.xml_declaration

    @classmethod
    def generate(cls, templates: Union[list, Iterator[MimeoTemplate]], parent: ElemTree.Element = None) -> Iterator[ElemTree.Element]:
        for template in templates:
            for copy in cls._process_single_template(template, parent):
                yield copy

    def stringify(self, root, mimeo_config):
        if self.__indent is None or self.__indent == 0:
            return ElemTree.tostring(root,
                                     encoding="utf-8",
                                     method="xml",
                                     xml_declaration=self.__xml_declaration).decode('ascii')
        else:
            xml_string = ElemTree.tostring(root)
            xml_minidom = minidom.parseString(xml_string)
            if self.__xml_declaration:
                return xml_minidom.toprettyxml(indent=" " * self.__indent, encoding="utf-8").decode('ascii')
            else:
                return xml_minidom.childNodes[0].toprettyxml(indent=" " * self.__indent, encoding="utf-8").decode('ascii')

    @classmethod
    @mimeo_context_switch
    @mimeo_clear_iterations
    def _process_single_template(cls, template: MimeoTemplate, parent: ElemTree.Element = None) -> List[ElemTree.Element]:
        logger.debug(f"Reading template [{template}]")
        copies = [cls._process_single_copy(template, parent) for _ in iter(range(template.count))]
        return copies

    @classmethod
    @mimeo_next_iteration
    def _process_single_copy(cls, template: MimeoTemplate, parent: ElemTree.Element = None):
        return cls._process_node(parent, template.model.root_name, template.model.root_data)

    @classmethod
    @mimeo_context
    def _process_node(cls, parent, element_tag, element_value, attributes: dict = None, context: MimeoContext = None):
        logger.fine(f"Rendering element - "
                    f"parent [{parent if parent is None else parent.tag}], "
                    f"element_tag [{element_tag}], "
                    f"element_value [{element_value}], "
                    f"attributes [{attributes}]")
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

            if isinstance(element_value, dict) and not MimeoRenderer.is_parametrized_mimeo_util(element_value):
                if MimeoConfig.MODEL_ATTRIBUTES_KEY in element_value:
                    element_value_copy = dict(element_value)
                    attrs = element_value_copy.pop(MimeoConfig.MODEL_ATTRIBUTES_KEY)
                    value = element_value_copy.get(MimeoConfig.MODEL_VALUE_KEY, element_value_copy)
                    if parent is not None:
                        parent.remove(element)
                        cls._process_node(parent, element_tag, value, attrs)
                    else:
                        return cls._process_node(parent, element_tag, value, attrs)
                else:
                    for child_tag, child_value in element_value.items():
                        cls._process_node(element, child_tag, child_value)
            elif isinstance(element_value, list):
                has_only_atomic_values = all(not isinstance(child, (list, dict)) for child in element_value)
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

                value_str = str(value) if value is not None else ""
                element.text = value_str.lower() if isinstance(value, bool) else value_str
                logger.fine(f"Rendered value [{element.text}]")

            if parent is None:
                return element

    @classmethod
    def _create_xml_element(cls, parent, element_tag, attributes):
        if parent is None:
            return ElemTree.Element(element_tag, attrib=attributes)
        else:
            return ElemTree.SubElement(parent, element_tag, attrib=attributes)
