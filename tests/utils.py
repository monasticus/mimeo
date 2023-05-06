import functools
import sys
from typing import Callable, List, Type

import pytest


def assert_throws(
        err_type: Type[Exception],
        message: str,
        params: dict = None,
) -> Callable:

    def test(func: Callable) -> Callable:

        @functools.wraps(func)
        def test_wrapper(*args, **kwargs):
            with pytest.raises(err_type) as err:
                func(*args, **kwargs)
            expected_msg = message if params is None else message.format(**params)
            assert err.value.args[0] == expected_msg
        return test_wrapper

    return test


def get_class_impl_error_msg(cls: str, methods_list: List[str]) -> str:
    methods = ', '.join(methods_list)
    plural = sys.version_info < (3, 9) or len(methods_list) > 1
    method = "methods" if plural else "method"
    return f"Can't instantiate abstract class {cls} with abstract {method} {methods}"
