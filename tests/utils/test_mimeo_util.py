
import tests.utils as test_utils
from mimeo.utils import MimeoUtil
from tests.utils import assert_throws


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
        raise AssertionError() from TypeError


@assert_throws(err_type=TypeError,
               message=test_utils.get_class_impl_error_msg(
                   "InvalidMimeoUtilWithoutRender",
                   ["render"],
               ))
def test_invalid_class_instantiation():
    InvalidMimeoUtilWithoutRender()
