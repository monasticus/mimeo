from mimeo.context import MimeoIteration
from mimeo.context.exc import (InvalidSpecialFieldName,
                               InvalidSpecialFieldValue, SpecialFieldNotFound)
from tests.utils import assert_throws


def test_iteration_id():
    assert MimeoIteration(1).id == 1
    assert MimeoIteration(2).id == 2
    assert MimeoIteration(3).id == 3


def test_iteration_key():
    key1 = MimeoIteration(1).key
    key2 = MimeoIteration(1).key
    key3 = MimeoIteration(1).key

    assert key1 != key2
    assert key2 != key3
    assert key3 != key1


def test_iteration_special_fields():
    iteration = MimeoIteration(1)
    iteration.add_special_field("SomeField1", 1)
    iteration.add_special_field("SomeField2", "value")
    iteration.add_special_field("SomeField3", True)

    assert iteration.get_special_field("SomeField1") == 1
    assert iteration.get_special_field("SomeField2") == "value"
    assert iteration.get_special_field("SomeField3") is True


@assert_throws(err_type=InvalidSpecialFieldName,
               message="A special field name needs to be a string value!")
def test_iteration_add_special_field_not_allowed_name():
    iteration = MimeoIteration(1)
    iteration.add_special_field(1, 1)


@assert_throws(err_type=InvalidSpecialFieldValue,
               message="Provided field value [{val}] is invalid (use any atomic value)!",
               params={"val": "{}"})
def test_iteration_add_special_field_not_allowed_values():
    iteration = MimeoIteration(1)
    iteration.add_special_field("SomeField", {})


@assert_throws(err_type=InvalidSpecialFieldValue,
               message="Provided field value [{val}] is invalid (use any atomic value)!",
               params={"val": "[]"})
def test_iteration_add_special_field_not_allowed_values():
    iteration = MimeoIteration(1)
    iteration.add_special_field("SomeField", [])


@assert_throws(err_type=SpecialFieldNotFound,
               message="Special Field [{field}] has not been found!",
               params={"field": "SomeField"})
def test_iteration_get_special_field_not_found():
    iteration = MimeoIteration(1)
    iteration.get_special_field("SomeField")
