from datetime import datetime, timedelta

from mimeo.utils.renderers import UtilsRenderer


def test_date_time_raw():
    date_time_value = UtilsRenderer.render_raw("date_time")
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def test_date_time_parametrized_default():
    mimeo_util = {"_name": "date_time"}
    date_time_value = UtilsRenderer.render_parametrized(mimeo_util)
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def test_date_time_parametrized_custom():
    mimeo_util = {
        "_name": "date_time",
        "days_delta": 1,
        "hours_delta": 2,
        "minutes_delta": -3,
        "seconds_delta": 5,
    }
    date_time_value = UtilsRenderer.render_parametrized(mimeo_util)
    delta = timedelta(days=1, hours=2, minutes=-3, seconds=5)
    expected_date_time_value = datetime.now() + delta
    assert date_time_value == expected_date_time_value.strftime("%Y-%m-%dT%H:%M:%S")
