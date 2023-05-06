from mimeo.config.exc import InvalidMimeoTemplate
from mimeo.config.mimeo_config import MimeoTemplate
from tests.utils import assert_throws


def test_str():
    template = {
      "count": 30,
      "model": {
        "SomeEntity": {
          "ChildNode": "value",
        },
      },
    }

    mimeo_template = MimeoTemplate(template)
    assert str(mimeo_template) == str(template)


def test_parsing_template():
    template = {
      "count": 30,
      "model": {
        "SomeEntity": {
          "ChildNode": "value",
        },
      },
    }

    mimeo_template = MimeoTemplate(template)
    assert mimeo_template.count == 30
    assert mimeo_template.model.root_name == "SomeEntity"
    assert mimeo_template.model.root_data == {
        "ChildNode": "value",
    }


@assert_throws(err_type=InvalidMimeoTemplate,
               msg="No count value in the Mimeo Template: {tmplt}",
               params={"tmplt": "{'model': {'SomeEntity': {'ChildNode': 'value'}}}"})
def test_parsing_template_without_count():
    template = {
      "model": {
        "SomeEntity": {
          "ChildNode": "value",
        },
      },
    }
    MimeoTemplate(template)


@assert_throws(err_type=InvalidMimeoTemplate,
               msg="No model data in the Mimeo Template: {tmplt}",
               params={"tmplt": "{'count': 30}"})
def test_parsing_template_with_multiple_roots():
    template = {
      "count": 30,
    }
    MimeoTemplate(template)
