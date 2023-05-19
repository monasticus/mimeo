
from mimeo.utils.exc import InvalidMimeoUtilError
from mimeo.utils.renderers import UtilsRenderer
from tests.utils import assert_throws


@assert_throws(err_type=InvalidMimeoUtilError,
               msg="Missing Mimeo Util name in configuration [{config}]!",
               config="{}")
def test_missing_mimeo_util_name():
    UtilsRenderer.render_parametrized({})


@assert_throws(err_type=InvalidMimeoUtilError,
               msg="No such Mimeo Util [{util}]!",
               util="non-existing-util")
def test_no_such_mimeo_util_raw():
    UtilsRenderer.render_raw("non-existing-util")


@assert_throws(err_type=InvalidMimeoUtilError,
               msg="No such Mimeo Util [{util}]!",
               util="non-existing-util")
def test_no_such_mimeo_util_parametrized():
    UtilsRenderer.render_parametrized({"_name": "non-existing-util"})
