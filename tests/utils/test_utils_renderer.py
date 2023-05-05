
from mimeo.utils.exc import InvalidMimeoUtil
from mimeo.utils.renderers import UtilsRenderer
from tests.test_tools import assert_throws


@assert_throws(err_type=InvalidMimeoUtil,
               message="Missing Mimeo Util name in configuration [{}]!")
def test_missing_mimeo_util_name():
    UtilsRenderer.render_parametrized({})


@assert_throws(err_type=InvalidMimeoUtil,
               message="No such Mimeo Util [{util}]!",
               params={"util": "non-existing-util"})
def test_no_such_mimeo_util_raw():
    UtilsRenderer.render_raw("non-existing-util")


@assert_throws(err_type=InvalidMimeoUtil,
               message="No such Mimeo Util [{util}]!",
               params={"util": "non-existing-util"})
def test_no_such_mimeo_util_parametrized():
    UtilsRenderer.render_parametrized({"_name": "non-existing-util"})
