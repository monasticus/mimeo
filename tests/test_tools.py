import pytest

from mimeo import tools
from mimeo.resources.exc import ResourceNotFound


def test_get_resource_existing():
    with tools.get_resource("logging.yaml") as resource:
        assert resource.name.endswith("resources/logging.yaml")


def test_get_resource_non_existing():
    with pytest.raises(ResourceNotFound) as err:
        tools.get_resource("non-existing-file.yaml")

    assert err.value.args[0] == "No such resource: [non-existing-file.yaml]"
