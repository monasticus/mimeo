import pytest

from mimeo.config import MimeoConfig
from mimeo.context import MimeoContext, MimeoContextManager
from mimeo.context.annotations import mimeo_context, mimeo_next_iteration


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
    def iteration(self):
        curr_iter = MimeoContextManager().get_current_context().curr_iteration().id
        return curr_iter * curr_iter


def test_mimeo_next_iteration(default_config):
    provider = ContextIterationProvider()
    with MimeoContextManager(default_config) as mimeo_manager:
        context1 = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context1)

        assert provider.iteration() == 1
        assert provider.iteration() == 4
        assert provider.iteration() == 9
