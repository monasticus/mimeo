"""The Mimeo Configuration Constants module."""
import yaml

from mimeo import tools

with tools.get_resource("constants.yaml") as config_file:
    constants = yaml.safe_load(config_file.read())
    _cc = constants["mimeo-config"]

########################################################################################
#                                    OUTPUT DETAILS                                    #
########################################################################################
_output_constants = _cc["output"]
OUTPUT_KEY = _output_constants["key"]
OUTPUT_FORMAT_KEY = _output_constants["format"]["key"]
OUTPUT_DIRECTION_KEY = _output_constants["direction"]["key"]

########################################################################################
# --------------------------------- format specific ---------------------------------- #
_format_details = _output_constants["format"]
SUPPORTED_OUTPUT_FORMATS = _format_details["supported-values"].values()
OUTPUT_FORMAT_XML = _format_details["supported-values"]["xml"]

# -------------------------------- xml format specific ------------------------------- #
_xml_format_details = _format_details["xml"]["details"]
OUTPUT_XML_DECLARATION_KEY = _xml_format_details["xml-declaration"]["key"]
OUTPUT_INDENT_KEY = _xml_format_details["indent"]["key"]

########################################################################################
# -------------------------------- direction specific -------------------------------- #
_direction_details = _output_constants["direction"]
SUPPORTED_OUTPUT_DIRECTIONS = _direction_details["supported-values"].values()
OUTPUT_DIRECTION_FILE = _direction_details["supported-values"]["file"]
OUTPUT_DIRECTION_STD_OUT = _direction_details["supported-values"]["std-out"]
OUTPUT_DIRECTION_HTTP = _direction_details["supported-values"]["http"]

# ----------------------------- file direction specific ------------------------------ #
_file_direction_details = _output_constants["direction"]["file"]["details"]
OUTPUT_DIRECTORY_PATH_KEY = _file_direction_details["directory-path"]["key"]
OUTPUT_FILE_NAME_KEY = _file_direction_details["file-name"]["key"]

# ----------------------------- http direction specific ------------------------------ #
REQUIRED_HTTP_DETAILS = _output_constants["direction"]["http"]["required"]

_http_direction_details = _output_constants["direction"]["http"]["details"]
OUTPUT_METHOD_KEY = _http_direction_details["method"]["key"]
OUTPUT_PROTOCOL_KEY = _http_direction_details["protocol"]["key"]
OUTPUT_HOST_KEY = _http_direction_details["host"]["key"]
OUTPUT_PORT_KEY = _http_direction_details["port"]["key"]
OUTPUT_ENDPOINT_KEY = _http_direction_details["endpoint"]["key"]
OUTPUT_USERNAME_KEY = _http_direction_details["username"]["key"]
OUTPUT_PASSWORD_KEY = _http_direction_details["password"]["key"]

_http_method_details = _http_direction_details["method"]
SUPPORTED_REQUEST_METHODS = _http_method_details["supported-values"].values()
OUTPUT_DIRECTION_HTTP_REQUEST_POST = _http_method_details["supported-values"]["post"]
OUTPUT_DIRECTION_HTTP_REQUEST_PUT = _http_method_details["supported-values"]["put"]

_protocol_details = _http_direction_details["protocol"]
SUPPORTED_REQUEST_PROTOCOLS = _protocol_details["supported-values"].values()
OUTPUT_DIRECTION_HTTP_PROTOCOL_HTTP = _protocol_details["supported-values"]["http"]
OUTPUT_DIRECTION_HTTP_PROTOCOL_HTTPS = _protocol_details["supported-values"]["https"]

########################################################################################
#                                      MIMEO VARS                                      #
########################################################################################
_vars_constants = _cc["vars"]
VARS_KEY = _vars_constants["key"]

########################################################################################
#                                   MIMEO TEMPLATES                                    #
########################################################################################
_templates_constants = _cc["templates"]
TEMPLATES_KEY = _templates_constants["key"]
TEMPLATES_COUNT_KEY = _templates_constants["count"]["key"]
TEMPLATES_MODEL_KEY = _templates_constants["model"]["key"]

########################################################################################
# -------------------------------- Mimeo Model level --------------------------------- #
_model_constants = _templates_constants["model"]
MODEL_CONTEXT_KEY = _model_constants["context"]["key"]
MODEL_ATTRIBUTES_KEY = _model_constants["attributes"]["key"]
MODEL_VALUE_KEY = _model_constants["text-node-value"]["key"]
MODEL_MIMEO_UTIL_KEY = _model_constants["mimeo-util"]["key"]
MODEL_MIMEO_UTIL_NAME_KEY = _model_constants["mimeo-util"]["name"]["key"]

__all__ = [
    "OUTPUT_KEY",
    "OUTPUT_FORMAT_KEY",
    "OUTPUT_DIRECTION_KEY",
    "SUPPORTED_OUTPUT_FORMATS",
    "OUTPUT_FORMAT_XML",
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
    "OUTPUT_DIRECTION_HTTP_REQUEST_POST",
    "OUTPUT_DIRECTION_HTTP_REQUEST_PUT",
    "SUPPORTED_REQUEST_PROTOCOLS",
    "OUTPUT_DIRECTION_HTTP_PROTOCOL_HTTP",
    "OUTPUT_DIRECTION_HTTP_PROTOCOL_HTTPS",
    "VARS_KEY",
    "TEMPLATES_KEY",
    "TEMPLATES_COUNT_KEY",
    "TEMPLATES_MODEL_KEY",
    "MODEL_CONTEXT_KEY",
    "MODEL_ATTRIBUTES_KEY",
    "MODEL_VALUE_KEY",
    "MODEL_MIMEO_UTIL_KEY",
    "MODEL_MIMEO_UTIL_NAME_KEY",
]
