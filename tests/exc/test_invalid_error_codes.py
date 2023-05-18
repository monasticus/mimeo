from mimeo.database.exc import DataNotFoundError, OutOfStockError
from mimeo.utils.exc import InvalidMimeoUtilError, InvalidValueError
from tests.utils import assert_throws

common_msg = "Provided error code is not a {cls} enum!"


@assert_throws(err_type=ValueError, msg=common_msg, cls="InvalidMimeoUtilError.Code")
def test_invalid_mimeo_util_error_code():
    raise InvalidMimeoUtilError("UNSUPPORTED_MIMEO_UTIL", name="unsupported_util")


@assert_throws(err_type=ValueError, msg=common_msg, cls="InvalidValueError.Code")
def test_invalid_value_error_code():
    raise InvalidValueError("NEGATIVE_LENGTH", length=-1)


@assert_throws(err_type=ValueError, msg=common_msg, cls="DataNotFoundError.Code")
def test_data_not_found_error_code():
    raise DataNotFoundError("NOT_FOUND", data="country")


@assert_throws(err_type=ValueError, msg=common_msg, cls="OutOfStockError.Code")
def test_out_of_stock_error_code():
    raise OutOfStockError("NO_MORE_UNIQUE_VALUES", num=5, data="cities")
