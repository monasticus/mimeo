import pytest

import tests as test_utils
from mimeo.utils import MimeoUtil


class ValidMimeoUtil(MimeoUtil):

    KEY = "invalid_mimeo_util"

    def render(self):
        pass


class InvalidMimeoUtilWithoutKey(MimeoUtil):

    def render(self):
        pass


class InvalidMimeoUtilWithKeyMethod(MimeoUtil):

    def KEY(self):
        pass

    def render(self):
        pass


class InvalidMimeoUtilWithoutRender(MimeoUtil):

    KEY = "invalid_mimeo_util"


class InvalidMimeoUtilWithoutKeyAndRender(MimeoUtil):
    pass


def test_issubclass_true():
    assert issubclass(ValidMimeoUtil, MimeoUtil)


def test_issubclass_false():
    assert not issubclass(InvalidMimeoUtilWithoutKey, MimeoUtil)
    assert not issubclass(InvalidMimeoUtilWithKeyMethod, MimeoUtil)
    assert not issubclass(InvalidMimeoUtilWithoutRender, MimeoUtil)
    assert not issubclass(InvalidMimeoUtilWithoutKeyAndRender, MimeoUtil)


def test_valid_class_instantiation():
    try:
        ValidMimeoUtil()
        assert True
    except TypeError:
        assert False


def test_invalid_class_instantiation():
    with pytest.raises(TypeError) as err:
        InvalidMimeoUtilWithoutRender()

    assert err.value.args[0] == test_utils.get_class_impl_error_msg("InvalidMimeoUtilWithoutRender", ["render"])
