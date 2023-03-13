import pytest

from mimeo.config.mimeo_config import MimeoTemplate
from mimeo.generators import Generator, GeneratorUtils


class GeneratorImpl(Generator):

    def generate(self, templates, parent=None):
        pass

    def stringify(self, data, mimeo_config):
        pass


@pytest.fixture
def mimeo_template():
    template = {
      "count": 30,
      "model": {
        "SomeEntity": {
          "ChildNode": "value"
        }
      }
    }

    return MimeoTemplate(template)


@pytest.fixture(autouse=True)
def setup():
    # Setup
    GeneratorUtils.get_for_context("SomeEntity").reset()
    yield


def test_get_str_value(mimeo_template):
    value = GeneratorImpl._get_value("str-value", mimeo_template)
    assert value == "str-value"


def test_get_int_value(mimeo_template):
    value = GeneratorImpl._get_value(1, mimeo_template)
    assert value == "1"


def test_get_bool_value(mimeo_template):
    value = GeneratorImpl._get_value(True, mimeo_template)
    assert value == "true"


def test_get_value_imitating_python_code(mimeo_template):
    value = GeneratorImpl._get_value("{'str-value'.upper()}", mimeo_template)
    assert value == "{'str-value'.upper()}"


def test_get_value_imitating_python_code2(mimeo_template):
    value = GeneratorImpl._get_value("{print()}", mimeo_template)
    assert value == "{print()}"


def test_get_value_using_generator_utils_default(mimeo_template):
    value = GeneratorImpl._get_value("{auto_increment()}", mimeo_template)
    assert value == "00001"


def test_get_value_using_generator_utils_customized(mimeo_template):
    value = GeneratorImpl._get_value("{auto_increment('MYID{}')}", mimeo_template)
    assert value == "MYID1"
