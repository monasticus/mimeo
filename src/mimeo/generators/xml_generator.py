import xml.etree.ElementTree as ElemTree
from typing import Iterator, Union
from xml.dom import minidom

from mimeo.generators import Generator, GeneratorUtils
from mimeo.model.mimeo_config import MimeoConfig, MimeoTemplate


class XMLGenerator(Generator):

    def __init__(self, mimeo_config: MimeoConfig):
        self.indent = mimeo_config.indent
        self.xml_declaration = mimeo_config.xml_declaration
        self.current_template = None

    def generate(self, templates: Union[list, Iterator[MimeoTemplate]], parent: ElemTree.Element = None):
        for template in templates:
            self.current_template = template
            GeneratorUtils.get_for_context(template.model.root_name).reset()
            for _ in iter(range(template.count)):
                yield self.__to_xml(parent,
                                    template.model.root_name,
                                    template.model.root_data,
                                    template.model.attributes)

    def stringify(self, root, mimeo_config):
        if self.indent is None:
            return ElemTree.tostring(root,
                                     encoding="utf-8",
                                     method="xml",
                                     xml_declaration=self.xml_declaration).decode('ascii')
        else:
            xml_string = ElemTree.tostring(root)
            xml_minidom = minidom.parseString(xml_string)
            if self.xml_declaration:
                return xml_minidom.toprettyxml(indent=" " * self.indent, encoding="utf-8").decode('ascii')
            else:
                return xml_minidom.childNodes[0].toprettyxml(indent=" " * self.indent, encoding="utf-8").decode('ascii')

    def __to_xml(self, parent, element_tag, element_value, attributes: dict = None):
        attributes = attributes if attributes is not None else {}
        if element_tag == MimeoConfig.TEMPLATES_KEY:
            templates = (MimeoTemplate(**template) for template in element_value)
            curr_template = self.current_template
            for _ in self.generate(templates, parent):
                pass
            self.current_template = curr_template
        else:
            element = ElemTree.Element(element_tag, attrib=attributes) if parent is None else ElemTree.SubElement(parent, element_tag, attrib=attributes)
            if isinstance(element_value, dict):
                for child_tag, child_value in element_value.items():
                    self.__to_xml(element, child_tag, child_value)
            elif isinstance(element_value, list):
                for child in element_value:
                    grand_child_tag = next(iter(child))
                    grand_child_data = child[grand_child_tag]
                    self.__to_xml(element, grand_child_tag, grand_child_data)
            else:
                element.text = XMLGenerator._get_value(element_value, self.current_template)

            if parent is None:
                return element
