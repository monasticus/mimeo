from typing import Optional

import pytest

from mimeo.config import MimeoConfigFactory
from mimeo.context import MimeoContext, MimeoContextManager
from mimeo.context.decorators import mimeo_context


@pytest.fixture(autouse=True)
def default_config():
    return MimeoConfigFactory.parse({
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True,
                    },
                },
            },
        ],
    })


class ContextNameProvider:

    @mimeo_context
    def context_name(self, context: Optional[MimeoContext] = None):
        return context.name


def test_injected_context(default_config):
    provider = ContextNameProvider()
    with MimeoContextManager(default_config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        assert provider.context_name() == "SomeContext"


def test_passed_context(default_config):
    provider = ContextNameProvider()
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context1)

        context2 = mimeo_manager.get_context("SomeOtherContext")
        assert provider.context_name(context2) == "SomeOtherContext"


def test_passed_named_context(default_config):
    provider = ContextNameProvider()
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context1)

        context2 = mimeo_manager.get_context("SomeOtherContext")
        assert provider.context_name(context=context2) == "SomeOtherContext"
