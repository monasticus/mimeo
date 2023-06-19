from __future__ import annotations

import functools
import sys
from typing import Callable

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
        methods_list: list[str],
) -> str:
    methods = ", ".join(methods_list)
    plural = sys.version_info < (3, 9) or len(methods_list) > 1
    method = "methods" if plural else "method"
    return f"Can't instantiate abstract class {cls} with abstract {method} {methods}"


def assert_throws(
        err_type: type[Exception],
        msg: str,
        **params,
) -> Callable:
    def test(func: Callable) -> Callable:
        @functools.wraps(func)
        def test_wrapper(*args, **kwargs):
            with pytest.raises(err_type) as err:
                func(*args, **kwargs)
            actual_msg = err.value.args[0]
            expected_msg = msg if params == {} else msg.format(**params)
            assert actual_msg == expected_msg

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
        details: dict,
):
    requests = mock.requests.get((method, URL(url)))
    assert requests is not None

    found = next(filter(lambda r: _matches_request(r, **details), requests))
    assert found is not None


def assert_requests_count(
        mock: aioresponses,
        expected_count: int,
):
    actual_count = 0
    for key in mock.requests:
        actual_count += len(mock.requests[key])
    assert actual_count == expected_count


def _matches_request(
        request: RequestCall,
        body: str = None,
        auth: tuple[str, str] = None,
        content_type: str = None,
) -> bool:
    actual_body = request.kwargs.get("data")
    actual_auth = request.kwargs.get("auth")
    actual_content_type = request.kwargs.get("headers").get("Content-Type")
    matches_body = body is None or actual_body == body
    matches_auth = auth is None or actual_auth == BasicAuth(auth[0], auth[1], "utf-8")
    matches_content_type = content_type is None or actual_content_type == content_type
    return matches_body and matches_auth and matches_content_type
