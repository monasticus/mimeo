from mimeo.config import MimeoConfig, MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.context.exc import (NoCorrespondingReferenceError,
                               NonPopulatedReferenceError)
from mimeo.generators import JSONGenerator
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


def test_generate_nested_templates():
    config_from_dict_templates_in_array = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "SingleNode": "value",
                        "MultipleNodes": [
                            {
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
                        ],
                    },
                },
            },
        ],
    })
    config_from_dict_templates_in_object = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
                        "SingleNode": "value",
                        "MultipleNodes": [
                            {
                                "Node": {
                                    "ChildNode": True,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": True,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": True,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": True,
                                },
                            },
                        ],
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict_templates_in_array)
    _test(config_from_dict_templates_in_object)
    _test(config_from_xml)


def test_generate_nested_templates_mixed_with_other_elements():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "SingleNode": "value",
                        "MultipleNodes": {
                            "NodesCount": 4,  # Will be ignored
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
                            <SingleNode>value</SingleNode>
                            <MultipleNodes>
                                <NodesCount>4</NodesCount> <!-- will be ignored -->
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
                        "SingleNode": "value",
                        "MultipleNodes": [
                            {
                                "Node": {
                                    "ChildNode": True,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": True,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": True,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": True,
                                },
                            },
                        ],
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_stringify_with_indent():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
            "indent": 2,
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
                <xml_declaration>false</xml_declaration>
                <indent>2</indent>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            for data in generator.generate(config.templates):
                data_str = generator.stringify(data)
                assert data_str == ('{\n'
                                    '  "SomeEntity": {\n'
                                    '    "@xmlns": "http://mimeo.arch.com/default-namespace",\n'
                                    '    "@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace",\n'
                                    '    "pn:ChildNode": "value"\n'
                                    '  }\n'
                                    '}')

    _test(config_from_dict)
    _test(config_from_xml)


def test_stringify_without_indent():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            for data in generator.generate(config.templates):
                data_str = generator.stringify(data)
                # Notice no new line at the end of string chunks
                assert data_str == (
                    '{"SomeEntity": {'
                    '"@xmlns": "http://mimeo.arch.com/default-namespace", '
                    '"@xmlns:pn": "http://mimeo.arch.com/prefixed-namespace", '
                    '"pn:ChildNode": "value"'
                    '}}')

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_mimeo_util_raw():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
                            <ChildNode>{auto_increment}</ChildNode>
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
                        "ChildNode": f"{index + 1:05d}",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_mimeo_util_parametrized():
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
                        "ChildNode": str(index + 1),
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_mimeo_util_parametrized_invalid():
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
    """)

    @assert_throws(err_type=InvalidValueError,
                   msg="The auto_increment Mimeo Util require a string value "
                       "for the pattern parameter and was: [{pattern}].",
                   pattern=1)
    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            for _ in generator.generate(config.templates):
                pass

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_auto_increment():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
                            <ChildNode>{auto_increment}</ChildNode>
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
                        "ChildNode": f"{index + 1:05d}",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_auto_increment_in_two_templates():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
                        "ChildNode": f"{index + 1:05d}",
                    },
                }

                count += 1

            assert count == 8

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_auto_increment_in_two_templates_with_customized_context_name():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for index, data in enumerate(generator.generate(config.templates)):
                # from 6th item it is the second template
                expected_increment = index + 1 if index < 5 else index - 5 + 1
                assert data == {
                    "SomeEntity": {
                        "ChildNode": f"{expected_increment:05d}",
                    },
                }

                count += 1

            assert count == 8

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_curr_iter_util():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
                            <ChildNode>{curr_iter}</ChildNode>
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
                curr_iter = index + 1
                assert data == {
                    "SomeEntity": {
                        "ChildNode": curr_iter,
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_curr_iter_util_in_two_templates():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for index, data in enumerate(generator.generate(config.templates)):
                # from 6th item it is the second template
                curr_iter = index + 1 if index < 5 else index - 5 + 1
                assert data == {
                    "SomeEntity": {
                        "ChildNode": curr_iter,
                    },
                }

                count += 1

            assert count == 8

    _test(config_from_dict)
    _test(config_from_xml)


def test_generates_using_curr_iter_util_in_nested_templates():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for index, data in enumerate(generator.generate(config.templates)):
                curr_iter = index + 1
                assert data == {
                    "SomeEntity": {
                        "SingleNode": curr_iter,
                        "MultipleNodes": [
                            {
                                "Node": {
                                    "ChildNode": 1,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": 2,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": 3,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": 4,
                                },
                            },
                        ],
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generates_using_curr_iter_util_in_nested_templates_indicating_one():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for index, data in enumerate(generator.generate(config.templates)):
                curr_iter = index + 1
                assert data == {
                    "SomeEntity": {
                        "SingleNode": curr_iter,
                        "MultipleNodes": [
                            {
                                "Node": {
                                    "ChildNode": curr_iter,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": curr_iter,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": curr_iter,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": curr_iter,
                                },
                            },
                        ],
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generates_using_curr_iter_util_in_nested_templates_indicating_customized_one():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for index, data in enumerate(generator.generate(config.templates)):
                curr_iter = index + 1
                assert data == {
                    "SomeEntity": {
                        "SingleNode": curr_iter,
                        "MultipleNodes": [
                            {
                                "Node": {
                                    "ChildNode": curr_iter,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": curr_iter,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": curr_iter,
                                },
                            },
                            {
                                "Node": {
                                    "ChildNode": curr_iter,
                                },
                            },
                        ],
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_curr_iter_and_auto_increment_utils():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
                            <ChildNode1>{curr_iter}</ChildNode1>
                            <ChildNode2>{curr_iter}</ChildNode2>
                            <ChildNode3>{auto_increment}</ChildNode3>
                            <ChildNode4>{auto_increment}</ChildNode4>
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
                curr_iter = index + 1
                assert data == {
                    "SomeEntity": {
                        "ChildNode1": curr_iter,
                        "ChildNode2": curr_iter,
                        "ChildNode3": f"{curr_iter * 2 - 1:05d}",  # 1, 3, 5, 7, 9
                        "ChildNode4": f"{curr_iter * 2:05d}",  # 2, 4, 6, 8, 10
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_key_util():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
                            <ChildNode1>{key}</ChildNode1>
                            <ChildNode2>{key}</ChildNode2>
                            <ChildNode3>{key}</ChildNode3>
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
            keys = []
            for _index, data in enumerate(generator.generate(config.templates)):
                assert len(data) == 1
                assert "SomeEntity" in data
                assert len(data["SomeEntity"]) == 3
                assert "ChildNode1" in data["SomeEntity"]
                assert "ChildNode2" in data["SomeEntity"]
                assert "ChildNode3" in data["SomeEntity"]
                assert isinstance(data["SomeEntity"]["ChildNode1"], str)
                assert isinstance(data["SomeEntity"]["ChildNode2"], str)
                assert isinstance(data["SomeEntity"]["ChildNode3"], str)

                key1 = data["SomeEntity"]["ChildNode1"]
                key2 = data["SomeEntity"]["ChildNode2"]
                key3 = data["SomeEntity"]["ChildNode3"]

                assert key1 == key2
                assert key2 == key3
                keys.append(key1)

                count += 1

            assert count == 5
            assert len(set(keys)) == len(keys)

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_key_util_in_separated_contexts():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{key}",
                        "OtherChildren": {
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
                            <ChildNode>{key}</ChildNode>
                            <OtherChildren>
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
                            </OtherChildren>
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
            for _index, data in enumerate(generator.generate(config.templates)):
                assert len(data) == 1
                assert "SomeEntity" in data
                assert len(data["SomeEntity"]) == 2
                assert "ChildNode" in data["SomeEntity"]
                assert "OtherChildren" in data["SomeEntity"]

                assert isinstance(data["SomeEntity"]["ChildNode"], str)
                assert isinstance(data["SomeEntity"]["OtherChildren"], list)
                assert len(data["SomeEntity"]["OtherChildren"]) == 1
                other_child = data["SomeEntity"]["OtherChildren"][0]
                assert len(other_child) == 1
                assert "NewContextNode" in other_child
                assert len(other_child["NewContextNode"]) == 1
                assert "GrandChild" in other_child["NewContextNode"]
                assert isinstance(other_child["NewContextNode"]["GrandChild"], str)

                key1 = data["SomeEntity"]["ChildNode"]
                key2 = other_child["NewContextNode"]["GrandChild"]

                assert key1 != key2

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_key_util_in_separated_contexts_indicating_one():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "ChildNode": "{key}",
                        "OtherChildren": {
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
                            <ChildNode>{key}</ChildNode>
                            <OtherChildren>
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
                            </OtherChildren>
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
            for _index, data in enumerate(generator.generate(config.templates)):
                assert len(data) == 1
                assert "SomeEntity" in data
                assert len(data["SomeEntity"]) == 2
                assert "ChildNode" in data["SomeEntity"]
                assert "OtherChildren" in data["SomeEntity"]

                assert isinstance(data["SomeEntity"]["ChildNode"], str)
                assert isinstance(data["SomeEntity"]["OtherChildren"], list)
                assert len(data["SomeEntity"]["OtherChildren"]) == 1
                other_child = data["SomeEntity"]["OtherChildren"][0]
                assert len(other_child) == 1
                assert "NewContextNode" in other_child
                assert len(other_child["NewContextNode"]) == 1
                assert "GrandChild" in other_child["NewContextNode"]
                assert isinstance(other_child["NewContextNode"]["GrandChild"], str)

                key1 = data["SomeEntity"]["ChildNode"]
                key2 = other_child["NewContextNode"]["GrandChild"]

                assert key1 == key2

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_key_util_in_two_templates_with_customized_iteration():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            data = list(generator.generate(config.templates))
            some_entity_data = data[:5]
            some_other_entity_data = data[5:]

            assert len(data) == 10
            assert len(some_entity_data) == 5
            assert len(some_other_entity_data) == 5

            some_entity_keys = []
            some_other_entity_keys = []
            for data in some_entity_data:
                assert len(data) == 1
                assert "CustomIteration1" in data
                assert len(data["CustomIteration1"]) == 1
                assert "ChildNode1" in data["CustomIteration1"]
                assert isinstance(data["CustomIteration1"]["ChildNode1"], str)

                key = data["CustomIteration1"]["ChildNode1"]
                some_entity_keys.append(key)

            for data in some_other_entity_data:
                assert len(data) == 1
                assert "CustomIteration2" in data
                assert len(data["CustomIteration2"]) == 1
                assert "ChildNode1" in data["CustomIteration2"]
                assert isinstance(data["CustomIteration2"]["ChildNode1"], str)

                key = data["CustomIteration2"]["ChildNode1"]
                some_other_entity_keys.append(key)

            for i in range(5):
                assert some_entity_keys[i] == some_other_entity_keys[i]

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_get_key_util_in_two_templates_with_customized_context_name():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
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
    config_from_xml = MimeoConfigFactory.parse("""
        <mimeo_configuration>
            <output>
                <format>json</format>
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            data = list(generator.generate(config.templates))
            some_entity_data = data[:5]
            some_other_entity_data = data[5:]

            assert len(data) == 10
            assert len(some_entity_data) == 5
            assert len(some_other_entity_data) == 5

            first_set_keys = []
            for data in some_entity_data:
                assert len(data) == 1
                assert "SomeEntity" in data
                assert len(data["SomeEntity"]) == 1
                assert "ChildNode1" in data["SomeEntity"]
                assert isinstance(data["SomeEntity"]["ChildNode1"], str)

                key = data["SomeEntity"]["ChildNode1"]
                first_set_keys.append(key)

            for data in some_other_entity_data:
                assert data == {
                    "SomeEntity": {
                        "ChildNode1": first_set_keys[-1],
                    },
                }

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        ":ChildNode1:": "value-1",
                        "ChildNode2": "{:ChildNode1:}",
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
                            <:ChildNode1:>value-1</:ChildNode1:>
                            <ChildNode2>{:ChildNode1:}</ChildNode2>
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
            for _index, data in enumerate(generator.generate(config.templates)):
                assert data == {
                    "SomeEntity": {
                        "ChildNode1": "value-1",
                        "ChildNode2": "value-1",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields_as_partial_values():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        ":ChildNode1:": "value-1",
                        ":ChildNode2:": "value-2",
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
    """)

    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            count = 0
            for _index, data in enumerate(generator.generate(config.templates)):
                assert data == {
                    "SomeEntity": {
                        "ChildNode1": "value-1",
                        "ChildNode2": "value-2",
                        "ChildNode3": "value-1-2",
                        "ChildNode4": "3-value-1-3",
                        "ChildNode5": "4-value-1",
                        "ChildNode6": "value-1-value-1",
                        "ChildNode7": "value-1-value-2",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields_using_namespace():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "ns:SomeEntity": {
                        "@xmlns:ns": "http://mimeo.arch.com/prefixed-namespace",
                        ":ns:ChildNode1:": "value-1",
                        "ns:ChildNode2": "{:ns:ChildNode1:}",
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
                        <ns:SomeEntity xmlns:ns="http://mimeo.arch.com/prefixed-namespace">
                            <:ns:ChildNode1:>value-1</:ns:ChildNode1:>
                            <ns:ChildNode2>{:ns:ChildNode1:}</ns:ChildNode2>
                        </ns:SomeEntity>
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
            for _index, data in enumerate(generator.generate(config.templates)):
                assert data == {
                    "ns:SomeEntity": {
                        "@xmlns:ns": "http://mimeo.arch.com/prefixed-namespace",
                        "ns:ChildNode1": "value-1",
                        "ns:ChildNode2": "value-1",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields_recursive():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        ":ChildNode1:": "value-1",
                        ":ChildNode2:": "{:ChildNode1:}",
                        "ChildNode3": "{:ChildNode2:}",
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
                            <:ChildNode1:>value-1</:ChildNode1:>
                            <:ChildNode2:>{:ChildNode1:}</:ChildNode2:>
                            <ChildNode3>{:ChildNode2:}</ChildNode3>
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
            for _index, data in enumerate(generator.generate(config.templates)):
                assert data == {
                    "SomeEntity": {
                        "ChildNode1": "value-1",
                        "ChildNode2": "value-1",
                        "ChildNode3": "value-1",
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_special_fields_in_template_context():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        ":ChildNode1:": "{curr_iter}",
                        "ChildNode2": "{:ChildNode1:}",
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
                            <:ChildNode1:>{curr_iter}</:ChildNode1:>
                            <ChildNode2>{:ChildNode1:}</ChildNode2>
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
                curr_iter = index + 1
                assert data == {
                    "SomeEntity": {
                        "ChildNode1": curr_iter,
                        "ChildNode2": curr_iter,
                    },
                }

                count += 1

            assert count == 5

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_reference_of_any_type():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "refs": {
            "parent": {
                "context": "SomeEntity",
                "field": "Node1",
                "type": "any",
            },
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "Node1": "{auto_increment}",
                    },
                },
            },
            {
                "count": 5,
                "model": {
                    "SomeChildEntity": {
                        "Parent": "{parent}",
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
            <refs>
                <parent>
                    <context>SomeEntity</context>
                    <field>Node1</field>
                    <type>any</type>
                </parent>
            </refs>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <Node1>{auto_increment}</Node1>
                        </SomeEntity>
                    </model>
                </_template_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeChildEntity>
                            <Parent>{parent}</Parent>
                        </SomeChildEntity>
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

            data = list(generator.generate(config.templates))
            parent_data = data[:5]
            child_data = data[5:]

            assert len(data) == 10
            assert len(parent_data) == 5
            assert len(child_data) == 5

            refs = []
            for index, data in enumerate(parent_data):
                assert data == {
                    "SomeEntity": {
                        "Node1": f"{index+1:05d}",
                    },
                }
                refs.append(data["SomeEntity"]["Node1"])

            for data in child_data:
                assert len(data) == 1
                assert "SomeChildEntity" in data
                assert len(data["SomeChildEntity"]) == 1
                assert "Parent" in data["SomeChildEntity"]
                assert data["SomeChildEntity"]["Parent"] in refs

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_reference_of_parallel_type():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "refs": {
            "parent": {
                "context": "SomeEntity",
                "field": "Node1",
                "type": "parallel",
            },
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "Node1": "{auto_increment}",
                    },
                },
            },
            {
                "count": 5,
                "model": {
                    "SomeChildEntity": {
                        "Parent": "{parent}",
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
            <refs>
                <parent>
                    <context>SomeEntity</context>
                    <field>Node1</field>
                    <type>parallel</type>
                </parent>
            </refs>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <Node1>{auto_increment}</Node1>
                        </SomeEntity>
                    </model>
                </_template_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeChildEntity>
                            <Parent>{parent}</Parent>
                        </SomeChildEntity>
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

            data = list(generator.generate(config.templates))
            parent_data = data[:5]
            child_data = data[5:]

            assert len(data) == 10
            assert len(parent_data) == 5
            assert len(child_data) == 5

            refs = []
            for index, data in enumerate(parent_data):
                assert data == {
                    "SomeEntity": {
                        "Node1": f"{index+1:05d}",
                    },
                }
                refs.append(data["SomeEntity"]["Node1"])

            for index, data in enumerate(child_data):
                assert len(data) == 1
                assert "SomeChildEntity" in data
                assert len(data["SomeChildEntity"]) == 1
                assert "Parent" in data["SomeChildEntity"]
                assert data["SomeChildEntity"]["Parent"] == refs[index]

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_reference_before_populated():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "refs": {
            "parent": {
                "context": "SomeEntity",
                "field": "Node1",
                "type": "any",
            },
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeChildEntity": {
                        "Parent": "{parent}",
                    },
                },
            },
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "Node1": "{auto_increment}",
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
            <refs>
                <parent>
                    <context>SomeEntity</context>
                    <field>Node1</field>
                    <type>any</type>
                </parent>
            </refs>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeChildEntity>
                            <Parent>{parent}</Parent>
                        </SomeChildEntity>
                    </model>
                </_template_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <Node1>{auto_increment}</Node1>
                        </SomeEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """)

    @assert_throws(err_type=NonPopulatedReferenceError,
                   msg="Reference [{ref}] has not been populated with any value!",
                   ref="parent")
    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            for _ in generator.generate(config.templates):
                pass

    _test(config_from_dict)
    _test(config_from_xml)


def test_generate_using_reference_not_being_generated():
    config_from_dict = MimeoConfigFactory.parse({
        "output": {
            "format": "json",
        },
        "refs": {
            "parent": {
                "context": "SomeEntity",
                "field": "Node1",
                "type": "parallel",
            },
        },
        "_templates_": [
            {
                "count": 5,
                "model": {
                    "SomeEntity": {
                        "Node1": "{auto_increment}",
                    },
                },
            },
            {
                "count": 6,
                "model": {
                    "SomeChildEntity": {
                        "Parent": "{parent}",
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
            <refs>
                <parent>
                    <context>SomeEntity</context>
                    <field>Node1</field>
                    <type>parallel</type>
                </parent>
            </refs>
            <_templates_>
                <_template_>
                    <count>5</count>
                    <model>
                        <SomeEntity>
                            <Node1>{auto_increment}</Node1>
                        </SomeEntity>
                    </model>
                </_template_>
                <_template_>
                    <count>6</count>
                    <model>
                        <SomeChildEntity>
                            <Parent>{parent}</Parent>
                        </SomeChildEntity>
                    </model>
                </_template_>
            </_templates_>
        </mimeo_configuration>
    """)

    @assert_throws(err_type=NoCorrespondingReferenceError,
                   msg="No corresponding reference [{ref}] for the iteration [{iter}].",
                   ref="parent",
                   iter=6)
    def _test(
            config: MimeoConfig,
    ):
        with MimeoContextManager(config):
            generator = JSONGenerator(config)
            for _ in generator.generate(config.templates):
                pass

    _test(config_from_dict)
    _test(config_from_xml)
