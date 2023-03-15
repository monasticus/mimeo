import pytest

from mimeo.config import MimeoConfig
from mimeo.generators import GeneratorUtils, XMLGenerator


@pytest.fixture(autouse=True)
def setup():
    # Setup
    GeneratorUtils.get_for_context("SomeEntity").reset()
    GeneratorUtils.get_for_context("SomeEntity").setup_iteration(0)
    yield


def get_generator_for_config(config_dict: dict):
    config = MimeoConfig(config_dict)
    return XMLGenerator(config)


def test_generate_single_template_model_without_attributes():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {}
                }
            }
        ]
    })
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
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "attributes": {
                        "xmlns": "http://data-generator.arch.com/default-namespace"
                    },
                    "SomeEntity": {}
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    count = 0
    for data in generator.generate(config.templates):
        assert data.tag == "SomeEntity"
        assert data.attrib == {"xmlns": "http://data-generator.arch.com/default-namespace"}
        assert len(list(data)) == 0  # number of children

        count += 1

    assert count == 5


def test_generate_single_template_model_with_prefixed_ns():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "attributes": {
                        "xmlns:pn": "http://data-generator.arch.com/prefixed-namespace"
                    },
                    "pn:SomeEntity": {}
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    count = 0
    for data in generator.generate(config.templates):
        assert data.tag == "pn:SomeEntity"
        assert data.attrib == {"xmlns:pn": "http://data-generator.arch.com/prefixed-namespace"}
        assert len(list(data)) == 0  # number of children

        count += 1

    assert count == 5


def test_generate_single_template_str_value():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "value"
                    }
                }
            }
        ]
    })
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
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": 1
                    }
                }
            }
        ]
    })
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
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": True
                    }
                }
            }
        ]
    })
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


def test_generate_single_template_child_elements():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": {
                            "GrandChildNode": "value"
                        }
                    }
                }
            }
        ]
    })
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


def test_generate_single_template_child_elements_in_array():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNodes": [
                            {
                                "ChildNode": "value-1"
                            },
                            {
                                "ChildNode": "value-2"
                            }
                        ]
                    }
                }
            }
        ]
    })
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


def test_generate_multiple_templates():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": {}
                }
            },
            {
                "count": 3,
                "model": {
                    "SomeEntity2": {}
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    roots = [root for root in generator.generate(config.templates)]
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
        "output_format": "xml",
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
                                            "ChildNode": True
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ]
    })
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
        "output_format": "xml",
        "xml_declaration": True,
        "indent": 4,
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "attributes": {
                        "xmlns": "http://data-generator.arch.com/default-namespace",
                        "xmlns:pn": "http://data-generator.arch.com/prefixed-namespace"
                    },
                    "SomeEntity": {
                        "pn:ChildNode": "value"
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    for data in generator.generate(config.templates):
        data_str = generator.stringify(data, config)
        assert data_str == ('<?xml version="1.0" encoding="utf-8"?>\n'
                            '<SomeEntity'
                            ' xmlns="http://data-generator.arch.com/default-namespace"'
                            ' xmlns:pn="http://data-generator.arch.com/prefixed-namespace">\n'
                            '    <pn:ChildNode>value</pn:ChildNode>\n'
                            '</SomeEntity>\n')


def test_stringify_with_indent_and_without_xml_declaration():
    config = MimeoConfig({
        "output_format": "xml",
        "xml_declaration": False,
        "indent": 4,
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "attributes": {
                        "xmlns": "http://data-generator.arch.com/default-namespace",
                        "xmlns:pn": "http://data-generator.arch.com/prefixed-namespace"
                    },
                    "SomeEntity": {
                        "pn:ChildNode": "value"
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    for data in generator.generate(config.templates):
        data_str = generator.stringify(data, config)
        assert data_str == ('<SomeEntity'
                            ' xmlns="http://data-generator.arch.com/default-namespace"'
                            ' xmlns:pn="http://data-generator.arch.com/prefixed-namespace">\n'
                            '    <pn:ChildNode>value</pn:ChildNode>\n'
                            '</SomeEntity>\n')


def test_stringify_without_indent_and_with_xml_declaration():
    config = MimeoConfig({
        "output_format": "xml",
        "xml_declaration": True,
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "attributes": {
                        "xmlns": "http://data-generator.arch.com/default-namespace",
                        "xmlns:pn": "http://data-generator.arch.com/prefixed-namespace"
                    },
                    "SomeEntity": {
                        "pn:ChildNode": "value"
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    for data in generator.generate(config.templates):
        data_str = generator.stringify(data, config)
        # Notice no new line at the end of string chunks
        assert data_str == ("<?xml version='1.0' encoding='utf-8'?>\n"
                            '<SomeEntity'
                            ' xmlns="http://data-generator.arch.com/default-namespace"'
                            ' xmlns:pn="http://data-generator.arch.com/prefixed-namespace">'
                            '<pn:ChildNode>value</pn:ChildNode>'
                            '</SomeEntity>')


def test_stringify_without_indent_and_xml_declaration():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "attributes": {
                        "xmlns": "http://data-generator.arch.com/default-namespace",
                        "xmlns:pn": "http://data-generator.arch.com/prefixed-namespace"
                    },
                    "SomeEntity": {
                        "pn:ChildNode": "value"
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    for data in generator.generate(config.templates):
        data_str = generator.stringify(data, config)
        # Notice no new line at the end of string chunks
        assert data_str == ('<SomeEntity'
                            ' xmlns="http://data-generator.arch.com/default-namespace"'
                            ' xmlns:pn="http://data-generator.arch.com/prefixed-namespace">'
                            '<pn:ChildNode>value</pn:ChildNode>'
                            '</SomeEntity>')


def test_generate_template_using_auto_increment_util():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{auto_increment('{}')}"
                    }
                }
            }
        ]
    })
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


def test_generate_template_using_auto_increment_util_in_two_templates():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{auto_increment('{}')}"
                    }
                }
            },
            {
                "count": 3,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{auto_increment('{}')}"
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    count = 0
    for index, data in enumerate(generator.generate(config.templates)):
        expected_increment = index+1 if index < 5 else index-5 + 1  # from 6th item it is the second template
        assert data.tag == "SomeEntity"
        assert data.attrib == {}
        assert len(list(data)) == 1  # number of children

        child = data.find("ChildNode")
        assert child.tag == "ChildNode"
        assert child.attrib == {}
        assert child.text == str(expected_increment)
        assert len(list(child)) == 0  # number of children

        count += 1

    assert count == 8


def test_generate_template_using_curr_iter_util():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{curr_iter()}"
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    count = 0
    for index, data in enumerate(generator.generate(config.templates)):
        curr_iter = index+1
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


def test_generate_template_using_curr_iter_util():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{curr_iter()}"
                    }
                }
            },
            {
                "count": 3,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{curr_iter()}"
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    count = 0
    for index, data in enumerate(generator.generate(config.templates)):
        curr_iter = index+1 if index < 5 else index-5 + 1  # from 6th item it is the second template
        print(generator.stringify(data, config))
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


def test_generate_templates_using_curr_iter_util_in_separated_contexts():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "SingleNode": "{curr_iter()}",
                        "MultipleNodes": {
                            "_templates_": [
                                {
                                    "count": 4,
                                    "model": {
                                        "Node": {
                                            "ChildNode": "{curr_iter()}"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    count = 0
    for index, data in enumerate(generator.generate(config.templates)):
        curr_iter = index+1
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
            nested_curr_iter = nested_index+1
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


def test_generate_templates_using_curr_iter_util_in_separated_contexts_indicating_one():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "SingleNode": "{curr_iter()}",
                        "MultipleNodes": {
                            "_templates_": [
                                {
                                    "count": 4,
                                    "model": {
                                        "Node": {
                                            "ChildNode": "{curr_iter('SomeEntity')}"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    count = 0
    for index, data in enumerate(generator.generate(config.templates)):
        curr_iter = index+1
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


def test_generate_template_using_curr_iter_and_auto_increment_utils():
    config = MimeoConfig({
        "output_format": "xml",
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": "{curr_iter()}",
                        "ChildNode2": "{curr_iter()}",
                        "ChildNode3": "{auto_increment('{}')}",
                        "ChildNode4": "{auto_increment('{}')}"
                    }
                }
            }
        ]
    })
    generator = XMLGenerator(config)
    count = 0
    for index, data in enumerate(generator.generate(config.templates)):
        curr_iter = index+1
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
        assert child.text == str(curr_iter*2 - 1)  # 1, 3, 5, 7, 9
        assert len(list(child)) == 0  # number of children

        child = data.find("ChildNode4")
        assert child.tag == "ChildNode4"
        assert child.attrib == {}
        assert child.text == str(curr_iter*2)  # 2, 4, 6, 8, 10
        assert len(list(child)) == 0  # number of children

        count += 1

    assert count == 5
