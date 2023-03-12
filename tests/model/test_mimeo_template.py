import pytest

from mimeo.model.exceptions import IncorrectMimeoTemplate
from mimeo.model.mimeo_config import MimeoTemplate


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
    assert mimeo_template.model.attributes == {}
    assert mimeo_template.model.root_name == "SomeEntity"
    assert mimeo_template.model.root_data == {
        "ChildNode": "value"
    }


def test_parsing_model_without_count():
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


def test_parsing_model_with_multiple_roots():
    template = {
      "count": 30
    }

    with pytest.raises(IncorrectMimeoTemplate) as err:
        MimeoTemplate(template)

    assert err.value.args[0] == "No model data in the Mimeo Template: " \
                                "{'count': 30}"
