import pytest

from mimeo.config.mimeo_config import MimeoTemplate
from mimeo.config.exc import IncorrectMimeoTemplate


def test_str():
    template = {
      "count": 30,
      "model": {
        "SomeEntity": {
          "ChildNode": "value"
        }
      }
    }

    mimeo_template = MimeoTemplate(template)
    assert str(mimeo_template) == str(template)


def test_parsing_template():
    template = {
      "count": 30,
      "model": {
        "SomeEntity": {
          "ChildNode": "value"
        }
      }
    }

    mimeo_template = MimeoTemplate(template)
    assert mimeo_template.count == 30
    assert mimeo_template.model.root_name == "SomeEntity"
    assert mimeo_template.model.root_data == {
        "ChildNode": "value"
    }


def test_parsing_template_without_count():
    template = {
      "model": {
        "SomeEntity": {
          "ChildNode": "value"
        }
      }
    }

    with pytest.raises(IncorrectMimeoTemplate) as err:
        MimeoTemplate(template)

    assert err.value.args[0] == "No count value in the Mimeo Template: " \
                                "{'model': {'SomeEntity': {'ChildNode': 'value'}}}"


def test_parsing_template_with_multiple_roots():
    template = {
      "count": 30
    }

    with pytest.raises(IncorrectMimeoTemplate) as err:
        MimeoTemplate(template)

    assert err.value.args[0] == "No model data in the Mimeo Template: " \
                                "{'count': 30}"
