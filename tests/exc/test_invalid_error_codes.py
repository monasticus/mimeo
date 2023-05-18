from mimeo.utils.exc import InvalidMimeoUtilError, InvalidValueError
from tests.utils import assert_throws


@assert_throws(err_type=ValueError,
               msg="Provided error code is not a InvalidMimeoUtilError.Code enum!")
def test_invalid_mimeo_util_error_code():
    raise InvalidMimeoUtilError("UNSUPPORTED_MIMEO_UTIL", "unsupported_util")


@assert_throws(err_type=ValueError,
               msg="Provided error code is not a InvalidValueError.Code enum!")
def test_invalid_value_error_code():
    raise InvalidValueError("NEGATIVE_LENGTH", length=-1)
