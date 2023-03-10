import json
import string
import xml.etree.ElementTree as ElemTree
from xml.dom import minidom
import re
import random

curr_id = 0


def auto_increment(pattern="{:05d}"):
    global curr_id
    curr_id += 1
    return pattern.format(curr_id)


def random_str(length=20):
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def random_int(length=1):
    return "".join(random.choice(string.digits) for i in range(length))


def generate_from_templates(parent, templates, xml_declaration = False):
    global curr_id
    for template in templates:
        # attributes = template["attributes"] if "attributes" in template else {}

        count = template["count"]
        model = template["model"]

        attributes = model.get_for_context("attributes", {})
        xmls = []
        for _ in iter(range(count)):
            root_name = next(filter(lambda key: key != "attributes", iter(model)))
            data = model[root_name]
            root = to_xml(parent, root_name, data, attributes)

            if parent is None:
                print(to_xml_string(ElemTree.ElementTree(root), indent, xml_declaration))
            xmls.append(root)
        curr_id = 0
        return xmls


def to_xml(parent, element_tag, element_value, attributes={}):
    if element_tag == "_templates_":
        generate_from_templates(parent, element_value)
    else:
        element = ElemTree.Element(element_tag, attrib=attributes) if parent is None else ElemTree.SubElement(parent, element_tag, attrib=attributes)
        if isinstance(element_value, dict):
            for child_tag, child_value in element_value.items():
                to_xml(element, child_tag, child_value)
        elif isinstance(element_value, list):
            for child in element_value:
                grand_child_tag = next(iter(child))
                grand_child_data = child[grand_child_tag]
                to_xml(element, grand_child_tag, grand_child_data)
        else:
            element.text = get_value(element_value)

        return element


def to_xml_string(document_node, indent: int = None, declaration: bool = True) -> str:
    xml = document_node.getroot()
    if indent is None:
        return ElemTree.tostring(xml,
                                 encoding="utf-8",
                                 method="xml",
                                 xml_declaration=declaration).decode('ascii')
    else:
        xml_string = ElemTree.tostring(xml)
        xml_minidom = minidom.parseString(xml_string)
        if declaration:
            return xml_minidom.toprettyxml(indent=" " * indent, encoding="utf-8").decode('ascii')
        else:
            return xml_minidom.childNodes[0].toprettyxml(indent=" " * indent, encoding="utf-8").decode('ascii')


def get_value(literal_value):
    literal_value_str = str(literal_value)
    pattern = re.compile("^\{(.*)\}$")
    if pattern.match(literal_value_str):
        match = next(pattern.finditer(literal_value))
        return eval(match.group(1))
    else:
        return literal_value_str if not isinstance(literal_value, bool) else literal_value_str.lower()


# Opening JSON file
with open('config-3.json') as config:
    data = json.load(config)

xml_declaration = data.get_for_context("xml_declaration", False)
if data["output_format"].lower() == "xml":

    templates = data["_templates_"]
    indent = data["indent"]

    xmls = generate_from_templates(None, templates, xml_declaration)

    # for xml in xmls:
    #     print(to_xml_string(ElemTree.ElementTree(xml), indent, xml_declaration))
else:
    print("Provided format is not supported!")

