import pytest

from mimeo.exceptions import NotAllowedInstantiation
from mimeo.generators import GeneratorUtils


@pytest.fixture
def default_generator_utils():
    return GeneratorUtils.get_for_context("SomeEntity")


@pytest.fixture(autouse=True)
def setup(default_generator_utils):
    # Setup
    default_generator_utils.reset()
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


def test_generator_utils_reset(default_generator_utils):
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"
    identifier = default_generator_utils.auto_increment()
    assert identifier == "00002"

    default_generator_utils.reset()

    identifier = default_generator_utils.auto_increment()
    assert identifier == "00001"
