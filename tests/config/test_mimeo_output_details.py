import pytest

from mimeo.config.mimeo_config import MimeoOutputDetails
from mimeo.exceptions import UnsupportedOutputDirection, MissingRequiredProperty


def test_parsing_output_details_stdout():
    output_details = {
        "direction": "stdout"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "stdout"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None
    assert mimeo_output_details.method is None
    assert mimeo_output_details.protocol is None
    assert mimeo_output_details.host is None
    assert mimeo_output_details.port is None
    assert mimeo_output_details.endpoint is None
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None


def test_parsing_output_details_stdout_with_file_customization():
    output_details = {
        "direction": "stdout",
        "directory_path": "out",
        "file_name": "out-file"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "stdout"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None
    assert mimeo_output_details.method is None
    assert mimeo_output_details.protocol is None
    assert mimeo_output_details.host is None
    assert mimeo_output_details.port is None
    assert mimeo_output_details.endpoint is None


def test_parsing_output_details_file_default():
    output_details = {
        "direction": "file"
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "file"
    assert mimeo_output_details.directory_path == "mimeo-output"
    assert mimeo_output_details.file_name_tmplt == "mimeo-output-{}.xml"
    assert mimeo_output_details.method is None
    assert mimeo_output_details.protocol is None
    assert mimeo_output_details.host is None
    assert mimeo_output_details.port is None
    assert mimeo_output_details.endpoint is None


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
        "port": 8080,
        "endpoint": "/document",
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "http"
    assert mimeo_output_details.method == "POST"
    assert mimeo_output_details.protocol == "http"
    assert mimeo_output_details.host == "localhost"
    assert mimeo_output_details.port == 8080
    assert mimeo_output_details.endpoint == "/document"
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
    }

    mimeo_output_details = MimeoOutputDetails("xml", output_details)
    assert mimeo_output_details.direction == "http"
    assert mimeo_output_details.method == "PUT"
    assert mimeo_output_details.protocol == "https"
    assert mimeo_output_details.host == "localhost"
    assert mimeo_output_details.port == 8080
    assert mimeo_output_details.endpoint == "/document"
    assert mimeo_output_details.directory_path is None
    assert mimeo_output_details.file_name_tmplt is None


def test_parsing_output_details_unsupported_direction():
    output_details = {
        "direction": "unsupported_direction"
    }

    with pytest.raises(UnsupportedOutputDirection) as err:
        MimeoOutputDetails("xml", output_details)

    assert err.value.args[0] == "Provided direction [unsupported_direction] is not supported!"


def test_parsing_output_details_missing_required_field():
    output_details = {
        "direction": "http",
        "host": "localhost",
        "port": 8080
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

    assert err.value.args[0] == "Missing required fields is HTTP output details: host, port, endpoint"
