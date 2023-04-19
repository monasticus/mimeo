import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContextManager
from mimeo.context.decorators import (mimeo_clear_iterations,
                                      mimeo_next_iteration)


@pytest.fixture(autouse=True)
def default_config():
    return MimeoConfig({
        "_templates_": [
            {
                "count": 10,
                "model": {
                    "SomeEntity": {
                        "ChildNode1": 1,
                        "ChildNode2": "value-2",
                        "ChildNode3": True
                    }
                }
            }
        ]
    })


class ContextIterationProvider:

    @mimeo_next_iteration
    def pow_iter(self):
        curr_iter = MimeoContextManager().get_current_context().curr_iteration().id
        return curr_iter * curr_iter

    @mimeo_clear_iterations
    @mimeo_next_iteration
    def pow_iter_from_scratch(self):
        curr_iter = MimeoContextManager().get_current_context().curr_iteration().id
        return curr_iter * curr_iter


def test_mimeo_next_iteration(default_config):
    provider = ContextIterationProvider()
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context1)

        assert provider.pow_iter() == 1
        assert provider.pow_iter() == 4
        assert provider.pow_iter() == 9


def test_mimeo_clear_iterations(default_config):
    provider = ContextIterationProvider()
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context1)

        assert provider.pow_iter() == 1
        assert provider.pow_iter() == 4
        assert provider.pow_iter_from_scratch() == 1
        assert provider.pow_iter() == 4
        assert provider.pow_iter() == 9
