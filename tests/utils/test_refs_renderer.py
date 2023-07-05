from mimeo.config import MimeoConfigFactory
from mimeo.context import MimeoContextManager
from mimeo.utils.renderers import RefsRenderer


def test_ref_any():
    config = MimeoConfigFactory.parse({
        "refs": {
            "custom_ref_any": {
                "context": "SomeContext",
                "field": "ChildNode",
                "type": "any",
            },
            "custom_ref_parallel": {
                "context": "SomeContext",
                "field": "ChildNode",
                "type": "parallel",
            },
        },
        "_templates_": [],
    })
    with MimeoContextManager(config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)

        mimeo_manager.cache_ref("ChildNode", 1)
        mimeo_manager.cache_ref("ChildNode", 2)
        mimeo_manager.cache_ref("ChildNode", 3)
        assert RefsRenderer.render("custom_ref_any") in [1, 2, 3]


def test_ref_parallel():
    config = MimeoConfigFactory.parse({
        "refs": {
            "custom_ref_any": {
                "context": "SomeContext",
                "field": "ChildNode",
                "type": "any",
            },
            "custom_ref_parallel": {
                "context": "SomeContext",
                "field": "ChildNode",
                "type": "parallel",
            },
        },
        "_templates_": [],
    })
    with MimeoContextManager(config) as mimeo_manager:
        context = mimeo_manager.get_context("SomeContext")
        mimeo_manager.set_current_context(context)
        context.next_iteration()
        mimeo_manager.cache_ref("ChildNode", 1)
        assert RefsRenderer.render("custom_ref_parallel") == 1
        assert RefsRenderer.render("custom_ref_parallel") == 1

        context.next_iteration()
        mimeo_manager.cache_ref("ChildNode", 2)
        assert RefsRenderer.render("custom_ref_parallel") == 2
        assert RefsRenderer.render("custom_ref_parallel") == 2

        context.next_iteration()
        mimeo_manager.cache_ref("ChildNode", 3)
        assert RefsRenderer.render("custom_ref_parallel") == 3
        assert RefsRenderer.render("custom_ref_parallel") == 3


