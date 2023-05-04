from mimeo.utils.renderers import UtilsRenderer


def test_random_item_raw():
    random_item = UtilsRenderer.render_raw("random_item")
    assert random_item == ""


def test_random_item_parametrized_default():
    random_item = UtilsRenderer.render_parametrized({"_name": "random_item"})
    assert random_item == ""


def test_random_item_parametrized_with_empty_items():
    random_item = UtilsRenderer.render_parametrized({"_name": "random_item", "items": []})
    assert random_item == ""


def test_random_item_parametrized_with_non_empty_items():
    items = ['a', 1, True]
    for _ in range(100):
        random_item = UtilsRenderer.render_parametrized({"_name": "random_item", "items": items})
        assert random_item in items
