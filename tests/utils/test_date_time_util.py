from datetime import datetime, timedelta

from mimeo.utils import UtilsRenderer


def test_date_time_raw():
    date_time_value = UtilsRenderer.render_raw("date_time")
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def test_date_time_parametrized_default():
    date_time_value = UtilsRenderer.render_parametrized({"_name": "date_time"})
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def test_date_time_parametrized_custom():
    date_time_value = UtilsRenderer.render_parametrized({
        "_name": "date_time",
        "days_delta": 1,
        "hours_delta": 2,
        "minutes_delta": -3,
        "seconds_delta": 5,
    })
    expected_date_time_value = datetime.now() + timedelta(days=1, hours=2, minutes=-3, seconds=5)
    assert date_time_value == expected_date_time_value.strftime("%Y-%m-%dT%H:%M:%S")
