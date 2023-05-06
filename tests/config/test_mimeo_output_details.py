
from mimeo.config.exc import (InvalidIndentError, MissingRequiredPropertyError,
                              UnsupportedPropertyValueError)
from mimeo.config.mimeo_config import MimeoOutput
from tests.utils import assert_throws


def test_str():
    output = {
        "direction": "stdout",
        "format": "xml",
        "xml_declaration": True,
        "indent": 4,
        "directory_path": "out",
        "file_name": "out-file",
        "method": "PUT",
        "protocol": "https",
        "host": "localhost",
        "port": 8080,
        "endpoint": "/document",
        "auth": "digest",
        "username": "admin",
        "password": "admin",
    }

    mimeo_output = MimeoOutput(output)
    assert str(mimeo_output) == str(output)


def test_parsing_output_with_default_direction_independent_settings():
    output = {}

    mimeo_output = MimeoOutput(output)
    assert mimeo_output.format == "xml"
    assert mimeo_output.xml_declaration is False
    assert mimeo_output.indent == 0


def test_parsing_output_with_customized_direction_independent_settings():
    output = {
        "format": "xml",
        "xml_declaration": True,
        "indent": 4,
    }

    mimeo_output = MimeoOutput(output)
    assert mimeo_output.format == "xml"
    assert mimeo_output.xml_declaration is True
    assert mimeo_output.indent == 4


def test_parsing_output_stdout():
    output = {
        "direction": "stdout",
    }

    mimeo_output = MimeoOutput(output)
    assert mimeo_output.direction == "stdout"
    assert mimeo_output.format == "xml"
    assert mimeo_output.xml_declaration is False
    assert mimeo_output.indent == 0
    assert mimeo_output.directory_path is None
    assert mimeo_output.file_name is None
    assert mimeo_output.method is None
    assert mimeo_output.auth is None
    assert mimeo_output.protocol is None
    assert mimeo_output.host is None
    assert mimeo_output.port is None
    assert mimeo_output.endpoint is None
    assert mimeo_output.username is None
    assert mimeo_output.password is None
    assert mimeo_output.directory_path is None
    assert mimeo_output.file_name is None


def test_parsing_output_stdout_with_other_directions_customization():
    output = {
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
        "password": "admin",
    }

    mimeo_output = MimeoOutput(output)
    assert mimeo_output.direction == "stdout"
    assert mimeo_output.format == "xml"
    assert mimeo_output.xml_declaration is False
    assert mimeo_output.indent == 0
    assert mimeo_output.directory_path is None
    assert mimeo_output.file_name is None
    assert mimeo_output.method is None
    assert mimeo_output.auth is None
    assert mimeo_output.protocol is None
    assert mimeo_output.host is None
    assert mimeo_output.port is None
    assert mimeo_output.endpoint is None
    assert mimeo_output.username is None
    assert mimeo_output.password is None


def test_parsing_output_file_default():
    output = {
        "direction": "file",
    }

    mimeo_output = MimeoOutput(output)
    assert mimeo_output.direction == "file"
    assert mimeo_output.format == "xml"
    assert mimeo_output.xml_declaration is False
    assert mimeo_output.indent == 0
    assert mimeo_output.directory_path == "mimeo-output"
    assert mimeo_output.file_name == "mimeo-output-{}.xml"
    assert mimeo_output.method is None
    assert mimeo_output.auth is None
    assert mimeo_output.protocol is None
    assert mimeo_output.host is None
    assert mimeo_output.port is None
    assert mimeo_output.endpoint is None
    assert mimeo_output.username is None
    assert mimeo_output.password is None


def test_parsing_output_file_customized():
    output = {
        "direction": "file",
        "directory_path": "out",
        "file_name": "out-file",
    }

    mimeo_output = MimeoOutput(output)
    assert mimeo_output.direction == "file"
    assert mimeo_output.format == "xml"
    assert mimeo_output.xml_declaration is False
    assert mimeo_output.indent == 0
    assert mimeo_output.directory_path == "out"
    assert mimeo_output.file_name == "out-file-{}.xml"
    assert mimeo_output.method is None
    assert mimeo_output.auth is None
    assert mimeo_output.protocol is None
    assert mimeo_output.host is None
    assert mimeo_output.port is None
    assert mimeo_output.endpoint is None
    assert mimeo_output.username is None
    assert mimeo_output.password is None


def test_parsing_output_http_default():
    output = {
        "direction": "http",
        "host": "localhost",
        "endpoint": "/document",
        "username": "admin",
        "password": "admin",
    }

    mimeo_output = MimeoOutput(output)
    assert mimeo_output.direction == "http"
    assert mimeo_output.format == "xml"
    assert mimeo_output.xml_declaration is False
    assert mimeo_output.indent == 0
    assert mimeo_output.method == "POST"
    assert mimeo_output.auth == "basic"
    assert mimeo_output.protocol == "http"
    assert mimeo_output.host == "localhost"
    assert mimeo_output.port is None
    assert mimeo_output.endpoint == "/document"
    assert mimeo_output.username == "admin"
    assert mimeo_output.password == "admin"
    assert mimeo_output.directory_path is None
    assert mimeo_output.file_name is None


def test_parsing_output_http_customized():
    output = {
        "direction": "http",
        "method": "PUT",
        "protocol": "https",
        "host": "localhost",
        "port": 8080,
        "endpoint": "/document",
        "auth": "digest",
        "username": "admin",
        "password": "admin",
    }

    mimeo_output = MimeoOutput(output)
    assert mimeo_output.direction == "http"
    assert mimeo_output.format == "xml"
    assert mimeo_output.xml_declaration is False
    assert mimeo_output.indent == 0
    assert mimeo_output.method == "PUT"
    assert mimeo_output.auth == "digest"
    assert mimeo_output.protocol == "https"
    assert mimeo_output.host == "localhost"
    assert mimeo_output.port == 8080
    assert mimeo_output.endpoint == "/document"
    assert mimeo_output.username == "admin"
    assert mimeo_output.password == "admin"
    assert mimeo_output.directory_path is None
    assert mimeo_output.file_name is None


@assert_throws(err_type=InvalidIndentError,
               msg="Provided indent [{indent}] is negative!",
               params={"indent": -1})
def test_parsing_output_with_invalid_indent():
    output = {
        "indent": -1,
    }
    MimeoOutput(output)


@assert_throws(err_type=UnsupportedPropertyValueError,
               msg="Provided format [{format}] is not supported! "
                   "Supported values: [{values}].",
               params={"format": "unsupported_format",
                       "values": "xml"})
def test_parsing_output_with_unsupported_format():
    output = {
        "format": "unsupported_format",
    }
    MimeoOutput(output)


@assert_throws(err_type=UnsupportedPropertyValueError,
               msg="Provided direction [{direction}] is not supported! "
                   "Supported values: [{values}].",
               params={"direction": "unsupported_direction",
                       "values": "stdout, file, http"})
def test_parsing_output_unsupported_direction():
    output = {
        "direction": "unsupported_direction",
    }
    MimeoOutput(output)


@assert_throws(err_type=UnsupportedPropertyValueError,
               msg="Provided auth [{auth}] is not supported! "
                   "Supported values: [{values}].",
               params={"auth": "unsupported_auth",
                       "values": "basic, digest"})
def test_parsing_output_unsupported_auth_method():
    output = {
        "direction": "http",
        "host": "localhost",
        "endpoint": "/documents",
        "auth": "unsupported_auth",
        "username": "admin",
        "password": "admin",
    }
    MimeoOutput(output)


@assert_throws(err_type=UnsupportedPropertyValueError,
               msg="Provided method [{method}] is not supported! "
                   "Supported values: [{values}].",
               params={"method": "unsupported_request_method",
                       "values": "POST, PUT"})
def test_parsing_output_unsupported_request_method():
    output = {
        "direction": "http",
        "method": "unsupported_request_method",
        "host": "localhost",
        "endpoint": "/documents",
        "username": "admin",
        "password": "admin",
    }
    MimeoOutput(output)


@assert_throws(err_type=MissingRequiredPropertyError,
               msg="Missing required fields is HTTP output details: {fields}",
               params={"fields": "endpoint"})
def test_parsing_output_missing_required_field():
    output = {
        "direction": "http",
        "host": "localhost",
        "username": "admin",
        "password": "admin",
    }
    MimeoOutput(output)


@assert_throws(err_type=MissingRequiredPropertyError,
               msg="Missing required fields is HTTP output details: {fields}",
               params={"fields": "host, endpoint, username, password"})
def test_parsing_output_missing_required_fields():
    output = {
        "direction": "http",
    }
    MimeoOutput(output)
