import functools
from typing import Callable, Type

import pytest

from mimeo import tools
from mimeo.resources.exc import ResourceNotFound


def assert_throws(err_type: Type[Exception], message: str, params: dict = None) -> Callable:

    def test(func: Callable) -> Callable:

        @functools.wraps(func)
        def test_wrapper(*args, **kwargs):
            with pytest.raises(err_type) as err:
                func(*args, **kwargs)
            expected_msg = message if params is None else message.format(**params)
            assert err.value.args[0] == expected_msg
        return test_wrapper

    return test


def test_get_resource_existing():
    with tools.get_resource("logging.yaml") as resource:
        assert resource.name.endswith("resources/logging.yaml")


@assert_throws(err_type=ResourceNotFound,
               message="No such resource: [{res}]",
               params={"res": "non-existing-file.yaml"})
def test_get_resource_non_existing():
    tools.get_resource("non-existing-file.yaml")
