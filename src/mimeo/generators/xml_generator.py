import xml.etree.ElementTree as ElemTree
from typing import Iterator, Union
from xml.dom import minidom

from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate
from mimeo.generators import Generator, GeneratorUtils


class XMLGenerator(Generator):

    def __init__(self, mimeo_config: MimeoConfig):
        super().__init__(mimeo_config)
        self.__indent = mimeo_config.indent
        self.__xml_declaration = mimeo_config.xml_declaration
        self.__current_template = None

    def generate(self, templates: Union[list, Iterator[MimeoTemplate]], parent: ElemTree.Element = None) -> Iterator[ElemTree.Element]:
        for template in templates:
            self.__current_template = template
            utils = GeneratorUtils.get_for_context(template.model.root_name)
            utils.reset()
            for i in iter(range(template.count)):
                utils.setup_iteration(i + 1)
                yield self.__to_xml(parent,
                                    template.model.root_name,
                                    template.model.root_data,
                                    template.model.attributes)

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

    def __to_xml(self, parent, element_tag, element_value, attributes: dict = None):
        attributes = attributes if attributes is not None else {}
        if element_tag == MimeoConfig.TEMPLATES_KEY:
            templates = (MimeoTemplate(template) for template in element_value)
            curr_template = self.__current_template
            for _ in self.generate(templates, parent):
                pass
            self.__current_template = curr_template
        else:
            is_special_field = GeneratorUtils.is_special_field(element_tag)
            if is_special_field:
                special_field = element_tag
                element_tag = GeneratorUtils.get_special_field_name(element_tag)

            element = ElemTree.Element(element_tag, attrib=attributes) if parent is None else ElemTree.SubElement(
                parent, element_tag, attrib=attributes)
            if isinstance(element_value, dict):
                for child_tag, child_value in element_value.items():
                    self.__to_xml(element, child_tag, child_value)
            elif isinstance(element_value, list):
                for child in element_value:
                    grand_child_tag = next(iter(child))
                    grand_child_data = child[grand_child_tag]
                    self.__to_xml(element, grand_child_tag, grand_child_data)
            else:
                element.text = GeneratorUtils.render_value(self.__current_template.model.root_name, element_value)
                if is_special_field:
                    utils = GeneratorUtils.get_for_context(self.__current_template.model.root_name)
                    utils.provide(special_field, element.text)

            if parent is None:
                return element
