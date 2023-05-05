from mimeo.utils.renderers import UtilsRenderer


def test_random_item_raw():
    random_item = UtilsRenderer.render_raw("random_item")
    assert random_item == ""


def test_random_item_parametrized_default():
    mimeo_util = {"_name": "random_item"}
    random_item = UtilsRenderer.render_parametrized(mimeo_util)
    assert random_item == ""


def test_random_item_parametrized_with_empty_items():
    mimeo_util = {"_name": "random_item", "items": []}
    random_item = UtilsRenderer.render_parametrized(mimeo_util)
    assert random_item == ""


def test_random_item_parametrized_with_non_empty_items():
    items = ['a', 1, True]
    mimeo_util = {"_name": "random_item", "items": items}
    for _ in range(100):
        random_item = UtilsRenderer.render_parametrized(mimeo_util)
        assert random_item in items
