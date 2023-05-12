import functools
import sys
from typing import Callable, List, Type, Tuple

import pytest
from aiohttp import BasicAuth
from aioresponses import aioresponses
from aioresponses.core import RequestCall
from yarl import URL

__all__ = [
    "get_class_impl_error_msg",
    "assert_throws",
    "assert_requests_sent",
    "assert_request_sent",
    "assert_requests_count",
]


def get_class_impl_error_msg(
        cls: str,
        methods_list: List[str],
) -> str:
    methods = ", ".join(methods_list)
    plural = sys.version_info < (3, 9) or len(methods_list) > 1
    method = "methods" if plural else "method"
    return f"Can't instantiate abstract class {cls} with abstract {method} {methods}"


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


def assert_requests_sent(
        mock: aioresponses,
        requests: list,
):
    assert_requests_count(mock, len(requests))
    for request in requests:
        assert_request_sent(mock, **request)


def assert_request_sent(
        mock: aioresponses,
        method: str,
        url: str,
        body: str = None,
        auth: Tuple[str, str] = None,
):
    requests = mock.requests.get((method, URL(url)))
    assert requests is not None

    found = next(filter(lambda r: _matches_request(r, body, auth), requests))
    assert found is not None


def assert_requests_count(
        mock: aioresponses,
        expected_count: int):
    actual_count = 0
    for key in mock.requests:
        actual_count += len(mock.requests[key])
    assert actual_count == expected_count


def _matches_request(
        request: RequestCall,
        body: str = None,
        auth: tuple[str, str] = None,
) -> bool:
    actual_body = request.kwargs.get("data")
    actual_auth = request.kwargs.get("auth")
    matches_body = body is None or actual_body == body
    matches_auth = auth is None or actual_auth == BasicAuth(auth[0], auth[1], "utf-8")
    return matches_body and matches_auth
