from datetime import date, timedelta

from mimeo.utils.renderers import UtilsRenderer


def test_date_raw():
    date_value = UtilsRenderer.render_raw("date")
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_date_parametrized_default():
    mimeo_util = {"_name": "date"}
    date_value = UtilsRenderer.render_parametrized(mimeo_util)
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_date_parametrized_with_positive_days_delta():
    mimeo_util = {"_name": "date", "days_delta": 5}
    date_value = UtilsRenderer.render_parametrized(mimeo_util)
    expected_date_value = date.today() + timedelta(5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_date_parametrized_with_negative_days_delta():
    mimeo_util = {"_name": "date", "days_delta": -5}
    date_value = UtilsRenderer.render_parametrized(mimeo_util)
    expected_date_value = date.today() + timedelta(-5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")
