import pytest

from mimeo.config.mimeo_config import MimeoOutputDetails
from mimeo.config.exc import (MissingRequiredProperty, UnsupportedAuthMethod,
                              UnsupportedOutputDirection,
                              UnsupportedRequestMethod)


def test_str():
    output_details = {
        "direction": "stdout",
        "directory_path": "out",
        "file_name": "out-file",
        "method": "PUT",
        "protocol": "https",
        "host": "localhost",
        "port": 8080,
        "endpoint": "/document",
        "auth": "digest",
        "username": "admin",
        "password": "admin"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert str(mimeo_output_details) == str(output_details)


def test_parsing_output_details_stdout():
    output_details = {
        "direction": "stdout"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "stdout"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None
    assert mimeo_output_details.method is None
    assert mimeo_output_details.auth is None
    assert mimeo_output_details.protocol is None
    assert mimeo_output_details.host is None
    assert mimeo_output_details.port is None
    assert mimeo_output_details.endpoint is None
    assert mimeo_output_details.username is None
    assert mimeo_output_details.password is None
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None


def test_parsing_output_details_stdout_with_other_directions_customization():
    output_details = {
        "direction": "stdout",
        "directory_path": "out",
        "file_name": "out-file",
        "method": "PUT",
        "protocol": "https",
        "host": "localhost",
        "port": 8080,
        "endpoint": "/document",
        "auth": "digest",
        "username": "admin",
        "password": "admin"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "stdout"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None
    assert mimeo_output_details.method is None
    assert mimeo_output_details.auth is None
    assert mimeo_output_details.protocol is None
    assert mimeo_output_details.host is None
    assert mimeo_output_details.port is None
    assert mimeo_output_details.endpoint is None
    assert mimeo_output_details.username is None
    assert mimeo_output_details.password is None


def test_parsing_output_details_file_default():
    output_details = {
        "direction": "file"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "file"
    assert mimeo_output_details.directory_path == "mimeo-output"
    assert mimeo_output_details.file_name_tmplt == "mimeo-output-{}.xml"
    assert mimeo_output_details.method is None
    assert mimeo_output_details.auth is None
    assert mimeo_output_details.protocol is None
    assert mimeo_output_details.host is None
    assert mimeo_output_details.port is None
    assert mimeo_output_details.endpoint is None
    assert mimeo_output_details.username is None
    assert mimeo_output_details.password is None


def test_parsing_output_details_file_customized():
    output_details = {
        "direction": "file",
        "directory_path": "out",
        "file_name": "out-file"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "file"
    assert mimeo_output_details.directory_path == "out"
    assert mimeo_output_details.file_name_tmplt == "out-file-{}.xml"


def test_parsing_output_details_http_default():
    output_details = {
        "direction": "http",
        "host": "localhost",
        "endpoint": "/document",
        "username": "admin",
        "password": "admin"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "http"
    assert mimeo_output_details.method == "POST"
    assert mimeo_output_details.auth == "basic"
    assert mimeo_output_details.protocol == "http"
    assert mimeo_output_details.host == "localhost"
    assert mimeo_output_details.port is None
    assert mimeo_output_details.endpoint == "/document"
    assert mimeo_output_details.username == "admin"
    assert mimeo_output_details.password == "admin"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None


def test_parsing_output_details_http_customized():
    output_details = {
        "direction": "http",
        "method": "PUT",
        "protocol": "https",
        "host": "localhost",
        "port": 8080,
        "endpoint": "/document",
        "auth": "digest",
        "username": "admin",
        "password": "admin"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "http"
    assert mimeo_output_details.method == "PUT"
    assert mimeo_output_details.auth == "digest"
    assert mimeo_output_details.protocol == "https"
    assert mimeo_output_details.host == "localhost"
    assert mimeo_output_details.port == 8080
    assert mimeo_output_details.endpoint == "/document"
    assert mimeo_output_details.username == "admin"
    assert mimeo_output_details.password == "admin"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None


def test_parsing_output_details_unsupported_direction():
    output_details = {
        "direction": "unsupported_direction"
    }

    with pytest.raises(UnsupportedOutputDirection) as err:
        MimeoOutputDetails("xml", output_details)

    assert err.value.args[0] == "Provided direction [unsupported_direction] is not supported!"


def test_parsing_output_details_unsupported_auth_method():
    output_details = {
        "direction": "http",
        "host": "localhost",
        "endpoint": "/documents",
        "auth": "unsupported_auth",
        "username": "admin",
        "password": "admin"
    }

    with pytest.raises(UnsupportedAuthMethod) as err:
        MimeoOutputDetails("xml", output_details)

    assert err.value.args[0] == "Provided auth [unsupported_auth] is not supported!"


def test_parsing_output_details_unsupported_request_method():
    output_details = {
        "direction": "http",
        "method": "unsupported_request_method",
        "host": "localhost",
        "endpoint": "/documents",
        "username": "admin",
        "password": "admin"
    }

    with pytest.raises(UnsupportedRequestMethod) as err:
        MimeoOutputDetails("xml", output_details)

    assert err.value.args[0] == "Provided request method [unsupported_request_method] is not supported!"


def test_parsing_output_details_missing_required_field():
    output_details = {
        "direction": "http",
        "host": "localhost",
        "username": "admin",
        "password": "admin"
    }

    with pytest.raises(MissingRequiredProperty) as err:
        MimeoOutputDetails("xml", output_details)

    assert err.value.args[0] == "Missing required fields is HTTP output details: endpoint"


def test_parsing_output_details_missing_required_fields():
    output_details = {
        "direction": "http"
    }

    with pytest.raises(MissingRequiredProperty) as err:
        MimeoOutputDetails("xml", output_details)

    assert err.value.args[0] == "Missing required fields is HTTP output details: host, endpoint, username, password"
