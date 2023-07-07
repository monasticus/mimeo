"""The Mimeo Configuration Constants module."""
from __future__ import annotations

import yaml

from mimeo import tools

with tools.get_resource("constants.yaml") as config_file:
    constants = yaml.safe_load(config_file.read())
    _cc = constants["mimeo-config"]

CONFIG_XML_ROOT_NAME: str = _cc["key"]

########################################################################################
#                                    OUTPUT DETAILS                                    #
########################################################################################
_output_constants: dict = _cc["output"]
OUTPUT_KEY: str = _output_constants["key"]
OUTPUT_FORMAT_KEY: str = _output_constants["format"]["key"]
OUTPUT_DIRECTION_KEY: str = _output_constants["direction"]["key"]

########################################################################################
# --------------------------------- format specific ---------------------------------- #
_format_details: dict = _output_constants["format"]["details"]
OUTPUT_INDENT_KEY: str = _format_details["indent"]["key"]

_format_values: dict = _output_constants["format"]["values"]
SUPPORTED_OUTPUT_FORMATS: tuple = tuple(
    format_["key"]
    for format_ in _format_values.values())
OUTPUT_FORMAT_XML: str = _format_values["xml"]["key"]
OUTPUT_FORMAT_JSON: str = _format_values["json"]["key"]

# -------------------------------- xml format specific ------------------------------- #
_xml_format_details: dict = _format_values["xml"]["details"]
OUTPUT_XML_DECLARATION_KEY: str = _xml_format_details["xml-declaration"]["key"]

########################################################################################
# -------------------------------- direction specific -------------------------------- #
_direction_details: dict = _output_constants["direction"]["values"]
SUPPORTED_OUTPUT_DIRECTIONS: tuple = tuple(
    direction["key"]
    for direction in _direction_details.values())
OUTPUT_DIRECTION_FILE: str = _direction_details["file"]["key"]
OUTPUT_DIRECTION_STD_OUT: str = _direction_details["std-out"]["key"]
OUTPUT_DIRECTION_HTTP: str = _direction_details["http"]["key"]

# ----------------------------- file direction specific ------------------------------ #
_file_direction_details: dict = _direction_details["file"]["details"]
OUTPUT_DIRECTORY_PATH_KEY: str = _file_direction_details["directory-path"]["key"]
OUTPUT_FILE_NAME_KEY: str = _file_direction_details["file-name"]["key"]

# ----------------------------- http direction specific ------------------------------ #
_http_direction_details: dict = _direction_details["http"]["details"]
REQUIRED_HTTP_DETAILS: tuple = tuple(
    prop["key"] for prop in _http_direction_details.values()
    if prop.get("required", False) is True)

OUTPUT_METHOD_KEY: str = _http_direction_details["method"]["key"]
OUTPUT_PROTOCOL_KEY: str = _http_direction_details["protocol"]["key"]
OUTPUT_HOST_KEY: str = _http_direction_details["host"]["key"]
OUTPUT_PORT_KEY: str = _http_direction_details["port"]["key"]
OUTPUT_ENDPOINT_KEY: str = _http_direction_details["endpoint"]["key"]
OUTPUT_USERNAME_KEY: str = _http_direction_details["username"]["key"]
OUTPUT_PASSWORD_KEY: str = _http_direction_details["password"]["key"]

_req_method_details: dict = _http_direction_details["method"]["values"]
SUPPORTED_REQUEST_METHODS: tuple = tuple(_req_method_details.values())
OUTPUT_HTTP_REQUEST_POST: str = _req_method_details["post"]
OUTPUT_HTTP_REQUEST_PUT: str = _req_method_details["put"]

_req_protocol_details: dict = _http_direction_details["protocol"]["values"]
SUPPORTED_REQUEST_PROTOCOLS: tuple = tuple(_req_protocol_details.values())
OUTPUT_PROTOCOL_HTTP: str = _req_protocol_details["http"]
OUTPUT_PROTOCOL_HTTPS: str = _req_protocol_details["https"]

########################################################################################
#                                      MIMEO VARS                                      #
########################################################################################
_vars_constants: dict = _cc["vars"]
VARS_KEY: str = _vars_constants["key"]

########################################################################################
#                                      MIMEO REFS                                      #
########################################################################################
_refs_constants: dict = _cc["refs"]
REFS_KEY: str = _refs_constants["key"]

########################################################################################
# ---------------------------------- refs details ------------------------------------ #
_refs_details: dict = _refs_constants["details"]
REQUIRED_REFS_DETAILS: tuple = tuple(
    prop["key"] for prop in _refs_details.values()
    if prop.get("required", False) is True)
REFS_DETAIL_CONTEXT: str = _refs_details["context"]["key"]
REFS_DETAIL_FIELD: str = _refs_details["field"]["key"]
REFS_DETAIL_TYPE: str = _refs_details["type"]["key"]

# ------------------------------------ refs types ------------------------------------ #
_refs_types: dict = _refs_details["type"]["values"]
SUPPORTED_REFS_TYPES: tuple = tuple(_refs_types.values())
REFS_TYPE_ANY: str = _refs_details["type"]["values"]["any"]
REFS_TYPE_PARALLEL: str = _refs_details["type"]["values"]["parallel"]

########################################################################################
# ------------------------------ refs forbidden names -------------------------------- #
REFS_FORBIDDEN_NAMES: tuple = tuple(_refs_constants["forbidden-names"])

########################################################################################
#                                   MIMEO TEMPLATES                                    #
########################################################################################
_templates_constants: dict = _cc["templates"]
TEMPLATES_KEY: str = _templates_constants["key"]
TEMPLATES_XML_TEMPLATE_TAG: str = _templates_constants["xml-template-tag"]["key"]
TEMPLATES_COUNT_KEY: str = _templates_constants["count"]["key"]
TEMPLATES_MODEL_KEY: str = _templates_constants["model"]["key"]

########################################################################################
# -------------------------------- Mimeo Model level --------------------------------- #
_model_constants: dict = _templates_constants["model"]
MODEL_CONTEXT_KEY: str = _model_constants["context"]["key"]
MODEL_ATTRIBUTES_KEY: str = _model_constants["attributes"]["key"]
MODEL_TEXT_VALUE_KEY: str = _model_constants["text-node-value"]["key"]
MODEL_MIMEO_UTIL_KEY: str = _model_constants["mimeo-util"]["key"]
MODEL_MIMEO_UTIL_NAME_KEY: str = _model_constants["mimeo-util"]["name"]["key"]

__all__ = [
    "CONFIG_XML_ROOT_NAME",
    "OUTPUT_KEY",
    "OUTPUT_FORMAT_KEY",
    "OUTPUT_DIRECTION_KEY",
    "SUPPORTED_OUTPUT_FORMATS",
    "OUTPUT_FORMAT_XML",
    "OUTPUT_FORMAT_JSON",
    "OUTPUT_XML_DECLARATION_KEY",
    "OUTPUT_INDENT_KEY",
    "SUPPORTED_OUTPUT_DIRECTIONS",
    "OUTPUT_DIRECTION_FILE",
    "OUTPUT_DIRECTION_STD_OUT",
    "OUTPUT_DIRECTION_HTTP",
    "OUTPUT_DIRECTORY_PATH_KEY",
    "OUTPUT_FILE_NAME_KEY",
    "REQUIRED_HTTP_DETAILS",
    "OUTPUT_METHOD_KEY",
    "OUTPUT_PROTOCOL_KEY",
    "OUTPUT_HOST_KEY",
    "OUTPUT_PORT_KEY",
    "OUTPUT_ENDPOINT_KEY",
    "OUTPUT_USERNAME_KEY",
    "OUTPUT_PASSWORD_KEY",
    "SUPPORTED_REQUEST_METHODS",
    "OUTPUT_HTTP_REQUEST_POST",
    "OUTPUT_HTTP_REQUEST_PUT",
    "SUPPORTED_REQUEST_PROTOCOLS",
    "OUTPUT_PROTOCOL_HTTP",
    "OUTPUT_PROTOCOL_HTTPS",
    "VARS_KEY",
    "REFS_KEY",
    "REQUIRED_REFS_DETAILS",
    "REFS_DETAIL_CONTEXT",
    "REFS_DETAIL_FIELD",
    "REFS_DETAIL_TYPE",
    "SUPPORTED_REFS_TYPES",
    "REFS_TYPE_ANY",
    "REFS_TYPE_PARALLEL",
    "REFS_FORBIDDEN_NAMES",
    "TEMPLATES_KEY",
    "TEMPLATES_XML_TEMPLATE_TAG",
    "TEMPLATES_COUNT_KEY",
    "TEMPLATES_MODEL_KEY",
    "MODEL_CONTEXT_KEY",
    "MODEL_ATTRIBUTES_KEY",
    "MODEL_TEXT_VALUE_KEY",
    "MODEL_MIMEO_UTIL_KEY",
    "MODEL_MIMEO_UTIL_NAME_KEY",
]
