import logging
import xml.etree.ElementTree as ElemTree
from typing import Iterator, List, Union
from xml.dom import minidom

from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate
from mimeo.context.annotations import (mimeo_clear_iterations,
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

    def generate(self, templates: Union[list, Iterator[MimeoTemplate]], parent: ElemTree.Element = None) -> Iterator[ElemTree.Element]:
        for template in templates:
            for copy in self.__process_single_template(template, parent):
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

    @mimeo_context_switch
    @mimeo_clear_iterations
    def __process_single_template(self, template: MimeoTemplate, parent: ElemTree.Element = None) -> List[ElemTree.Element]:
        logger.debug(f"Reading template [{template}]")
        copies = [self.__process_single_copy(template, parent) for _ in iter(range(template.count))]
        return copies

    @mimeo_next_iteration
    def __process_single_copy(self, template: MimeoTemplate, parent: ElemTree.Element = None):
        return self.__to_xml(parent, template.model.root_name, template.model.root_data)

    def __to_xml(self, parent, element_tag, element_value, attributes: dict = None):
        logger.fine(f"Rendering element - "
                    f"parent [{parent if parent is None else parent.tag}], "
                    f"element_tag [{element_tag}], "
                    f"element_value [{element_value}], "
                    f"attributes [{attributes}]")
        attributes = attributes if attributes is not None else {}
        if element_tag == MimeoConfig.TEMPLATES_KEY:
            templates = (MimeoTemplate(template) for template in element_value)
            for _ in self.generate(templates, parent):
                pass
        else:
            is_special_field = MimeoRenderer.is_special_field(element_tag)
            if is_special_field:
                element_tag = MimeoRenderer.get_special_field_name(element_tag)

            element = ElemTree.Element(element_tag, attrib=attributes) if parent is None else ElemTree.SubElement(
                parent, element_tag, attrib=attributes)
            if isinstance(element_value, dict) and MimeoConfig.MODEL_MIMEO_UTIL_KEY not in element_value:
                if MimeoConfig.MODEL_ATTRIBUTES_KEY in element_value:
                    element_value_copy = dict(element_value)
                    attrs = element_value_copy.pop(MimeoConfig.MODEL_ATTRIBUTES_KEY)
                    value = element_value_copy.get(MimeoConfig.MODEL_VALUE_KEY, element_value_copy)
                    if parent is not None:
                        parent.remove(element)
                        self.__to_xml(parent, element_tag, value, attrs)
                    else:
                        return self.__to_xml(parent, element_tag, value, attrs)
                else:
                    for child_tag, child_value in element_value.items():
                        self.__to_xml(element, child_tag, child_value)
            elif isinstance(element_value, list):
                has_only_atomic_values = all(not isinstance(child, (list, dict)) for child in element_value)
                if has_only_atomic_values:
                    parent.remove(element)
                    for child in element_value:
                        self.__to_xml(parent, element_tag, child)
                else:
                    for child in element_value:
                        grand_child_tag = next(iter(child))
                        grand_child_data = child[grand_child_tag]
                        self.__to_xml(element, grand_child_tag, grand_child_data)
            else:
                value = MimeoRenderer.render(element_value)
                if is_special_field:
                    self._mimeo_manager.get_current_context().curr_iteration().add_special_field(element_tag,
                                                                                                 value)

                value_str = str(value)
                element.text = value_str.lower() if isinstance(value, bool) else value_str
                logger.fine(f"Rendered value [{element.text}]")

            if parent is None:
                return element
