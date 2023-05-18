from mimeo.database.exc import DataNotFoundError
from mimeo.utils.exc import InvalidMimeoUtilError, InvalidValueError
from tests.utils import assert_throws


@assert_throws(err_type=ValueError,
               msg="Provided error code is not a InvalidMimeoUtilError.Code enum!")
def test_invalid_mimeo_util_error_code():
    raise InvalidMimeoUtilError("UNSUPPORTED_MIMEO_UTIL", name="unsupported_util")


@assert_throws(err_type=ValueError,
               msg="Provided error code is not a InvalidValueError.Code enum!")
def test_invalid_value_error_code():
    raise InvalidValueError("NEGATIVE_LENGTH", length=-1)


@assert_throws(err_type=ValueError,
               msg="Provided error code is not a DataNotFoundError.Code enum!")
def test_data_not_found_error_code():
    raise DataNotFoundError("NOT_FOUND", data="country")
