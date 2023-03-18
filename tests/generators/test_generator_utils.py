from datetime import date, datetime, timedelta

import pytest

from mimeo.config import MimeoConfig
from mimeo.exceptions import (InvalidSpecialFieldValue,
                              NotAllowedInstantiation, NotASpecialField)
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


def test_direct_instantiation():
    with pytest.raises(NotAllowedInstantiation) as err:
        GeneratorUtils("some_hardcoded_key")

    assert err.value.args[0] == "GeneratorUtils cannot be instantiated directly! " \
                                "Please use GeneratorUtils.get_for_context(context)"


def test_render_value_str_value(default_context):
    value = GeneratorUtils.render_value(default_context, "str-value")
    assert value == "str-value"


def test_render_value_int_value(default_context):
    value = GeneratorUtils.render_value(default_context, 1)
    assert value == "1"


def test_render_value_bool_value(default_context):
    value = GeneratorUtils.render_value(default_context, True)
    assert value == "true"


def test_render_value_value_imitating_python_code(default_context):
    value = GeneratorUtils.render_value(default_context, "{'str-value'.upper()}")
    assert value == "{'str-value'.upper()}"


def test_render_value_value_imitating_python_code2(default_context):
    value = GeneratorUtils.render_value(default_context, "{print()}")
    assert value == "{print()}"


def test_instantiation_for_context():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity")
    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity")
    assert generator_utils1 is generator_utils2


def test_random_str(default_context, default_generator_utils):
    random_str = default_generator_utils.random_str()
    assert isinstance(random_str, str)
    assert len(random_str) == 20

    random_str = GeneratorUtils.render_value(default_context, "{random_str()}")
    assert isinstance(random_str, str)
    assert len(random_str) == 20


def test_random_str_with_customized_length(default_context, default_generator_utils):
    random_str = default_generator_utils.random_str(3)
    assert isinstance(random_str, str)
    assert len(random_str) == 3

    random_str = GeneratorUtils.render_value(default_context, "{random_str(3)}")
    assert isinstance(random_str, str)
    assert len(random_str) == 3


def test_random_int(default_context, default_generator_utils):
    for _ in range(100):
        random_int = default_generator_utils.random_int()
        assert isinstance(random_int, int)
        assert random_int >= 0
        assert random_int < 100

        random_int = GeneratorUtils.render_value(default_context, "{random_int()}")
        assert isinstance(random_int, str)
        assert int(random_int) >= 0
        assert int(random_int) < 100


def test_random_int_with_customized_length(default_context, default_generator_utils):
    for _ in range(100):
        random_int = default_generator_utils.random_int(10)
        assert isinstance(random_int, int)
        assert random_int >= 0
        assert random_int < 10

        random_int = GeneratorUtils.render_value(default_context, "{random_int(10)}")
        assert isinstance(random_int, str)
        assert int(random_int) >= 0
        assert int(random_int) < 10


def test_auto_increment(default_context, default_generator_utils):
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00002"


def test_auto_increment_render_value(default_context, default_generator_utils):
    identifier = GeneratorUtils.render_value(default_context, "{auto_increment()}")
    assert identifier == "00001"
    identifier = GeneratorUtils.render_value(default_context, "{auto_increment()}")
    assert identifier == "00002"


def test_auto_increment_with_customized_format(default_context, default_generator_utils):
    identifier = default_generator_utils.auto_increment("{}")
    assert identifier == "1"
    identifier = default_generator_utils.auto_increment("MYID/{}")
    assert identifier == "MYID/2"
    identifier = default_generator_utils.auto_increment("MYID_{:010d}")
    assert identifier == "MYID_0000000003"


def test_auto_increment_with_customized_format_render_value(default_context, default_generator_utils):
    identifier = GeneratorUtils.render_value(default_context, "{auto_increment('{}')}")
    assert identifier == "1"
    identifier = GeneratorUtils.render_value(default_context, "{auto_increment('MYID/{}')}")
    assert identifier == "MYID/2"
    identifier = GeneratorUtils.render_value(default_context, "{auto_increment('MYID_{:010d}')}")
    assert identifier == "MYID_0000000003"


def test_auto_increment_for_different_context():
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


def test_curr_iter(default_context, default_generator_utils):
    default_generator_utils.setup_iteration(1)
    curr_iter = default_generator_utils.curr_iter()
    assert curr_iter == 1

    default_generator_utils.setup_iteration(2)
    curr_iter = default_generator_utils.curr_iter()
    assert (curr_iter) == 2


def test_curr_iter_render_value(default_context, default_generator_utils):
    default_generator_utils.setup_iteration(1)
    curr_iter = GeneratorUtils.render_value(default_context, "{curr_iter()}")
    assert curr_iter == "1"

    default_generator_utils.setup_iteration(2)
    curr_iter = GeneratorUtils.render_value(default_context, "{curr_iter()}")
    assert curr_iter == "2"


def test_curr_iter_from_different_context():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    generator_utils1.setup_iteration(1)
    curr_iter = generator_utils1.curr_iter()
    assert curr_iter == 1
    generator_utils1.setup_iteration(2)
    curr_iter = generator_utils1.curr_iter()
    assert curr_iter == 2

    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    generator_utils2.setup_iteration(5)
    curr_iter = generator_utils2.curr_iter()
    assert curr_iter == 5

    curr_iter = generator_utils2.curr_iter("SomeEntity1")
    assert curr_iter == 2


def test_key_in_several_iterations(default_context, default_generator_utils):
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


def test_key_in_several_iterations_render_value(default_context, default_generator_utils):
    default_generator_utils.setup_iteration(1)
    key1_1 = GeneratorUtils.render_value(default_context, "{key()}")
    key1_2 = GeneratorUtils.render_value(default_context, "{key()}")

    default_generator_utils.setup_iteration(2)
    key2_1 = GeneratorUtils.render_value(default_context, "{key()}")
    key2_2 = GeneratorUtils.render_value(default_context, "{key()}")

    default_generator_utils.setup_iteration(3)
    key3_1 = GeneratorUtils.render_value(default_context, "{key()}")
    key3_2 = GeneratorUtils.render_value(default_context, "{key()}")

    assert key1_1 == key1_2
    assert key2_1 == key2_2
    assert key3_1 == key3_2
    assert key1_1 != key2_1
    assert key2_1 != key3_1
    assert key3_1 != key1_1


def test_key_in_several_contexts():
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


def test_get_key():
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    generator_utils1.setup_iteration(1)
    key = generator_utils1.key()
    key_outside_context = generator_utils2.get_key("SomeEntity1")

    assert key == key_outside_context


def test_get_key_render_value(default_context, default_generator_utils):
    generator_utils1 = GeneratorUtils.get_for_context("SomeEntity1")
    generator_utils2 = GeneratorUtils.get_for_context("SomeEntity2")
    generator_utils1.setup_iteration(1)
    key = generator_utils1.key()
    key_outside_context = GeneratorUtils.render_value("SomeEntity2", "{get_key('SomeEntity1')}")

    assert key == key_outside_context


def test_get_key_with_customized_iteration():
    generator_utils1 = GeneratorUtils.get_for_context("CustomizedIndex1")
    generator_utils2 = GeneratorUtils.get_for_context("CustomizedIndex2")
    generator_utils1.setup_iteration(1)
    generator_utils1.setup_iteration(2)
    key = generator_utils1.key()
    generator_utils1.setup_iteration(3)
    key_outside_context = generator_utils2.get_key("CustomizedIndex1", 2)

    assert key == key_outside_context


def test_get_key_with_customized_iteration_render_value():
    generator_utils1 = GeneratorUtils.get_for_context("CustomizedIndexEval1")
    generator_utils2 = GeneratorUtils.get_for_context("CustomizedIndexEval2")
    generator_utils1.setup_iteration(1)
    generator_utils1.setup_iteration(2)
    key = generator_utils1.key()
    generator_utils1.setup_iteration(3)
    key_outside_context = GeneratorUtils.render_value("CustomizedIndexEval2", "{get_key('CustomizedIndexEval1', 2)}")

    assert key == key_outside_context


def test_reset(default_generator_utils):
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00002"

    default_generator_utils.reset()

    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"


def test_date(default_context, default_generator_utils):
    date_value = default_generator_utils.date()
    assert date_value == date.today().strftime("%Y-%m-%d")

    date_value = GeneratorUtils.render_value(default_context, "{date()}")
    assert date_value == date.today().strftime("%Y-%m-%d")


def test_date_with_customized_positive_days_delta(default_context, default_generator_utils):
    expected_date_value = date.today() + timedelta(5)

    date_value = default_generator_utils.date(5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")

    date_value = GeneratorUtils.render_value(default_context, "{date(5)}")
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_date_with_customized_negative_days_delta(default_context, default_generator_utils):
    expected_date_value = date.today() + timedelta(days=-5)

    date_value = default_generator_utils.date(-5)
    assert date_value == expected_date_value.strftime("%Y-%m-%d")

    date_value = GeneratorUtils.render_value(default_context, "{date(-5)}")
    assert date_value == expected_date_value.strftime("%Y-%m-%d")


def test_date_time(default_context, default_generator_utils):
    date_time_value = default_generator_utils.date_time()
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    date_time_value = GeneratorUtils.render_value(default_context, "{date_time()}")
    assert date_time_value == datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def test_date_time_with_timedelta(default_context, default_generator_utils):
    expected_date_time_value = datetime.now() + timedelta(days=1, hours=2, minutes=-3, seconds=5)

    date_time_value = default_generator_utils.date_time(1, 2, -3, 5)
    assert date_time_value == expected_date_time_value.strftime("%Y-%m-%dT%H:%M:%S")

    date_time_value = GeneratorUtils.render_value(default_context, "{date_time(1, 2, -3, 5)}")
    assert date_time_value == expected_date_time_value.strftime("%Y-%m-%dT%H:%M:%S")


def test_vars_str():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "custom-value-1"
        },
        "_templates_": []
    })
    GeneratorUtils.setup(config)
    value = GeneratorUtils.render_value("SomeEntity", "{CUSTOM_VAR_1}")
    assert value == "custom-value-1"


def test_vars_int():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": 1
        },
        "_templates_": []
    })
    GeneratorUtils.setup(config)
    value = GeneratorUtils.render_value("SomeEntity", "{CUSTOM_VAR_1}")
    assert value == "1"


def test_vars_bool():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": True
        },
        "_templates_": []
    })
    GeneratorUtils.setup(config)
    value = GeneratorUtils.render_value("SomeEntity", "{CUSTOM_VAR_1}")
    assert value == "true"


def test_vars_pointing_to_var():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "custom-value-1",
            "CUSTOM_VAR_2": "{CUSTOM_VAR_1}"
        },
        "_templates_": []
    })
    GeneratorUtils.setup(config)
    value = GeneratorUtils.render_value("SomeEntity", "{CUSTOM_VAR_2}")
    assert value == "custom-value-1"


def test_vars_pointing_to_non_existing_var():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "{NON_EXISTING_VAR}"
        },
        "_templates_": []
    })
    GeneratorUtils.setup(config)
    value = GeneratorUtils.render_value("SomeEntity", "{CUSTOM_VAR_1}")
    assert value == "{NON_EXISTING_VAR}"


def test_vars_pointing_to_funct():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "{auto_increment('{}')}"
        },
        "_templates_": []
    })
    GeneratorUtils.setup(config)
    value = GeneratorUtils.render_value("SomeEntity", "{CUSTOM_VAR_1}")
    assert value == "1"


def test_vars_pointing_to_invalid_funct():
    config = MimeoConfig({
        "vars": {
            "CUSTOM_VAR_1": "{auto_increment(1)}"
        },
        "_templates_": []
    })
    GeneratorUtils.setup(config)
    value = GeneratorUtils.render_value("SomeEntity", "{auto_increment(1)}")
    assert value == "{auto_increment(1)}"


def test_is_special_field_true():
    assert GeneratorUtils.is_special_field("{:SomeChild:}")
    assert GeneratorUtils.is_special_field("{:Some_Child:}")
    assert GeneratorUtils.is_special_field("{:Some-Child:}")
    assert GeneratorUtils.is_special_field("{:SomeChild1:}")


def test_is_special_field_false():
    assert not GeneratorUtils.is_special_field(":SomeField:}")
    assert not GeneratorUtils.is_special_field("{:SomeField:")
    assert not GeneratorUtils.is_special_field("{SomeField:}")
    assert not GeneratorUtils.is_special_field("{:SomeField}")
    assert not GeneratorUtils.is_special_field("SomeField:}")
    assert not GeneratorUtils.is_special_field("{:SomeField")
    assert not GeneratorUtils.is_special_field("{SomeField}")
    assert not GeneratorUtils.is_special_field(":SomeField:")
    assert not GeneratorUtils.is_special_field("SomeField")
    assert not GeneratorUtils.is_special_field("{::}")
    assert not GeneratorUtils.is_special_field("{:Some Field:}")


def test_get_special_field_name():
    assert GeneratorUtils.get_special_field_name("{:SomeField:}") == "SomeField"


def test_get_special_field_name_when_invalid():
    with pytest.raises(NotASpecialField) as err:
        GeneratorUtils.get_special_field_name("{:SomeField}")

    assert err.value.args[0] == "Provided field [{:SomeField}] is not a special one (use {:NAME:})!"


def test_provide_not_special_field(default_generator_utils):
    with pytest.raises(NotASpecialField) as err:
        default_generator_utils.provide("{SomeField}", "custom-value")

    assert err.value.args[0] == "Provided field [{SomeField}] is not a special one (use {:NAME:})!"


def test_provide_invalid_special_field_value(default_generator_utils):
    with pytest.raises(InvalidSpecialFieldValue) as err:
        default_generator_utils.provide("{:SomeField:}", {})

    assert err.value.args[0] == "Provided field value [{}] is invalid (use any atomic value)!"

    with pytest.raises(InvalidSpecialFieldValue) as err:
        default_generator_utils.provide("{:SomeField:}", [])

    assert err.value.args[0] == "Provided field value [[]] is invalid (use any atomic value)!"


def test_inject_not_special_field(default_generator_utils):
    with pytest.raises(NotASpecialField) as err:
        default_generator_utils.inject("{:SomeNotSpecialField:}")

    assert err.value.args[0] == "There's no such a special field [SomeNotSpecialField]!"


def test_provide_and_inject_str(default_generator_utils):
    field_name = default_generator_utils.provide("{:SomeField:}", "custom-value")
    assert field_name == "SomeField"

    field_value = default_generator_utils.inject("{:SomeField:}")
    assert field_value == "custom-value"


def test_provide_and_inject_int(default_generator_utils):
    field_name = default_generator_utils.provide("{:SomeField:}", 1)
    assert field_name == "SomeField"

    field_value = default_generator_utils.inject("{:SomeField:}")
    assert field_value == 1


def test_provide_and_inject_bool(default_generator_utils):
    field_name = default_generator_utils.provide("{:SomeField:}", True)
    assert field_name == "SomeField"

    field_value = default_generator_utils.inject("{:SomeField:}")
    assert field_value is True


def test_not_allowed_functions():
    to_render = "{setup(MimeoConfig({'_templates_':[]}))}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render

    to_render = "{reset()}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render

    to_render = "{setup_iteration(1)}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render

    to_render = "{render_value(auto_increment())}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render

    to_render = "{is_special_field()}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render

    to_render = "{get_special_field_name()}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render

    to_render = "{provide()}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render

    to_render = "{inject()}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render

    to_render = "{key('non-existing-parameter')}"
    value = GeneratorUtils.render_value("SomeEntity", to_render)
    assert value == to_render
