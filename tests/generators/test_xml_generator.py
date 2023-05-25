from mimeo.config import MimeoConfig, MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.generators import XMLGenerator
from mimeo.generators.exc import UnsupportedStructureError
from mimeo.utils.exc import InvalidValueError
from tests.utils import assert_throws


def test_generate_single_template_model_without_attributes():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity/>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = XMLGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data.tag == "SomeEntity"
                assert data.attrib == {}
                assert len(list(data)) == 0  # number of children

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_attributes():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "@xmlns": "http://mimeo.arch.com/default-namespace",
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity xmlns="http://mimeo.arch.com/default-namespace"/>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = XMLGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data.tag == "SomeEntity"
                assert data.attrib == {"xmlns": "http://mimeo.arch.com/default-namespace"}
                assert len(list(data)) == 0  # number of children

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_prefixed_ns():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "pn:SomeEntity": {
                        "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <pn:SomeEntity xmlns:pn="http://mimeo.arch.com/prefixed-namespace"/>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = XMLGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data.tag == "pn:SomeEntity"
                assert data.attrib == {"xmlns:pn": "http://mimeo.arch.com/prefixed-namespace"}
                assert len(list(data)) == 0  # number of children

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_attributes_in_atomic_child():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "pn:ChildNode": {
                            "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            "#text": "string-value",
                        },
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <pn:ChildNode xmlns:pn="http://mimeo.arch.com/prefixed-namespace">string-value</pn:ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_attributes_in_complex_child():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "pn:ChildNode": {
                            "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            "pn:GrandChild": "string-value",
                        },
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <pn:ChildNode xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
                                <pn:GrandChild>string-value</pn:GrandChild>
                            </pn:ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_attributes_in_child_mixed():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": {
                            "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            "#text": "string-value",
                            "GrandChild": "string-value",  # will be ignored
                        },
                    },
                },
            },
        ],
    })

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)


def test_generate_single_template_str_value():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>value</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_int_value():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>1</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_bool_value():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>true</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_none_value():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode />
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_using_variables():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <vars>
                <CUSTOM_VAR_1>custom-value-1</CUSTOM_VAR_1>
                <CUSTOM_VAR_2>1</CUSTOM_VAR_2>
                <CUSTOM_VAR_3>true</CUSTOM_VAR_3>
                <CUSTOM_VAR_4>{CUSTOM_VAR_2}</CUSTOM_VAR_4>
                <CUSTOM_VAR_5>{curr_iter}</CUSTOM_VAR_5>
                <CUSTOM_VAR_6>
                    <_mimeo_util>
                        <_name>auto_increment</_name>
                        <pattern>{}</pattern>
                    </_mimeo_util>
                </CUSTOM_VAR_6>
            </vars>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode1>{CUSTOM_VAR_1}</ChildNode1>
                            <ChildNode2>{CUSTOM_VAR_2}</ChildNode2>
                            <ChildNode3>{CUSTOM_VAR_3}</ChildNode3>
                            <ChildNode4>{CUSTOM_VAR_4}</ChildNode4>
                            <ChildNode5>{CUSTOM_VAR_5}</ChildNode5>
                            <ChildNode6>{CUSTOM_VAR_6}</ChildNode6>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_child_elements():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>
                                <GrandChildNode>value</GrandChildNode>
                            </ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_only_atomic_child_elements_in_array():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNodes": {
                            "ChildNode": [
                                "value-1",
                                1,
                                True,
                            ],
                        },
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNodes>
                                <ChildNode>value-1</ChildNode>
                                <ChildNode>1</ChildNode>
                                <ChildNode>true</ChildNode>
                            </ChildNodes>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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
                assert len(list(child_nodes_node)) == 3  # number of children

                child_nodes = child_nodes_node.findall("ChildNode")

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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_only_complex_child_elements_in_array():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNodes": {
                            "ChildNode": [
                                {
                                    "SomeValue1": "value-1-1",
                                    "SomeValue2": "value-1-2",
                                },
                                {
                                    "SomeValue1": "value-2-1",
                                    "SomeValue2": "value-2-2",
                                },
                            ],
                        },
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNodes>
                                <ChildNode>
                                    <SomeValue1>value-1-1</SomeValue1>
                                    <SomeValue2>value-1-2</SomeValue2>
                                </ChildNode>
                                <ChildNode>
                                    <SomeValue1>value-2-1</SomeValue1>
                                    <SomeValue2>value-2-2</SomeValue2>
                                </ChildNode>
                            </ChildNodes>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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
                assert len(list(child_node1)) == 2  # number of children
                some_value_1_1 = child_node1.find("SomeValue1")
                assert some_value_1_1.tag == "SomeValue1"
                assert some_value_1_1.attrib == {}
                assert some_value_1_1.text == "value-1-1"
                assert len(list(some_value_1_1)) == 0  # number of children
                some_value_1_2 = child_node1.find("SomeValue2")
                assert some_value_1_2.tag == "SomeValue2"
                assert some_value_1_2.attrib == {}
                assert some_value_1_2.text == "value-1-2"
                assert len(list(some_value_1_2)) == 0  # number of children

                child_node2 = child_nodes[1]
                assert child_node2.tag == "ChildNode"
                assert child_node2.attrib == {}
                assert len(list(child_node2)) == 2  # number of children
                some_value_2_1 = child_node2.find("SomeValue1")
                assert some_value_2_1.tag == "SomeValue1"
                assert some_value_2_1.attrib == {}
                assert some_value_2_1.text == "value-2-1"
                assert len(list(some_value_2_1)) == 0  # number of children
                some_value_2_2 = child_node2.find("SomeValue2")
                assert some_value_2_2.tag == "SomeValue2"
                assert some_value_2_2.attrib == {}
                assert some_value_2_2.text == "value-2-2"
                assert len(list(some_value_2_2)) == 0  # number of children

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_atomic_child_elements_with_mimeo_util_in_array():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNodes": {
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
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNodes>
                                <ChildNode>value-1</ChildNode>
                                <ChildNode>
                                    <_mimeo_util>
                                        <_name>auto_increment</_name>
                                        <pattern>{}</pattern>
                                    </_mimeo_util>
                                </ChildNode>
                            </ChildNodes>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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
                assert child_node2.text == str(count + 1)
                assert len(list(child_node2)) == 0  # number of children

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_mixed_child_elements_in_array():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNodes": {
                            "ChildNode": [
                                "value-1",
                                {
                                    "SomeValue1": "value-2-1",
                                    "SomeValue2": "value-2-2",
                                },
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
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNodes>
                                <ChildNode>value-1</ChildNode>
                                <ChildNode>
                                    <SomeValue1>value-2-1</SomeValue1>
                                    <SomeValue2>value-2-2</SomeValue2>
                                </ChildNode>
                                <ChildNode>
                                    <_mimeo_util>
                                        <_name>auto_increment</_name>
                                        <pattern>{}</pattern>
                                    </_mimeo_util>
                                </ChildNode>
                            </ChildNodes>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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
                assert len(list(child_nodes_node)) == 3  # number of children

                child_nodes = child_nodes_node.findall("ChildNode")

                child_node1 = child_nodes[0]
                assert child_node1.tag == "ChildNode"
                assert child_node1.attrib == {}
                assert child_node1.text == "value-1"
                assert len(list(child_node1)) == 0  # number of children

                child_node2 = child_nodes[1]
                assert child_node2.tag == "ChildNode"
                assert child_node2.attrib == {}
                assert len(list(child_node2)) == 2  # number of children
                some_value_1 = child_node2.find("SomeValue1")
                assert some_value_1.tag == "SomeValue1"
                assert some_value_1.attrib == {}
                assert some_value_1.text == "value-2-1"
                assert len(list(some_value_1)) == 0  # number of children
                some_value_2 = child_node2.find("SomeValue2")
                assert some_value_2.tag == "SomeValue2"
                assert some_value_2.attrib == {}
                assert some_value_2.text == "value-2-2"
                assert len(list(some_value_2)) == 0  # number of children

                child_node3 = child_nodes[2]
                assert child_node3.tag == "ChildNode"
                assert child_node3.attrib == {}
                assert child_node3.text == str(count + 1)
                assert len(list(child_node3)) == 0  # number of children

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_list_child_element_in_array():
    config_from_dict = MimeoConfig({
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

    @assert_throws(err_type=UnsupportedStructureError,
                   msg="An array can include only atomic types (including Mimeo Utils) "
                       "or only JSON objects! Unsupported structure found in {e}: {s}",
                   e="ChildNode", s="[['atomic']]")
    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = XMLGenerator(config)
            for _ in generator.generate(config.templates):
                pass

    _test(config_from_dict)


def test_generate_multiple_templates():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>2</count>
                    <model>
                        <SomeEntity />
                    </model>
                </_template_>
                <_template_>
                    <count>3</count>
                    <model>
                        <SomeEntity2 />
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_nested_templates():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <SingleNode>value</SingleNode>
                            <MultipleNodes>
                                <_templates_>
                                    <_template_>
                                        <count>4</count>
                                        <model>
                                            <Node>
                                                <ChildNode>true</ChildNode>
                                            </Node>
                                        </model>
                                    </_template_>
                                </_templates_>
                            </MultipleNodes>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_stringify_with_indent_and_xml_declaration():
    config_from_dict = MimeoConfig({
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
                        "@xmlns": "http://mimeo.arch.com/default-namespace",
                        "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        "pn:ChildNode": "value",
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
                <xml_declaration>true</xml_declaration>
                <indent>4</indent>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity
                            xmlns="http://mimeo.arch.com/default-namespace"
                            xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
                            <pn:ChildNode>value</pn:ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_stringify_with_indent_and_without_xml_declaration():
    config_from_dict = MimeoConfig({
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
                        "@xmlns": "http://mimeo.arch.com/default-namespace",
                        "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        "pn:ChildNode": "value",
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
                <xml_declaration>false</xml_declaration>
                <indent>4</indent>
            </output>
            <_templates_>
                <_template_>
                    <count>1</count>
                    <model>
                        <SomeEntity
                            xmlns="http://mimeo.arch.com/default-namespace"
                            xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
                            <pn:ChildNode>value</pn:ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = XMLGenerator(config)
            for data in generator.generate(config.templates):
                data_str = generator.stringify(data)
                assert data_str == ('<SomeEntity'
                                    ' xmlns="http://mimeo.arch.com/default-namespace"'
                                    ' xmlns:pn="http://mimeo.arch.com/prefixed-namespace">\n'
                                    '    <pn:ChildNode>value</pn:ChildNode>\n'
                                    '</SomeEntity>\n')

    _test(config_from_dict)
    _test(config_from_xml)


def test_stringify_without_indent_and_with_xml_declaration():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
            "xml_declaration": True,
        },
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "SomeEntity": {
                        "@xmlns": "http://mimeo.arch.com/default-namespace",
                        "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        "pn:ChildNode": "value",
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
                <xml_declaration>true</xml_declaration>
            </output>
            <_templates_>
                <_template_>
                    <count>1</count>
                    <model>
                        <SomeEntity
                            xmlns="http://mimeo.arch.com/default-namespace"
                            xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
                            <pn:ChildNode>value</pn:ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_stringify_without_indent_and_xml_declaration():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 1,
                "model": {
                    "SomeEntity": {
                        "@xmlns": "http://mimeo.arch.com/default-namespace",
                        "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                        "pn:ChildNode": "value",
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>1</count>
                    <model>
                        <SomeEntity
                            xmlns="http://mimeo.arch.com/default-namespace"
                            xmlns:pn="http://mimeo.arch.com/prefixed-namespace">
                            <pn:ChildNode>value</pn:ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_mimeo_util_raw():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>{auto_increment}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_mimeo_util_parametrized():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>
                                <_mimeo_util>
                                    <_name>auto_increment</_name>
                                    <pattern>{}</pattern>
                                </_mimeo_util>
                            </ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_mimeo_util_parametrized_invalid():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>
                                <_mimeo_util>
                                    <_name>auto_increment</_name>
                                    <pattern>1</pattern>
                                </_mimeo_util>
                            </ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    @assert_throws(err_type=InvalidValueError,
                   msg="The auto_increment Mimeo Util require a string value "
                       "for the pattern parameter and was: [{pattern}].",
                   pattern=1)
    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = XMLGenerator(config)
            for _ in generator.generate(config.templates):
                pass

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_auto_increment():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>{auto_increment}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_auto_increment_in_two_templates():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>{auto_increment}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
                <_template_>
                    <count>3</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>{auto_increment}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_auto_increment_in_two_templates_with_customized_context_name():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>{auto_increment}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
                <_template_>
                    <count>3</count>
                    <model>
                        <context>A different set</context>
                        <SomeEntity>
                            <ChildNode>{auto_increment}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_curr_iter_util():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>{curr_iter}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_curr_iter_util_in_two_templates():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>{curr_iter}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
                <_template_>
                    <count>3</count>
                    <model>
                        <SomeEntity>
                            <ChildNode>{curr_iter}</ChildNode>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generates_using_curr_iter_util_in_nested_templates():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <SingleNode>{curr_iter}</SingleNode>
                            <MultipleNodes>
                                <_templates_>
                                    <_template_>
                                        <count>4</count>
                                        <model>
                                            <Node>
                                                <ChildNode>{curr_iter}</ChildNode>
                                            </Node>
                                        </model>
                                    </_template_>
                                </_templates_>
                            </MultipleNodes>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generates_using_curr_iter_util_in_nested_templates_indicating_one():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <SingleNode>{curr_iter}</SingleNode>
                            <MultipleNodes>
                                <_templates_>
                                    <_template_>
                                        <count>4</count>
                                        <model>
                                            <Node>
                                                <ChildNode>
                                                    <_mimeo_util>
                                                        <_name>curr_iter</_name>
                                                        <context>SomeEntity</context>
                                                    </_mimeo_util>
                                                </ChildNode>
                                            </Node>
                                        </model>
                                    </_template_>
                                </_templates_>
                            </MultipleNodes>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generates_using_curr_iter_util_in_nested_templates_indicating_customized_one():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <context>ROOT</context>
                        <SomeEntity>
                            <SingleNode>{curr_iter}</SingleNode>
                            <MultipleNodes>
                                <_templates_>
                                    <_template_>
                                        <count>4</count>
                                        <model>
                                            <Node>
                                                <ChildNode>
                                                    <_mimeo_util>
                                                        <_name>curr_iter</_name>
                                                        <context>ROOT</context>
                                                    </_mimeo_util>
                                                </ChildNode>
                                            </Node>
                                        </model>
                                    </_template_>
                                </_templates_>
                            </MultipleNodes>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_curr_iter_and_auto_increment_utils():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode1>{curr_iter}</ChildNode1>
                            <ChildNode2>{curr_iter}</ChildNode2>
                            <ChildNode3>{auto_increment}</ChildNode3>
                            <ChildNode4>{auto_increment}</ChildNode4>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_key_util():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode1>{key}</ChildNode1>
                            <ChildNode2>{key}</ChildNode2>
                            <ChildNode3>{key}</ChildNode3>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_key_util_in_separated_contexts():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode1>{key}</ChildNode1>
                            <_templates_>
                                <_template_>
                                    <count>1</count>
                                    <model>
                                        <NewContextNode>
                                            <GrandChild>{key}</GrandChild>
                                        </NewContextNode>
                                    </model>
                                </_template_>
                            </_templates_>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_key_util_in_separated_contexts_indicating_one():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <ChildNode1>{key}</ChildNode1>
                            <_templates_>
                                <_template_>
                                    <count>1</count>
                                    <model>
                                        <NewContextNode>
                                            <GrandChild>
                                                <_mimeo_util>
                                                    <_name>key</_name>
                                                    <context>SomeEntity</context>
                                                </_mimeo_util>
                                            </GrandChild>
                                        </NewContextNode>
                                    </model>
                                </_template_>
                            </_templates_>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_key_util_in_two_templates_with_customized_iteration():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <CustomIteration1>
                            <ChildNode1>{key}</ChildNode1>
                        </CustomIteration1>
                    </model>
                </_template_>
                <_template_>
                    <count>5</count>
                    <model>
                        <CustomIteration2>
                            <ChildNode1>
                                <_mimeo_util>
                                    <_name>key</_name>
                                    <context>CustomIteration1</context>
                                    <iteration>{curr_iter}</iteration>
                                </_mimeo_util>
                            </ChildNode1>
                        </CustomIteration2>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_get_key_util_in_two_templates_with_customized_context_name():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <context>First SomeEntity set</context>
                        <SomeEntity>
                            <ChildNode1>{key}</ChildNode1>
                        </SomeEntity>
                    </model>
                </_template_>
                <_template_>
                    <count>5</count>
                    <model>
                        <context>Second SomeEntity set</context>
                        <SomeEntity>
                            <ChildNode1>
                                <_mimeo_util>
                                    <_name>key</_name>
                                    <context>First SomeEntity set</context>
                                </_mimeo_util>
                            </ChildNode1>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <:ChildNode1:>value-1</:ChildNode1:>
                            <ChildNode2>{:ChildNode1:}</ChildNode2>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields_as_partial_values():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <:ChildNode1:>value-1</:ChildNode1:>
                            <:ChildNode2:>value-2</:ChildNode2:>
                            <ChildNode3>{:ChildNode1:}-2</ChildNode3>
                            <ChildNode4>3-{:ChildNode1:}-3</ChildNode4>
                            <ChildNode5>4-{:ChildNode1:}</ChildNode5>
                            <ChildNode6>{:ChildNode1:}-{:ChildNode1:}</ChildNode6>
                            <ChildNode7>{:ChildNode1:}-{:ChildNode2:}</ChildNode7>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields_using_namespace():
    config_from_dict = MimeoConfig({
        "output": {
            "format": "xml",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "ns:SomeEntity": {
                        "@xmlns:ns": "http://mimeo.arch.com/prefixed-namespace",
                        "{:ns:ChildNode1:}": "value-1",
                        "ns:ChildNode2": "{:ns:ChildNode1:}",
                    },
                },
            },
        ],
    })
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <ns:SomeEntity xmlns:ns="http://mimeo.arch.com/prefixed-namespace">
                            <:ns:ChildNode1:>value-1</:ns:ChildNode1:>
                            <ns:ChildNode2>{:ns:ChildNode1:}</ns:ChildNode2>
                        </ns:SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields_recursive():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <:ChildNode1:>value-1</:ChildNode1:>
                            <:ChildNode2:>{:ChildNode1:}</:ChildNode2:>
                            <ChildNode3>{:ChildNode2:}</ChildNode3>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields_in_template_context():
    config_from_dict = MimeoConfig({
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
    config_from_xml = MimeoConfig(MimeoConfigFactory.parse_source("""
        <mimeo_configuration>
            <output>
                <format>xml</format>
            </output>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <:ChildNode1:>{curr_iter}</:ChildNode1:>
                            <ChildNode2>{:ChildNode1:}</ChildNode2>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """))

    def _test(
            config: MimeoConfig,
    ):
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

    _test(config_from_dict)
    _test(config_from_xml)
