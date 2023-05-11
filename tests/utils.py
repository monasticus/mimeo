import functools
import sys
from typing import Callable, List, Type

import pytest
from requests import PreparedRequest


def assert_throws(
        err_type: Type[Exception],
        msg: str,
        params: dict = None,
) -> Callable:

    def test(func: Callable) -> Callable:

        @functools.wraps(func)
        def test_wrapper(*args, **kwargs):
            with pytest.raises(err_type) as err:
                func(*args, **kwargs)
            expected_msg = msg if params is None else msg.format(**params)
            assert err.value.args[0] == expected_msg
        return test_wrapper

    return test


def get_class_impl_error_msg(
        cls: str,
        methods_list: List[str],
) -> str:
    methods = ", ".join(methods_list)
    plural = sys.version_info < (3, 9) or len(methods_list) > 1
    method = "methods" if plural else "method"
    return f"Can't instantiate abstract class {cls} with abstract {method} {methods}"


def get_request_body_matcher(
        body_list: list,
) -> Callable:

    def match_body(r: PreparedRequest) -> tuple[bool, str]:
        valid = r.body in body_list
        reason = f"The request body [{r.body}] doesn't match any of expected."
        return valid, reason

    return match_body
