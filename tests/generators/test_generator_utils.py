import pytest
from datetime import date, datetime, timedelta

from mimeo.exceptions import NotAllowedInstantiation, InvalidMimeoUtil
from mimeo.generators import GeneratorUtils


@pytest.fixture
def default_context() -> str:
    return "SomeEntity"


@pytest.fixture
def default_generator_utils(default_context) -> GeneratorUtils:
    return GeneratorUtils.get_for_context(default_context)


@pytest.fixture(autouse=True)
def setup(default_generator_utils):
    # Setup
    default_generator_utils.reset()
    default_generator_utils.setup_iteration(0)
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


def test_generator_utils_random_str(default_context, default_generator_utils):
    random_str = default_generator_utils.random_str()
    assert isinstance(random_str, str)
    assert len(random_str) == 20

    random_str = GeneratorUtils.eval(default_context, "random_str()")
    assert isinstance(random_str, str)
    assert len(random_str) == 20


def test_generator_utils_random_str_with_customized_length(default_context, default_generator_utils):
    random_str = default_generator_utils.random_str(3)
    assert isinstance(random_str, str)
    assert len(random_str) == 3

    random_str = GeneratorUtils.eval(default_context, "random_str(3)")
    assert isinstance(random_str, str)
    assert len(random_str) == 3


def test_generator_utils_random_int(default_context, default_generator_utils):
    random_int = default_generator_utils.random_int()
    assert isinstance(random_int, str)
    assert len(random_int) == 1

    random_int = GeneratorUtils.eval(default_context, "random_int()")
    assert isinstance(random_int, str)
    assert len(random_int) == 1


def test_generator_utils_random_int_with_customized_length(default_context, default_generator_utils):
    random_int = default_generator_utils.random_int(10)
    assert isinstance(random_int, str)
    assert len(random_int) == 10

    random_int = GeneratorUtils.eval(default_context, "random_int(10)")
    assert isinstance(random_int, str)
    assert len(random_int) == 10


def test_generator_utils_auto_increment(default_context, default_generator_utils):
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00002"


def test_generator_utils_auto_increment_eval(default_context, default_generator_utils):
    identifier = GeneratorUtils.eval(default_context, "auto_increment()")
    assert identifier == "00001"
    identifier = GeneratorUtils.eval(default_context, "auto_increment()")
    assert identifier == "00002"


def test_generator_utils_auto_increment_with_customized_format(default_context, default_generator_utils):
    identifier = default_generator_utils.auto_increment("{}")
    assert identifier == "1"
    identifier = default_generator_utils.auto_increment("MYID/{}")
    assert identifier == "MYID/2"
    identifier = default_generator_utils.auto_increment("MYID_{:010d}")
    assert identifier == "MYID_0000000003"


def test_generator_utils_auto_increment_with_customized_format_eval(default_context, default_generator_utils):
    identifier = GeneratorUtils.eval(default_context, "auto_increment('{}')")
    assert identifier == "1"
    identifier = GeneratorUtils.eval(default_context, "auto_increment('MYID/{}')")
    assert identifier == "MYID/2"
    identifier = GeneratorUtils.eval(default_context, "auto_increment('MYID_{:010d}')")
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


def test_generator_utils_curr_iter(default_context, default_generator_utils):
    default_generator_utils.setup_iteration(1)
    curr_iter = default_generator_utils.curr_iter()
    assert curr_iter == "1"

    default_generator_utils.setup_iteration(2)
    curr_iter = default_generator_utils.curr_iter()
    assert curr_iter == "2"


def test_generator_utils_curr_iter_eval(default_context, default_generator_utils):
    default_generator_utils.setup_iteration(1)
    curr_iter = GeneratorUtils.eval(default_context, "curr_iter()")
    assert curr_iter == "1"

    default_generator_utils.setup_iteration(2)
    curr_iter = GeneratorUtils.eval(default_context, "curr_iter()")
    assert curr_iter == "2"


def test_generator_utils_curr_iter_from_different_context():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    generator_utils1.setup_iteration(1)
    curr_iter = generator_utils1.curr_iter()
    assert curr_iter == "1"
    generator_utils1.setup_iteration(2)
    curr_iter = generator_utils1.curr_iter()
    assert curr_iter == "2"

    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    generator_utils2.setup_iteration(5)
    curr_iter = generator_utils2.curr_iter()
    assert curr_iter == "5"

    curr_iter = generator_utils2.curr_iter("SomeEntity1")
    assert curr_iter == "2"


def test_generator_utils_key_in_several_iterations(default_context, default_generator_utils):
    default_generator_utils.setup_iteration(1)
    key1_1 = default_generator_utils.key()
    key1_2 = default_generator_utils.key()

    default_generator_utils.setup_iteration(2)
    key2_1 = default_generator_utils.key()
    key2_2 = default_generator_utils.key()

    default_generator_utils.setup_iteration(3)
    key3_1 = default_generator_utils.key()
    key3_2 = default_generator_utils.key()

    assert key1_1 == key1_2
    assert key2_1 == key2_2
    assert key3_1 == key3_2
    assert key1_1 != key2_1
    assert key2_1 != key3_1
    assert key3_1 != key1_1


def test_generator_utils_key_in_several_iterations_eval(default_context, default_generator_utils):
    default_generator_utils.setup_iteration(1)
    key1_1 = GeneratorUtils.eval(default_context, "key()")
    key1_2 = GeneratorUtils.eval(default_context, "key()")

    default_generator_utils.setup_iteration(2)
    key2_1 = GeneratorUtils.eval(default_context, "key()")
    key2_2 = GeneratorUtils.eval(default_context, "key()")

    default_generator_utils.setup_iteration(3)
    key3_1 = GeneratorUtils.eval(default_context, "key()")
    key3_2 = GeneratorUtils.eval(default_context, "key()")

    assert key1_1 == key1_2
    assert key2_1 == key2_2
    assert key3_1 == key3_2
    assert key1_1 != key2_1
    assert key2_1 != key3_1
    assert key3_1 != key1_1


def test_generator_utils_key_in_several_contexts():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    generator_utils3 = GeneratorUtils.get_for_context("SomeEntity3")

    generator_utils1.setup_iteration(1)
    generator_utils2.setup_iteration(1)
    generator_utils3.setup_iteration(1)

    key1_1 = generator_utils1.key()
    key1_2 = generator_utils1.key()
    key2_1 = generator_utils2.key()
    key2_2 = generator_utils2.key()
    key3_1 = generator_utils3.key()
    key3_2 = generator_utils3.key()

    assert key1_1 == key1_2
    assert key2_1 == key2_2
    assert key3_1 == key3_2
    assert key1_1 != key2_1
    assert key2_1 != key3_1
    assert key3_1 != key1_1


def test_generator_utils_get_key():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    generator_utils1.setup_iteration(1)
    key = generator_utils1.key()
    key_outside_context = generator_utils2.get_key("SomeEntity1")

    assert key == key_outside_context


def test_generator_utils_get_key_eval(default_context, default_generator_utils):
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    generator_utils1.setup_iteration(1)
    key = generator_utils1.key()
    key_outside_context = GeneratorUtils.eval("SomeEntity2", "get_key('SomeEntity1')")

    assert key == key_outside_context


def test_generator_utils_get_key_with_customized_index():
    generator_utils1 = GeneratorUtils.get_for_context("CustomizedIndex1")
    generator_utils2 = GeneratorUtils.get_for_context("CustomizedIndex2")
    generator_utils1.setup_iteration(1)
    generator_utils1.setup_iteration(2)
    key = generator_utils1.key()
    generator_utils1.setup_iteration(3)
    key_outside_context = generator_utils2.get_key("CustomizedIndex1", 1)

    assert key == key_outside_context


def test_generator_utils_get_key_with_customized_index_eval():
    generator_utils1 = GeneratorUtils.get_for_context("CustomizedIndexEval1")
    generator_utils2 = GeneratorUtils.get_for_context("CustomizedIndexEval2")
    generator_utils1.setup_iteration(1)
    generator_utils1.setup_iteration(2)
    key = generator_utils1.key()
    generator_utils1.setup_iteration(3)
    key_outside_context = GeneratorUtils.eval("CustomizedIndexEval2", "get_key('CustomizedIndexEval1', 1)")

    assert key == key_outside_context


def test_generator_utils_reset(default_generator_utils):
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00002"

    default_generator_utils.reset()

    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"


def test_generator_utils_date(default_context, default_generator_utils):
    date_value = default_generator_utils.date()
    assert date_value == date.today().strftime("%Y-%m-%d")

    date_value = GeneratorUtils.eval(default_context, "date()")
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_generator_utils_date_with_customized_positive_days_delta(default_context, default_generator_utils):
    expected_date_value = date.today() + timedelta(5)

    date_value = default_generator_utils.date(5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")

    date_value = GeneratorUtils.eval(default_context, "date(5)")
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_generator_utils_date_with_customized_negative_days_delta(default_context, default_generator_utils):
    expected_date_value = date.today() + timedelta(days=-5)

    date_value = default_generator_utils.date(-5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")

    date_value = GeneratorUtils.eval(default_context, "date(-5)")
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_generator_utils_date_time(default_context, default_generator_utils):
    date_time_value = default_generator_utils.date_time()
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    date_time_value = GeneratorUtils.eval(default_context, "date_time()")
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def test_generator_utils_date_time_with_timedelta(default_context, default_generator_utils):
    expected_date_time_value = datetime.now() + timedelta(days=1, hours=2, minutes=-3, seconds=5)

    date_time_value = default_generator_utils.date_time(1, 2, -3, 5)
    assert date_time_value == expected_date_time_value.strftime("%Y-%m-%dT%H:%M:%S")

    date_time_value = GeneratorUtils.eval(default_context, "date_time(1, 2, -3, 5)")
    assert date_time_value == expected_date_time_value.strftime("%Y-%m-%dT%H:%M:%S")


def test_generator_utils_not_allowed_functions():
    with pytest.raises(InvalidMimeoUtil) as err:
        GeneratorUtils.eval("SomeEntity", "reset()")

    assert err.value.args[0] == "Provided function [reset()] is invalid!"

    with pytest.raises(InvalidMimeoUtil) as err:
        GeneratorUtils.eval("SomeEntity", "setup_iteration(1)")

    assert err.value.args[0] == "Provided function [setup_iteration(1)] is invalid!"

    with pytest.raises(InvalidMimeoUtil) as err:
        GeneratorUtils.eval("SomeEntity", "eval(auto_increment())")

    assert err.value.args[0] == "Provided function [eval(auto_increment())] is invalid!"

    with pytest.raises(InvalidMimeoUtil) as err:
        GeneratorUtils.eval("SomeEntity", "key('non-existing-parameter')")

    assert err.value.args[0] == "Provided function [key('non-existing-parameter')] is invalid!"
