import pytest
from datetime import date, datetime, timedelta

from mimeo.exceptions import NotAllowedInstantiation
from mimeo.generators import GeneratorUtils


@pytest.fixture
def default_generator_utils() -> GeneratorUtils:
    return GeneratorUtils.get_for_context("SomeEntity")


@pytest.fixture(autouse=True)
def setup(default_generator_utils):
    # Setup
    default_generator_utils.reset()
    default_generator_utils.set_curr_iter(0)
    yield


def test_generator_utils_direct_instantiation():
    with pytest.raises(NotAllowedInstantiation) as err:
        GeneratorUtils("some_hardcoded_key")

    assert err.value.args[0] == "GeneratorUtils cannot be instantiated directly! " \
                                "Please use GeneratorUtils.get_for_context(context)"


def test_generator_utils_instantiation_for_context():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity")
    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity")
    assert generator_utils1 is generator_utils2


def test_generator_utils_random_str(default_generator_utils):
    random_str = default_generator_utils.random_str()
    assert isinstance(random_str, str)
    assert len(random_str) == 20


def test_generator_utils_random_str_with_customized_length(default_generator_utils):
    random_str = default_generator_utils.random_str(3)
    assert isinstance(random_str, str)
    assert len(random_str) == 3


def test_generator_utils_random_int(default_generator_utils):
    random_int = default_generator_utils.random_int()
    assert isinstance(random_int, str)
    assert len(random_int) == 1


def test_generator_utils_random_int_with_customized_length(default_generator_utils):
    random_int = default_generator_utils.random_int(10)
    assert isinstance(random_int, str)
    assert len(random_int) == 10


def test_generator_utils_auto_increment(default_generator_utils):
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00002"


def test_generator_utils_auto_increment_with_customized_format(default_generator_utils):
    identifier = default_generator_utils.auto_increment("{}")
    assert identifier == "1"
    identifier = default_generator_utils.auto_increment("MYID/{}")
    assert identifier == "MYID/2"
    identifier = default_generator_utils.auto_increment("MYID_{:010d}")
    assert identifier == "MYID_0000000003"


def test_generator_utils_auto_increment_for_different_context():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    identifier = generator_utils1.auto_increment()
    assert identifier == "00001"
    identifier = generator_utils1.auto_increment()
    assert identifier == "00002"

    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    identifier = generator_utils2.auto_increment()
    assert identifier == "00001"
    identifier = generator_utils2.auto_increment()
    assert identifier == "00002"


def test_generator_utils_curr_iter(default_generator_utils):
    default_generator_utils.set_curr_iter(1)
    curr_iter = default_generator_utils.curr_iter()
    assert curr_iter == "1"

    default_generator_utils.set_curr_iter(2)
    curr_iter = default_generator_utils.curr_iter()
    assert curr_iter == "2"


def test_generator_utils_curr_iter_from_different_context():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    generator_utils1.set_curr_iter(1)
    curr_iter = generator_utils1.curr_iter()
    assert curr_iter == "1"
    generator_utils1.set_curr_iter(2)
    curr_iter = generator_utils1.curr_iter()
    assert curr_iter == "2"

    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    generator_utils2.set_curr_iter(5)
    curr_iter = generator_utils2.curr_iter()
    assert curr_iter == "5"

    curr_iter = generator_utils2.curr_iter("SomeEntity1")
    assert curr_iter == "2"


def test_generator_utils_reset(default_generator_utils):
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00002"

    default_generator_utils.reset()

    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"


def test_generator_utils_date(default_generator_utils):
    date_value = default_generator_utils.date()
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_generator_utils_date_with_customized_positive_days_delta(default_generator_utils):
    date_value = default_generator_utils.date(5)
    expected_date_value = date.today() + timedelta(5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_generator_utils_date_with_customized_negative_days_delta(default_generator_utils):
    date_value = default_generator_utils.date(-5)
    expected_date_value = date.today() + timedelta(days=-5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_generator_utils_date_time(default_generator_utils):
    date_time_value = default_generator_utils.date_time()
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def test_generator_utils_date_time_with_timedelta(default_generator_utils):
    date_time_value = default_generator_utils.date_time(1, 2, -3, 5)
    expected_date_time_value = datetime.now() + timedelta(days=1, hours=2, minutes=-3, seconds=5)
    assert date_time_value == expected_date_time_value.strftime("%Y-%m-%dT%H:%M:%S")
