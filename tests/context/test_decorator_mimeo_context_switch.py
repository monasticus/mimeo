import pytest

from mimeo.config import MimeoConfig
from mimeo.config.mimeo_config import MimeoTemplate
from mimeo.context import MimeoContextManager
from mimeo.context.decorators import mimeo_context_switch


@pytest.fixture(autouse=True)
def default_config():
    return MimeoConfig({
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": {
                            "_templates_": [
                                {
                                    "count": 10,
                                    "model": {
                                        "GrandChild": {
                                            "_templates_": [
                                                {
                                                    "count": 10,
                                                    "model": {
                                                        "Details": {
                                                            "Detail1": 1,
                                                            "Detail2": "value-2",
                                                            "Detail3": True,
                                                        },
                                                    },
                                                },
                                            ],
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


class ContextBucket:

    CONTEXTS = []

    def reset(self):
        self.CONTEXTS = []

    def collect_contexts(self, template: MimeoTemplate):
        prev_context = MimeoContextManager().get_current_context()
        self.CONTEXTS.append(prev_context if prev_context is None else prev_context.name)

        self.collect_with_switch(template)

        next_context = MimeoContextManager().get_current_context()
        self.CONTEXTS.append(next_context if next_context is None else next_context.name)

    @mimeo_context_switch
    def collect_with_switch(self, template: MimeoTemplate):
        self.__traverse(template.model.root_data)

    def __traverse(self, data: dict):
        for key, value in data.items():
            if key == "_templates_":
                for template in value:
                    self.collect_contexts(MimeoTemplate(template))
            elif isinstance(value, list):
                for item in value:
                    self.__traverse(item)
            elif isinstance(value, dict):
                self.__traverse(value)


def test_context_switch(default_config: MimeoConfig):
    bucket = ContextBucket()
    bucket.reset()
    with MimeoContextManager(default_config):
        for template in default_config.templates:
            bucket.collect_contexts(template)

    assert bucket.CONTEXTS == [
        None,
        "SomeEntity",
        "GrandChild",
        # "Details",  Not present as context are collected before and after switch
        "GrandChild",
        "SomeEntity",
        None,
    ]


def test_context_switch_with_named_param(default_config: MimeoConfig):
    bucket = ContextBucket()
    bucket.reset()
    with MimeoContextManager(default_config):
        for template in default_config.templates:
            bucket.collect_with_switch(template=template)

    print(bucket.CONTEXTS)
    assert bucket.CONTEXTS == [
        # None,       Not present as using annotated function directly in this scenario
        "SomeEntity",
        "GrandChild",
        # "Details",  Not present as context are collected before and after switch
        "GrandChild",
        "SomeEntity",
        # None        Not present as using annotated function directly in this scenario
    ]
