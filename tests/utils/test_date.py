from datetime import date, timedelta

from mimeo.utils import MimeoUtilRenderer


def test_date_raw():
    date_value = MimeoUtilRenderer.render_raw("date")
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_date_parametrized_default():
    date_value = MimeoUtilRenderer.render_parametrized({"name": "date"})
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_date_parametrized_with_positive_days_delta():
    date_value = MimeoUtilRenderer.render_parametrized({"name": "date", "days_delta": 5})
    expected_date_value = date.today() + timedelta(5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_date_parametrized_with_negative_days_delta():
    date_value = MimeoUtilRenderer.render_parametrized({"name": "date", "days_delta": -5})
    expected_date_value = date.today() + timedelta(-5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")
