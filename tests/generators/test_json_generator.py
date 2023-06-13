from mimeo.config import MimeoConfig, MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.generators import JSONGenerator
from mimeo.generators.exc import UnsupportedStructureError
from mimeo.utils.exc import InvalidValueError
from tests.utils import assert_throws


def test_generate_single_template_model_without_attributes():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": None,
                },
            },
        ],
    })
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": None,
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_attributes():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "@xmlns": "http://mimeo.arch.com/default-namespace",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_prefixed_ns():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "pn:SomeEntity": {
                        "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_attributes_in_atomic_child():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "pn:ChildNode": {
                            "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            "#text": "string-value",
                        },
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_attributes_in_complex_child():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "pn:ChildNode": {
                            "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            "pn:GrandChild": "string-value",
                        },
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_model_with_attributes_in_child_mixed():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": {
                            "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            "#text": "string-value",
                            "GrandChild": "string-value",  # will NOT be ignored
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
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNode": {
                            "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",
                            "#text": "string-value",
                            "GrandChild": "string-value",  # will NOT be ignored
                        },
                    },
                }

                count += 1

    _test(config_from_dict)


def test_generate_single_template_str_value():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNode": "value",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_int_value():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNode": 1,
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_bool_value():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNode": True,
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_none_value():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNode": None,
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_using_variables():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for index, data in enumerate(generator.generate(config.templates)):
                assert data == {
                    "SomeEntity": {
                        "ChildNode1": "custom-value-1",
                        "ChildNode2": 1,
                        "ChildNode3": True,
                        "ChildNode4": 1,
                        "ChildNode5": index+1,
                        "ChildNode6": str(index+1),
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_child_elements():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNode": {
                            "GrandChildNode": "value",
                        },
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_only_atomic_child_elements_in_array():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNodes": {
                            "ChildNode": [
                                "value-1",
                                1,
                                True,
                            ],
                        },
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_only_complex_child_elements_in_array():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
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
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_atomic_child_elements_with_mimeo_util_in_array():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNodes": {
                            "ChildNode": [
                                "value-1",
                                str(count + 1),
                            ],
                        },
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_mixed_child_elements_in_array():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNodes": {
                            "ChildNode": [
                                "value-1",
                                {
                                    "SomeValue1": "value-2-1",
                                    "SomeValue2": "value-2-2",
                                },
                                str(count + 1),
                            ],
                        },
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_single_template_list_child_element_in_array():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for data in generator.generate(config.templates):
                assert data == {
                    "SomeEntity": {
                        "ChildNode": [
                            [
                                "atomic",
                            ],
                        ],
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)


def test_generate_multiple_templates():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 2,
                "model": {
                    "SomeEntity": None,
                },
            },
            {
                "count": 3,
                "model": {
                    "SomeEntity2": None,
                },
            },
        ],
    })
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            nodes = list(generator.generate(config.templates))
            template_1_nodes = nodes[:2]
            template_2_nodes = nodes[2:]

            assert len(nodes) == 5
            assert len(template_1_nodes) == 2
            assert len(template_2_nodes) == 3

            for data in template_1_nodes:
                assert data == {
                    "SomeEntity": None,
                }

            for data in template_2_nodes:
                assert data == {
                    "SomeEntity2": None,
                }

    _test(config_from_dict)
    _test(config_from_xml)