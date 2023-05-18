from mimeo.utils.exc import InvalidMimeoUtilError
from tests.utils import assert_throws


@assert_throws(err_type=ValueError,
               msg="Provided error code is not a InvalidMimeoUtilError.Code enum!")
def test_invalid_mimeo_util_error_code():
    raise InvalidMimeoUtilError("MISSING_MIMEO_UTIL", "a")
