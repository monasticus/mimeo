from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.generators import XMLGenerator
from mimeo.generators.exc import UnsupportedStructureError
from mimeo.utils.exc import InvalidValueError
from tests.utils import assert_throws


def test_generate_single_template_model_without_attributes():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {},
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_model_with_attributes():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "_attrs": {
                            "xmlns": "http://mimeo.arch.com/default-namespace",
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {"xmlns": "http://mimeo.arch.com/default-namespace"}
            assert len(list(data)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_model_with_prefixed_ns():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "pn:SomeEntity": {
                        "_attrs": {
                            "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "pn:SomeEntity"
            assert data.attrib == {"xmlns:pn": "http://mimeo.arch.com/prefixed-namespace"}
            assert len(list(data)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_model_with_attributes_in_atomic_child():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "pn:ChildNode": {
                            "_attrs": {
                                "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            },
                            "_value": "string-value",
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("pn:ChildNode")
            assert child.tag == "pn:ChildNode"
            assert child.attrib == {"xmlns:pn": "http://mimeo.arch.com/prefixed-namespace"}
            assert child.text == "string-value"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_model_with_attributes_in_complex_child():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "pn:ChildNode": {
                            "_attrs": {
                                "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            },
                            "pn:GrandChild": "string-value",
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("pn:ChildNode")
            assert child.tag == "pn:ChildNode"
            assert child.attrib == {"xmlns:pn": "http://mimeo.arch.com/prefixed-namespace"}
            assert len(list(child)) == 1  # number of children

            grand_child = child.find("pn:GrandChild")
            assert grand_child.tag == "pn:GrandChild"
            assert grand_child.attrib == {}
            assert grand_child.text == "string-value"
            assert len(list(grand_child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_model_with_attributes_in_child_mixed():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": {
                            "_attrs": {
                                "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            },
                            "_value": "string-value",
                            "GrandChild": "string-value",  # will be ignored
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {"xmlns:pn": "http://mimeo.arch.com/prefixed-namespace"}
            assert child.text == "string-value"
            assert len(list(child)) == 0  # number of children

            count += 1


def test_generate_single_template_str_value():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == "value"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_int_value():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": 1,
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == "1"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_bool_value():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": True,
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == "true"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_none_value():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": None,
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == ""
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_using_variables():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "vars": {
            "CUSTOM_VAR_1": "custom-value-1",
            "CUSTOM_VAR_2": 1,
            "CUSTOM_VAR_3": True,
            "CUSTOM_VAR_4": "{CUSTOM_VAR_2}",
            "CUSTOM_VAR_5": "{curr_iter}",
            "CUSTOM_VAR_6": {
                "_mimeo_util": {
                    "_name": "auto_increment",
                    "pattern": "{}",
                },
            },
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": "{CUSTOM_VAR_1}",
                        "ChildNode2": "{CUSTOM_VAR_2}",
                        "ChildNode3": "{CUSTOM_VAR_3}",
                        "ChildNode4": "{CUSTOM_VAR_4}",
                        "ChildNode5": "{CUSTOM_VAR_5}",
                        "ChildNode6": "{CUSTOM_VAR_6}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 6  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert child.text == "custom-value-1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode2")
            assert child.tag == "ChildNode2"
            assert child.attrib == {}
            assert child.text == "1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode3")
            assert child.tag == "ChildNode3"
            assert child.attrib == {}
            assert child.text == "true"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode4")
            assert child.tag == "ChildNode4"
            assert child.attrib == {}
            assert child.text == "1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode5")
            assert child.tag == "ChildNode5"
            assert child.attrib == {}
            assert child.text == str(index+1)
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode6")
            assert child.tag == "ChildNode6"
            assert child.attrib == {}
            assert child.text == str(index+1)
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_child_elements():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": {
                            "GrandChildNode": "value",
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert len(list(child)) == 1  # number of children

            grand_child = child.find("GrandChildNode")
            assert grand_child.tag == "GrandChildNode"
            assert grand_child.attrib == {}
            assert grand_child.text == "value"
            assert len(list(grand_child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_complex_child_elements_in_array():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNodes": [
                            {
                                "ChildNode": "value-1",
                            },
                            {
                                "ChildNode": "value-2",
                            },
                        ],
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child_nodes_node = data.find("ChildNodes")
            assert child_nodes_node.tag == "ChildNodes"
            assert child_nodes_node.attrib == {}
            assert len(list(child_nodes_node)) == 2  # number of children

            child_nodes = child_nodes_node.findall("ChildNode")

            child_node1 = child_nodes[0]
            assert child_node1.tag == "ChildNode"
            assert child_node1.attrib == {}
            assert child_node1.text == "value-1"
            assert len(list(child_node1)) == 0  # number of children
            child_node2 = child_nodes[1]
            assert child_node2.tag == "ChildNode"
            assert child_node2.attrib == {}
            assert child_node2.text == "value-2"
            assert len(list(child_node2)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_only_atomic_child_elements_in_array():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": [
                            "value-1",
                            1,
                            True,
                        ],
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 3  # number of children

            child_nodes = data.findall("ChildNode")

            child_node1 = child_nodes[0]
            assert child_node1.tag == "ChildNode"
            assert child_node1.attrib == {}
            assert child_node1.text == "value-1"
            assert len(list(child_node1)) == 0  # number of children
            child_node2 = child_nodes[1]
            assert child_node2.tag == "ChildNode"
            assert child_node2.attrib == {}
            assert child_node2.text == "1"
            assert len(list(child_node2)) == 0  # number of children
            child_node3 = child_nodes[2]
            assert child_node3.tag == "ChildNode"
            assert child_node3.attrib == {}
            assert child_node3.text == "true"
            assert len(list(child_node3)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_single_template_only_atomic_child_elements_with_mimeo_util_in_array():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": [
                            "value-1",
                            {
                                "_mimeo_util": {
                                    "_name": "auto_increment",
                                    "pattern": "{}",
                                },
                            },
                        ],
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            child_nodes = data.findall("ChildNode")

            child_node1 = child_nodes[0]
            assert child_node1.tag == "ChildNode"
            assert child_node1.attrib == {}
            assert child_node1.text == "value-1"
            assert len(list(child_node1)) == 0  # number of children
            child_node2 = child_nodes[1]
            assert child_node2.tag == "ChildNode"
            assert child_node2.attrib == {}
            assert child_node2.text == str(count + 1)
            assert len(list(child_node2)) == 0  # number of children

            count += 1

        assert count == 5


@assert_throws(err_type=UnsupportedStructureError,
               msg="An array can include only atomic types (including Mimeo Utils) or "
                   "only JSON objects! Unsupported structure found in {e}: {s}",
               params={"e": "ChildNode", "s": "[['atomic']]"})
def test_generate_single_template_list_child_element_in_array():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": [
                            [
                                "atomic",
                            ],
                        ],
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        for _ in generator.generate(config.templates):
            pass


@assert_throws(err_type=UnsupportedStructureError,
               msg="An array can include only atomic types (including Mimeo Utils) or "
                   "only JSON objects! Unsupported structure found in {e}: {s}",
               params={"e": "ChildNodes", "s": "['atomic', {'ChildNode': 'value-1'}]"})
def test_generate_single_template_mixed_child_elements_in_array():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNodes": [
                            "atomic",
                            {
                                "ChildNode": "value-1",
                            },
                        ],
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        for _ in generator.generate(config.templates):
            pass


@assert_throws(err_type=UnsupportedStructureError,
               msg="An array can include only atomic types (including Mimeo Utils) or "
                   "only JSON objects! Unsupported structure found in {e}: {s}",
               params={"e": "ChildNodes",
                       "s": "[{'_mimeo_util': {'_name': 'auto_increment', "
                            "'pattern': '{}'}}, {'ChildNode': 'value-1'}]"})
def test_generate_single_template_complex_child_elements_with_mimeo_util_in_array():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNodes": [
                            {
                                "_mimeo_util": {
                                    "_name": "auto_increment",
                                    "pattern": "{}",
                                },
                            },
                            {
                                "ChildNode": "value-1",
                            },
                        ],
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        for _ in generator.generate(config.templates):
            pass


def test_generate_multiple_templates():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {},
                },
            },
            {
                "count": 3,
                "model": {
                    "SomeEntity2": {},
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        roots = list(generator.generate(config.templates))
        template_1_roots = roots[:2]
        template_2_roots = roots[2:]

        assert len(roots) == 5
        assert len(template_1_roots) == 2
        assert len(template_2_roots) == 3

        for data in template_1_roots:
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 0  # number of children

        for data in template_2_roots:
            assert data.tag == "SomeEntity2"
            assert data.attrib == {}
            assert len(list(data)) == 0  # number of children


def test_generate_nested_templates():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "SingleNode": "value",
                        "MultipleNodes": {
                            "_templates_": [
                                {
                                    "count": 4,
                                    "model": {
                                        "Node": {
                                            "ChildNode": True,
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for data in generator.generate(config.templates):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            single_node = data.find("SingleNode")
            assert single_node.tag == "SingleNode"
            assert single_node.attrib == {}
            assert single_node.text == "value"
            assert len(list(single_node)) == 0  # number of children

            multiples_nodes_node = data.find("MultipleNodes")
            assert multiples_nodes_node.tag == "MultipleNodes"
            assert multiples_nodes_node.attrib == {}
            assert len(list(multiples_nodes_node)) == 4  # number of children

            nodes = multiples_nodes_node.findall("Node")
            for node in nodes:
                assert node.tag == "Node"
                assert node.attrib == {}
                assert len(list(node)) == 1  # number of children

                child_node = node.find("ChildNode")
                assert child_node.tag == "ChildNode"
                assert child_node.attrib == {}
                assert child_node.text == "true"
                assert len(list(child_node)) == 0  # number of children

            count += 1

        assert count == 5


def test_stringify_with_indent_and_xml_declaration():
    config = MimeoConfig({
        "output": {
            "format": "xml",
            "xml_declaration": True,
            "indent": 4,
        },
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "SomeEntity": {
                        "_attrs": {
                            "xmlns": "http://mimeo.arch.com/default-namespace",
                            "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        },
                        "pn:ChildNode": "value",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        for data in generator.generate(config.templates):
            data_str = generator.stringify(data)
            assert data_str == ('<?xml version="1.0" encoding="utf-8"?>\n'
                                '<SomeEntity'
                                ' xmlns="http://mimeo.arch.com/default-namespace"'
                                ' xmlns:pn="http://mimeo.arch.com/prefixed-namespace">\n'
                                '    <pn:ChildNode>value</pn:ChildNode>\n'
                                '</SomeEntity>\n')


def test_stringify_with_indent_and_without_xml_declaration():
    config = MimeoConfig({
        "output": {
            "format": "xml",
            "xml_declaration": False,
            "indent": 4,
        },
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "SomeEntity": {
                        "_attrs": {
                            "xmlns": "http://mimeo.arch.com/default-namespace",
                            "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        },
                        "pn:ChildNode": "value",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        for data in generator.generate(config.templates):
            data_str = generator.stringify(data)
            assert data_str == ('<SomeEntity'
                                ' xmlns="http://mimeo.arch.com/default-namespace"'
                                ' xmlns:pn="http://mimeo.arch.com/prefixed-namespace">\n'
                                '    <pn:ChildNode>value</pn:ChildNode>\n'
                                '</SomeEntity>\n')


def test_stringify_without_indent_and_with_xml_declaration():
    config = MimeoConfig({
        "output": {
            "format": "xml",
            "xml_declaration": True,
        },
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "SomeEntity": {
                        "_attrs": {
                            "xmlns": "http://mimeo.arch.com/default-namespace",
                            "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        },
                        "pn:ChildNode": "value",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        for data in generator.generate(config.templates):
            data_str = generator.stringify(data)
            # Notice no new line at the end of string chunks
            assert data_str == ("<?xml version='1.0' encoding='utf-8'?>\n"
                                '<SomeEntity'
                                ' xmlns="http://mimeo.arch.com/default-namespace"'
                                ' xmlns:pn="http://mimeo.arch.com/prefixed-namespace">'
                                '<pn:ChildNode>value</pn:ChildNode>'
                                '</SomeEntity>')


def test_stringify_without_indent_and_xml_declaration():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "SomeEntity": {
                        "_attrs": {
                            "xmlns": "http://mimeo.arch.com/default-namespace",
                            "xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        },
                        "pn:ChildNode": "value",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        for data in generator.generate(config.templates):
            data_str = generator.stringify(data)
            # Notice no new line at the end of string chunks
            assert data_str == ('<SomeEntity'
                                ' xmlns="http://mimeo.arch.com/default-namespace"'
                                ' xmlns:pn="http://mimeo.arch.com/prefixed-namespace">'
                                '<pn:ChildNode>value</pn:ChildNode>'
                                '</SomeEntity>')


def test_generate_using_mimeo_util_raw():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{auto_increment}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == f"{index + 1:05d}"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_mimeo_util_parametrized():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": {
                            "_mimeo_util": {
                                "_name": "auto_increment",
                                "pattern": "{}",
                            },
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == str(index + 1)
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


@assert_throws(err_type=InvalidValueError,
               msg="The auto_increment Mimeo Util require a string value "
                   "for the pattern parameter and was: [{pattern}].",
               params={"pattern": 1})
def test_generate_using_mimeo_util_parametrized_invalid():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": {
                            "_mimeo_util": {
                                "_name": "auto_increment",
                                "pattern": 1,
                            },
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        for _ in generator.generate(config.templates):
            pass


def test_generate_using_auto_increment():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{auto_increment}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == f"{index + 1:05d}"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_auto_increment_in_two_templates():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{auto_increment}",
                    },
                },
            },
            {
                "count": 3,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{auto_increment}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == f"{index + 1:05d}"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 8


def test_generate_using_auto_increment_in_two_templates_with_customized_context_name():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{auto_increment}",
                    },
                },
            },
            {
                "count": 3,
                "model": {
                    "context": "A different set",
                    "SomeEntity": {
                        "ChildNode": "{auto_increment}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            # from 6th item it is the second template
            expected_increment = index + 1 if index < 5 else index - 5 + 1
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == f"{expected_increment:05d}"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 8


def test_generate_using_curr_iter_util():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{curr_iter}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            curr_iter = index + 1
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == str(curr_iter)
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_curr_iter_util_in_two_templates():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{curr_iter}",
                    },
                },
            },
            {
                "count": 3,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{curr_iter}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            # from 6th item it is the second template
            curr_iter = index + 1 if index < 5 else index - 5 + 1
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode")
            assert child.tag == "ChildNode"
            assert child.attrib == {}
            assert child.text == str(curr_iter)
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 8


def test_generates_using_curr_iter_util_in_nested_templates():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "SingleNode": "{curr_iter}",
                        "MultipleNodes": {
                            "_templates_": [
                                {
                                    "count": 4,
                                    "model": {
                                        "Node": {
                                            "ChildNode": "{curr_iter}",
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            curr_iter = index + 1
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            single_node = data.find("SingleNode")
            assert single_node.tag == "SingleNode"
            assert single_node.attrib == {}
            assert single_node.text == str(curr_iter)
            assert len(list(single_node)) == 0  # number of children

            multiples_nodes_node = data.find("MultipleNodes")
            assert multiples_nodes_node.tag == "MultipleNodes"
            assert multiples_nodes_node.attrib == {}
            assert len(list(multiples_nodes_node)) == 4  # number of children

            nodes = multiples_nodes_node.findall("Node")
            for nested_index, node in enumerate(nodes):
                nested_curr_iter = nested_index + 1
                assert node.tag == "Node"
                assert node.attrib == {}
                assert len(list(node)) == 1  # number of children

                child_node = node.find("ChildNode")
                assert child_node.tag == "ChildNode"
                assert child_node.attrib == {}
                assert child_node.text == str(nested_curr_iter)
                assert len(list(child_node)) == 0  # number of children

            count += 1

        assert count == 5


def test_generates_using_curr_iter_util_in_nested_templates_indicating_one():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "SingleNode": "{curr_iter}",
                        "MultipleNodes": {
                            "_templates_": [
                                {
                                    "count": 4,
                                    "model": {
                                        "Node": {
                                            "ChildNode": {
                                                "_mimeo_util": {
                                                    "_name": "curr_iter",
                                                    "context": "SomeEntity",
                                                },
                                            },
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            curr_iter = index + 1
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            single_node = data.find("SingleNode")
            assert single_node.tag == "SingleNode"
            assert single_node.attrib == {}
            assert single_node.text == str(curr_iter)
            assert len(list(single_node)) == 0  # number of children

            multiples_nodes_node = data.find("MultipleNodes")
            assert multiples_nodes_node.tag == "MultipleNodes"
            assert multiples_nodes_node.attrib == {}
            assert len(list(multiples_nodes_node)) == 4  # number of children

            nodes = multiples_nodes_node.findall("Node")
            for _, node in enumerate(nodes):
                assert node.tag == "Node"
                assert node.attrib == {}
                assert len(list(node)) == 1  # number of children

                child_node = node.find("ChildNode")
                assert child_node.tag == "ChildNode"
                assert child_node.attrib == {}
                assert child_node.text == str(curr_iter)
                assert len(list(child_node)) == 0  # number of children

            count += 1

        assert count == 5


def test_generates_using_curr_iter_util_in_nested_templates_indicating_customized_one():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "ROOT",
                    "SomeEntity": {
                        "SingleNode": "{curr_iter}",
                        "MultipleNodes": {
                            "_templates_": [
                                {
                                    "count": 4,
                                    "model": {
                                        "Node": {
                                            "ChildNode": {
                                                "_mimeo_util": {
                                                    "_name": "curr_iter",
                                                    "context": "ROOT",
                                                },
                                            },
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            curr_iter = index + 1
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            single_node = data.find("SingleNode")
            assert single_node.tag == "SingleNode"
            assert single_node.attrib == {}
            assert single_node.text == str(curr_iter)
            assert len(list(single_node)) == 0  # number of children

            multiples_nodes_node = data.find("MultipleNodes")
            assert multiples_nodes_node.tag == "MultipleNodes"
            assert multiples_nodes_node.attrib == {}
            assert len(list(multiples_nodes_node)) == 4  # number of children

            nodes = multiples_nodes_node.findall("Node")
            for _, node in enumerate(nodes):
                assert node.tag == "Node"
                assert node.attrib == {}
                assert len(list(node)) == 1  # number of children

                child_node = node.find("ChildNode")
                assert child_node.tag == "ChildNode"
                assert child_node.attrib == {}
                assert child_node.text == str(curr_iter)
                assert len(list(child_node)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_curr_iter_and_auto_increment_utils():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": "{curr_iter}",
                        "ChildNode2": "{curr_iter}",
                        "ChildNode3": "{auto_increment}",
                        "ChildNode4": "{auto_increment}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            curr_iter = index + 1
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 4  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert child.text == str(curr_iter)  # 1, 2, 3, 4, 5
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode2")
            assert child.tag == "ChildNode2"
            assert child.attrib == {}
            assert child.text == str(curr_iter)  # 1, 2, 3, 4, 5
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode3")
            assert child.tag == "ChildNode3"
            assert child.attrib == {}
            assert child.text == "{:05d}".format(curr_iter * 2 - 1)  # 1, 3, 5, 7, 9
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode4")
            assert child.tag == "ChildNode4"
            assert child.attrib == {}
            assert child.text == "{:05d}".format(curr_iter * 2)  # 2, 4, 6, 8, 10
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_key_util():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": "{key}",
                        "ChildNode2": "{key}",
                        "ChildNode3": "{key}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        keys = []
        for _index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 3  # number of children

            child = data.find("ChildNode1")
            key1 = child.text
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode2")
            key2 = child.text
            assert child.tag == "ChildNode2"
            assert child.attrib == {}
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode3")
            key3 = child.text
            assert child.tag == "ChildNode3"
            assert child.attrib == {}
            assert len(list(child)) == 0  # number of children

            assert key1 == key2
            assert key2 == key3
            keys.append(key1)

            count += 1

        assert count == 5
        assert len(set(keys)) == len(keys)


def test_generate_using_key_util_in_separated_contexts():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": "{key}",
                        "_templates_": [
                            {
                                "count": 1,
                                "model": {
                                    "NewContextNode": {
                                        "GrandChild": "{key}",
                                    },
                                },
                            },
                        ],
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for _index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            child = data.find("ChildNode1")
            key1 = child.text
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert len(list(child)) == 0  # number of children

            new_context_node = data.find("NewContextNode")
            assert new_context_node.tag == "NewContextNode"
            assert new_context_node.attrib == {}
            assert len(list(new_context_node)) == 1  # number of children

            grand_child = new_context_node.find("GrandChild")
            key2 = grand_child.text
            assert grand_child.tag == "GrandChild"
            assert grand_child.attrib == {}
            assert len(list(grand_child)) == 0  # number of children

            assert key1 != key2

            count += 1

        assert count == 5


def test_generate_using_key_util_in_separated_contexts_indicating_one():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": "{key}",
                        "_templates_": [
                            {
                                "count": 1,
                                "model": {
                                    "NewContextNode": {
                                        "GrandChild": {
                                            "_mimeo_util": {
                                                "_name": "key",
                                                "context": "SomeEntity",
                                            },
                                        },
                                    },
                                },
                            },
                        ],
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for _index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            child = data.find("ChildNode1")
            key1 = child.text
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert len(list(child)) == 0  # number of children

            new_context_node = data.find("NewContextNode")
            assert new_context_node.tag == "NewContextNode"
            assert new_context_node.attrib == {}
            assert len(list(new_context_node)) == 1  # number of children

            grand_child = new_context_node.find("GrandChild")
            key2 = grand_child.text
            assert grand_child.tag == "GrandChild"
            assert grand_child.attrib == {}
            assert len(list(grand_child)) == 0  # number of children

            assert key1 == key2

            count += 1

        assert count == 5


def test_generate_using_key_util_in_two_templates_with_customized_iteration():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "CustomIteration1": {
                        "ChildNode1": "{key}",
                    },
                },
            },
            {
                "count": 5,
                "model": {
                    "CustomIteration2": {
                        "ChildNode1": {
                            "_mimeo_util": {
                                "_name": "key",
                                "context": "CustomIteration1",
                                "iteration": "{curr_iter}",
                            },
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        data = list(generator.generate(config.templates))
        some_entity_data = data[:5]
        some_other_entity_data = data[5:]

        assert len(data) == 10
        assert len(some_entity_data) == 5
        assert len(some_other_entity_data) == 5

        some_entity_keys = []
        some_other_entity_keys = []
        for data in some_entity_data:
            assert data.tag == "CustomIteration1"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert len(list(child)) == 0  # number of children
            some_entity_keys.append(child.text)

        for data in some_other_entity_data:
            assert data.tag == "CustomIteration2"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert len(list(child)) == 0  # number of children
            some_other_entity_keys.append(child.text)

        for i in range(5):
            assert some_entity_keys[i] == some_other_entity_keys[i]


def test_generate_using_get_key_util_in_two_templates_with_customized_context_name():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "context": "First SomeEntity set",
                    "SomeEntity": {
                        "ChildNode1": "{key}",
                    },
                },
            },
            {
                "count": 5,
                "model": {
                    "context": "Second SomeEntity set",
                    "SomeEntity": {
                        "ChildNode1": {
                            "_mimeo_util": {
                                "_name": "key",
                                "context": "First SomeEntity set",
                            },
                        },
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        data = list(generator.generate(config.templates))
        some_entity_data = data[:5]
        some_other_entity_data = data[5:]

        assert len(data) == 10
        assert len(some_entity_data) == 5
        assert len(some_other_entity_data) == 5

        first_set_keys = []
        for data in some_entity_data:
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert len(list(child)) == 0  # number of children
            first_set_keys.append(child.text)

        for data in some_other_entity_data:
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 1  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert child.text == first_set_keys[-1]  # the last child from first set
            assert len(list(child)) == 0  # number of children


def test_generate_using_special_fields():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "{:ChildNode1:}": "value-1",
                        "ChildNode2": "{:ChildNode1:}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for _index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert child.text == "value-1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode2")
            assert child.tag == "ChildNode2"
            assert child.attrib == {}
            assert child.text == "value-1"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_special_fields_as_partial_values():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "{:ChildNode1:}": "value-1",
                        "{:ChildNode2:}": "value-2",
                        "ChildNode3": "{:ChildNode1:}-2",
                        "ChildNode4": "3-{:ChildNode1:}-3",
                        "ChildNode5": "4-{:ChildNode1:}",
                        "ChildNode6": "{:ChildNode1:}-{:ChildNode1:}",
                        "ChildNode7": "{:ChildNode1:}-{:ChildNode2:}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for _index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 7  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert child.text == "value-1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode2")
            assert child.tag == "ChildNode2"
            assert child.attrib == {}
            assert child.text == "value-2"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode3")
            assert child.tag == "ChildNode3"
            assert child.attrib == {}
            assert child.text == "value-1-2"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode4")
            assert child.tag == "ChildNode4"
            assert child.attrib == {}
            assert child.text == "3-value-1-3"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode5")
            assert child.tag == "ChildNode5"
            assert child.attrib == {}
            assert child.text == "4-value-1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode6")
            assert child.tag == "ChildNode6"
            assert child.attrib == {}
            assert child.text == "value-1-value-1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode7")
            assert child.tag == "ChildNode7"
            assert child.attrib == {}
            assert child.text == "value-1-value-2"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_special_fields_using_namespace():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "ns:SomeEntity": {
                        "_attrs": {
                            "xmlns:ns": "http://mimeo.arch.com/prefixed-namespace",
                        },
                        "{:ns:ChildNode1:}": "value-1",
                        "ns:ChildNode2": "{:ns:ChildNode1:}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for _index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "ns:SomeEntity"
            assert data.attrib == {
                "xmlns:ns": "http://mimeo.arch.com/prefixed-namespace",
            }
            assert len(list(data)) == 2  # number of children

            child = data.find("ns:ChildNode1")
            assert child.tag == "ns:ChildNode1"
            assert child.attrib == {}
            assert child.text == "value-1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ns:ChildNode2")
            assert child.tag == "ns:ChildNode2"
            assert child.attrib == {}
            assert child.text == "value-1"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_special_fields_recursive():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "{:ChildNode1:}": "value-1",
                        "{:ChildNode2:}": "{:ChildNode1:}",
                        "ChildNode3": "{:ChildNode2:}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for _index, data in enumerate(generator.generate(config.templates)):
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 3  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert child.text == "value-1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode2")
            assert child.tag == "ChildNode2"
            assert child.attrib == {}
            assert child.text == "value-1"
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode3")
            assert child.tag == "ChildNode3"
            assert child.attrib == {}
            assert child.text == "value-1"
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5


def test_generate_using_special_fields_in_template_context():
    config = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "{:ChildNode1:}": "{curr_iter}",
                        "ChildNode2": "{:ChildNode1:}",
                    },
                },
            },
        ],
    })

    with MimeoContextManager(config):
        generator = XMLGenerator(config)
        count = 0
        for index, data in enumerate(generator.generate(config.templates)):
            curr_iter = index + 1
            assert data.tag == "SomeEntity"
            assert data.attrib == {}
            assert len(list(data)) == 2  # number of children

            child = data.find("ChildNode1")
            assert child.tag == "ChildNode1"
            assert child.attrib == {}
            assert child.text == str(curr_iter)
            assert len(list(child)) == 0  # number of children

            child = data.find("ChildNode2")
            assert child.tag == "ChildNode2"
            assert child.attrib == {}
            assert child.text == str(curr_iter)
            assert len(list(child)) == 0  # number of children

            count += 1

        assert count == 5

