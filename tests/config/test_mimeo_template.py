from mimeo.config.exc import InvalidMimeoTemplateError
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


@assert_throws(err_type=InvalidMimeoTemplateError,
               msg="No count property in the Mimeo Template: {tmplt}",
               tmplt="{'model': {'SomeEntity': {'ChildNode': 'value'}}}")
def test_parsing_template_without_count():
    template = {
      "model": {
        "SomeEntity": {
          "ChildNode": "value",
        },
      },
    }
    MimeoTemplate(template)


@assert_throws(err_type=InvalidMimeoTemplateError,
               msg="No model property in the Mimeo Template: {tmplt}",
               tmplt="{'count': 30}")
def test_parsing_template_with_multiple_roots():
    template = {
      "count": 30,
    }
    MimeoTemplate(template)
