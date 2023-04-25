"""The Mimeo Configuration module.

It contains classes representing Mimeo Configuration components
at all levels. All of them are Data Transfer Objects:
    * MimeoDTO
        A superclass for all Mimeo configuration DTOs
    * MimeoConfig
        A MimeoDTO class representing Mimeo Configuration
    * MimeoOutputDetails
        A MimeoDTO class representing Mimeo Output Details
    * MimeoTemplate
        A MimeoDTO class representing Mimeo Template
    * MimeoModel
        A MimeoDTO class representing Mimeo Model
"""
import re

from mimeo.config.exc import (InvalidIndent, InvalidMimeoConfig,
                              InvalidMimeoModel, InvalidMimeoTemplate,
                              InvalidVars, MissingRequiredProperty,
                              UnsupportedPropertyValue)
from mimeo.logging import setup_logging

# setup logging when mimeo is used as a python library
setup_logging()


class MimeoDTO:
    """A superclass for all Mimeo configuration DTOs.

    It is meant to store a source dictionary for logging purposes.

    Methods
    -------
    __str__
        Returns the stringified source dictionary of a DTO
    """

    def __init__(self, source: dict):
        """Initialize MimeoDTO class.

        Parameters
        ----------
        source : dict
            The source dictionary for a Mimeo DTO
        """
        self._source = source

    def __str__(self):
        """Return the stringified source dictionary of a DTO."""
        return str(self._source)


class MimeoConfig(MimeoDTO):
    """A MimeoDTO class representing Mimeo Configuration.

    It is a python representation of a Mimeo Configuration file / dictionary.

    Attributes
    ----------
    OUTPUT_FORMAT_KEY : str
        A Mimeo Configuration output format key
    OUTPUT_DETAILS_KEY : str
        A Mimeo Configuration output details key
    OUTPUT_DETAILS_DIRECTION_KEY : str
        A Mimeo Configuration output direction key
    OUTPUT_DETAILS_DIRECTORY_PATH_KEY : str
        A Mimeo Configuration output directory path key
    OUTPUT_DETAILS_FILE_NAME_KEY : str
        A Mimeo Configuration output file name key
    OUTPUT_DETAILS_METHOD_KEY : str
        A Mimeo Configuration http method key
    OUTPUT_DETAILS_PROTOCOL_KEY : str
        A Mimeo Configuration http protocol key
    OUTPUT_DETAILS_HOST_KEY : str
        A Mimeo Configuration http host key
    OUTPUT_DETAILS_PORT_KEY : str
        A Mimeo Configuration http port key
    OUTPUT_DETAILS_ENDPOINT_KEY : str
        A Mimeo Configuration http endpoint key
    OUTPUT_DETAILS_AUTH_KEY : str
        A Mimeo Configuration http auth key
    OUTPUT_DETAILS_USERNAME_KEY : str
        A Mimeo Configuration http username key
    OUTPUT_DETAILS_PASSWORD_KEY : str
        A Mimeo Configuration http password key
    XML_DECLARATION_KEY : str
        A Mimeo Configuration xml declaration key
    INDENT_KEY : str
        A Mimeo Configuration indent key
    VARS_KEY : str
        A Mimeo Configuration vars key
    TEMPLATES_KEY : str
        A Mimeo Configuration templates key
    TEMPLATES_COUNT_KEY : str
        A Mimeo Configuration template's count key
    TEMPLATES_MODEL_KEY : str
        A Mimeo Configuration template's model key
    MODEL_CONTEXT_KEY : str
        A Mimeo Configuration model's context name key
    MODEL_ATTRIBUTES_KEY : str
        A Mimeo Configuration attributes key (for nodes' attributes)
    MODEL_VALUE_KEY : str
        A Mimeo Configuration value key (for nodes' value)
    MODEL_MIMEO_UTIL_KEY : str
        A Mimeo Configuration Mimeo Util key
    MODEL_MIMEO_UTIL_NAME_KEY : str
        A Mimeo Configuration Mimeo Util's name key
    SUPPORTED_OUTPUT_FORMATS : set
        A set of supported output formats
    OUTPUT_DETAILS_DIRECTION_FILE : str
        The 'file' output direction
    OUTPUT_DETAILS_DIRECTION_STD_OUT : str
        The 'stdout' output direction
    OUTPUT_DETAILS_DIRECTION_HTTP : str
        The 'http' output direction
    OUTPUT_DETAILS_DIRECTION_HTTP_REQUEST_POST : str
        The 'POST' http request method
    OUTPUT_DETAILS_DIRECTION_HTTP_REQUEST_PUT : str
        The 'PUT' http request method
    OUTPUT_DETAILS_DIRECTION_HTTP_AUTH_BASIC : str
        The 'basic' http auth method
    OUTPUT_DETAILS_DIRECTION_HTTP_AUTH_DIGEST : str
        The 'digest' http auth method
    SUPPORTED_OUTPUT_DIRECTIONS : set
        List of supported output directions
    SUPPORTED_REQUEST_METHODS : set
        List of supported http request methods
    SUPPORTED_AUTH_METHODS : set
        List of supported auth request methods
    REQUIRED_HTTP_DETAILS : set
        List of required http request output direction details

    output_format : str, default 'xml'
        A Mimeo Configuration output format setting
    output_details : MimeoOutputDetails, default {}
        A Mimeo Output Details settings
    xml_declaration : bool, default False
        A Mimeo Configuration xml declaration setting
    indent : int, default 0
        A Mimeo Configuration indent setting
    vars : dict, default {}
        A Mimeo Configuration vars setting
    templates : list
        A Mimeo Templates setting
    """

    OUTPUT_FORMAT_KEY = "output_format"
    OUTPUT_DETAILS_KEY = "output_details"
    OUTPUT_DETAILS_DIRECTION_KEY = "direction"
    OUTPUT_DETAILS_DIRECTORY_PATH_KEY = "directory_path"
    OUTPUT_DETAILS_FILE_NAME_KEY = "file_name"
    OUTPUT_DETAILS_METHOD_KEY = "method"
    OUTPUT_DETAILS_PROTOCOL_KEY = "protocol"
    OUTPUT_DETAILS_HOST_KEY = "host"
    OUTPUT_DETAILS_PORT_KEY = "port"
    OUTPUT_DETAILS_ENDPOINT_KEY = "endpoint"
    OUTPUT_DETAILS_AUTH_KEY = "auth"
    OUTPUT_DETAILS_USERNAME_KEY = "username"
    OUTPUT_DETAILS_PASSWORD_KEY = "password"
    XML_DECLARATION_KEY = "xml_declaration"
    INDENT_KEY = "indent"
    VARS_KEY = "vars"
    TEMPLATES_KEY = "_templates_"
    TEMPLATES_COUNT_KEY = "count"
    TEMPLATES_MODEL_KEY = "model"
    MODEL_CONTEXT_KEY = "context"
    MODEL_ATTRIBUTES_KEY = "_attrs"
    MODEL_VALUE_KEY = "_value"
    MODEL_MIMEO_UTIL_KEY = "_mimeo_util"
    MODEL_MIMEO_UTIL_NAME_KEY = "_name"

    OUTPUT_FORMAT_XML = "xml"

    OUTPUT_DETAILS_DIRECTION_FILE = "file"
    OUTPUT_DETAILS_DIRECTION_STD_OUT = "stdout"
    OUTPUT_DETAILS_DIRECTION_HTTP = "http"

    OUTPUT_DETAILS_DIRECTION_HTTP_REQUEST_POST = "POST"
    OUTPUT_DETAILS_DIRECTION_HTTP_REQUEST_PUT = "PUT"

    OUTPUT_DETAILS_DIRECTION_HTTP_AUTH_BASIC = "basic"
    OUTPUT_DETAILS_DIRECTION_HTTP_AUTH_DIGEST = "digest"

    SUPPORTED_OUTPUT_FORMATS = (OUTPUT_FORMAT_XML,)

    SUPPORTED_OUTPUT_DIRECTIONS = (OUTPUT_DETAILS_DIRECTION_STD_OUT,
                                   OUTPUT_DETAILS_DIRECTION_FILE,
                                   OUTPUT_DETAILS_DIRECTION_HTTP)
    SUPPORTED_REQUEST_METHODS = (OUTPUT_DETAILS_DIRECTION_HTTP_REQUEST_POST,
                                 OUTPUT_DETAILS_DIRECTION_HTTP_REQUEST_PUT)
    SUPPORTED_AUTH_METHODS = (OUTPUT_DETAILS_DIRECTION_HTTP_AUTH_BASIC,
                              OUTPUT_DETAILS_DIRECTION_HTTP_AUTH_DIGEST)
    REQUIRED_HTTP_DETAILS = (OUTPUT_DETAILS_HOST_KEY,
                             OUTPUT_DETAILS_ENDPOINT_KEY,
                             OUTPUT_DETAILS_USERNAME_KEY,
                             OUTPUT_DETAILS_PASSWORD_KEY)

    def __init__(self, config: dict):
        """Initialize MimeoConfig class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        config : dict
            A source config dictionary
        """
        super().__init__(config)
        self.output_format = MimeoConfig._get_output_format(config)
        self.output_details = MimeoOutputDetails(self.output_format, config.get(self.OUTPUT_DETAILS_KEY, {}))
        self.xml_declaration = config.get(self.XML_DECLARATION_KEY, False)
        self.indent = MimeoConfig._get_indent(config)
        self.vars = MimeoConfig._get_vars(config)
        self.templates = MimeoConfig._get_templates(config)

    @staticmethod
    def _get_output_format(config: dict) -> str:
        """Extract an output format from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary

        Returns
        -------
        output_format : str
            The customized output format or 'xml' by default

        Raises
        ------
        UnsupportedPropertyValue
            If the customized output format is not supported
        """
        output_format = config.get(MimeoConfig.OUTPUT_FORMAT_KEY, MimeoConfig.OUTPUT_FORMAT_XML)
        if output_format in MimeoConfig.SUPPORTED_OUTPUT_FORMATS:
            return output_format
        else:
            raise UnsupportedPropertyValue(MimeoConfig.OUTPUT_FORMAT_KEY,
                                           output_format,
                                           MimeoConfig.SUPPORTED_OUTPUT_FORMATS)

    @staticmethod
    def _get_indent(config: dict) -> int:
        """Extract an indent value from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary

        Returns
        -------
        indent : int
            The customized indent or 0 by default

        Raises
        ------
        InvalidIndent
            If the customized indent is lower than zero
        """
        indent = config.get(MimeoConfig.INDENT_KEY, 0)
        if indent >= 0:
            return indent
        else:
            raise InvalidIndent(indent)

    @staticmethod
    def _get_vars(config: dict) -> dict:
        """Extract variables from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary

        Returns
        -------
        variables : dict
            Customized variables or an empty dictionary

        Raises
        ------
        InvalidVars
            If (1) the vars key does not point to a dictionary or
            (2) some variable's name does not start with a letter,
            is not SNAKE_UPPER_CASE with possible digits or
            (3) some variable's value points to non-atomic value nor Mimeo Util
        """
        variables = config.get(MimeoConfig.VARS_KEY, {})
        if not isinstance(variables, dict):
            raise InvalidVars(f"vars property does not store an object: {variables}")
        for var, val in variables.items():
            if not re.match(r"^[A-Z][A-Z_0-9]*$", var):
                raise InvalidVars(f"Provided var [{var}] is invalid "
                                  "(you can use upper-cased name with underscore and digits, starting with a letter)!")
            if isinstance(val, list) or (isinstance(val, dict) and not MimeoConfig._is_mimeo_util_object(val)):
                raise InvalidVars(f"Provided var [{var}] is invalid (you can use ony atomic values and Mimeo Utils)!")
        return variables

    @staticmethod
    def _get_templates(config: dict) -> list:
        """Extract Mimeo Templates from the source dictionary.

        Parameters
        ----------
        config : dict
            A source config dictionary

        Returns
        -------
        list
            A Mimeo Templates list

        Raises
        ------
        IncorrectMimeoConfig
            If (1) the source dictionary does not include the _templates_ key or
            (2) the _templates_ key does not point to a list
        """
        templates = config.get(MimeoConfig.TEMPLATES_KEY)
        if templates is None:
            raise InvalidMimeoConfig(f"No templates in the Mimeo Config: {config}")
        elif not isinstance(templates, list):
            raise InvalidMimeoConfig(f"_templates_ property does not store an array: {config}")
        else:
            return [MimeoTemplate(template) for template in config.get(MimeoConfig.TEMPLATES_KEY)]

    @staticmethod
    def _is_mimeo_util_object(obj: dict) -> bool:
        """Verify if the object is a Mimeo Util.

        Parameters
        ----------
        obj : dict
            An object to verify

        Returns
        -------
        bool
            True if the object is a dictionary having only one key: _mimeo_util, otherwise False
        """
        return isinstance(obj, dict) and len(obj) == 1 and MimeoConfig.MODEL_MIMEO_UTIL_KEY in obj


class MimeoOutputDetails(MimeoDTO):
    """A MimeoDTO class representing Mimeo Output Details.

    It is a python representation of a Mimeo Output Details configuration node.

    Attributes
    ----------
    direction : str, default 'file'
        The configured output direction
    directory_path : str, default 'mimeo-output'
        The configured file output directory
    file_name_tmplt : str, default 'mimeo-output-{}.{output_format}'
        The configured file output file name template
    method : str, default POST
        The configured http output request method
    protocol : str, default 'http'
        The configured http output protocol
    host : str
        The configured http output host
    port : str
        The configured http output port
    endpoint : str
        The configured http output endpoint
    auth : str, default 'basic'
        The configured http output auth method
    username : str
        The configured http output username
    password : str
        The configured http output password
    """

    def __init__(self, output_format: str, output_details: dict):
        """Initialize MimeoOutputDetails class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        output_format : str
            An output format
        output_details : dict
            A source config output details dictionary
        """
        super().__init__(output_details)
        self.direction = MimeoOutputDetails._get_direction(output_details)
        MimeoOutputDetails._validate_output_details(self.direction, output_details)
        self.directory_path = MimeoOutputDetails._get_directory_path(self.direction, output_details)
        self.file_name_tmplt = MimeoOutputDetails._get_file_name_tmplt(self.direction, output_details, output_format)
        self.method = MimeoOutputDetails._get_method(self.direction, output_details)
        self.protocol = MimeoOutputDetails._get_protocol(self.direction, output_details)
        self.host = MimeoOutputDetails._get_host(self.direction, output_details)
        self.port = MimeoOutputDetails._get_port(self.direction, output_details)
        self.endpoint = MimeoOutputDetails._get_endpoint(self.direction, output_details)
        self.auth = MimeoOutputDetails._get_auth(self.direction, output_details)
        self.username = MimeoOutputDetails._get_username(self.direction, output_details)
        self.password = MimeoOutputDetails._get_password(self.direction, output_details)

    @staticmethod
    def _get_direction(output_details: dict) -> str:
        """Extract output direction from the source dictionary.

        Parameters
        ----------
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        direction : str
            The configured output direction

        Raises
        ------
        UnsupportedPropertyValue
            If the configured output direction is not supported
        """
        direction = output_details.get(MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY,
                                       MimeoConfig.OUTPUT_DETAILS_DIRECTION_FILE)
        if direction in MimeoConfig.SUPPORTED_OUTPUT_DIRECTIONS:
            return direction
        else:
            raise UnsupportedPropertyValue(MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY,
                                           direction,
                                           MimeoConfig.SUPPORTED_OUTPUT_DIRECTIONS)

    @staticmethod
    def _get_directory_path(direction: str, output_details: dict) -> str:
        """Extract an output directory path from the source dictionary.

        It is extracted only when the output direction is 'file'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        str
            The configured output directory path when the output direction is 'file'.
            Otherwise, None. If the 'directory_path' setting is missing returns
            'mimeo-output' by default.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_FILE:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_DIRECTORY_PATH_KEY, "mimeo-output")

    @staticmethod
    def _get_file_name_tmplt(direction: str, output_details: dict, output_format: str):
        """Generate an output file name template based on the source dictionary.

        It is generated only when the output direction is 'file'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        str
            The configured output file name template when the output direction is 'file'.
            Otherwise, None. If the 'file_name' setting is missing returns
            'mimeo-output-{}.{output_format}' by default.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_FILE:
            file_name = output_details.get(MimeoConfig.OUTPUT_DETAILS_FILE_NAME_KEY, "mimeo-output")
            return f"{file_name}-{'{}'}.{output_format}"

    @staticmethod
    def _get_method(direction: str, output_details: dict) -> str:
        """Extract an HTTP request method from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        method: str
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None. If the 'method' setting is missing returns
            'POST' by default.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            method = output_details.get(MimeoConfig.OUTPUT_DETAILS_METHOD_KEY,
                                        MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP_REQUEST_POST)
            if method in MimeoConfig.SUPPORTED_REQUEST_METHODS:
                return method
            else:
                raise UnsupportedPropertyValue(MimeoConfig.OUTPUT_DETAILS_METHOD_KEY,
                                               method,
                                               MimeoConfig.SUPPORTED_REQUEST_METHODS)

    @staticmethod
    def _get_protocol(direction: str, output_details: dict) -> str:
        """Extract an HTTP protocol from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        str
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None. If the 'protocol' setting is missing returns
            'http' by default.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PROTOCOL_KEY,
                                      MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP)

    @staticmethod
    def _get_host(direction: str, output_details: dict) -> str:
        """Extract an HTTP host from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        str
            The configured HTTP host when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_HOST_KEY)

    @staticmethod
    def _get_port(direction: str, output_details: dict) -> str:
        """Extract an HTTP port from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        str
            The configured HTTP port when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PORT_KEY)

    @staticmethod
    def _get_endpoint(direction: str, output_details: dict) -> str:
        """Extract an HTTP endpoint from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        str
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_ENDPOINT_KEY)

    @staticmethod
    def _get_auth(direction: str, output_details: dict) -> str:
        """Extract an HTTP auth method from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        method: str
            The configured HTTP auth method when the output direction is 'http'.
            Otherwise, None. If the 'auth' setting is missing returns
            'basic' by default.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            auth =  output_details.get(MimeoConfig.OUTPUT_DETAILS_AUTH_KEY,
                                       MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP_AUTH_BASIC)
            if auth in MimeoConfig.SUPPORTED_AUTH_METHODS:
                return auth
            else:
                raise UnsupportedPropertyValue(MimeoConfig.OUTPUT_DETAILS_AUTH_KEY,
                                               auth,
                                               MimeoConfig.SUPPORTED_AUTH_METHODS)

    @staticmethod
    def _get_username(direction: str, output_details: dict) -> str:
        """Extract a username from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        str
            The configured username when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_USERNAME_KEY)

    @staticmethod
    def _get_password(direction: str, output_details: dict) -> str:
        """Extract a password from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Returns
        -------
        str
            The configured password when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PASSWORD_KEY)

    @staticmethod
    def _validate_output_details(direction: str, output_details: dict) -> None:
        """Validate output details in the source dictionary.

        The validation is being done according to the configured output
        direction.

        Parameters
        ----------
        direction : str
            The configured output direction
        output_details : dict
            A source config output details dictionary

        Raises
        ------
        MissingRequiredProperty
            If the output details doesn't include all required settings for the direction
        """
        if direction == MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP:
            missing_details = []
            for detail in MimeoConfig.REQUIRED_HTTP_DETAILS:
                if detail not in output_details:
                    missing_details.append(detail)
            if len(missing_details) > 0:
                missing_details_str = ', '.join(missing_details)
                raise MissingRequiredProperty(f"Missing required fields is HTTP output details: {missing_details_str}")


class MimeoTemplate(MimeoDTO):
    """A MimeoDTO class representing Mimeo Template.

    It is a python representation of a Mimeo Template configuration node.

    Attributes
    ----------
    count : int
        A configured count of the Mimeo Template
    model : MimeoModel
        A configured model of the Mimeo Template
    """

    def __init__(self, template: dict):
        """Initialize MimeoTemplate class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        template : dict
            A source config template dictionary
        """
        super().__init__(template)
        MimeoTemplate._validate_template(template)
        self.count = template.get(MimeoConfig.TEMPLATES_COUNT_KEY)
        self.model = MimeoModel(template.get(MimeoConfig.TEMPLATES_MODEL_KEY))

    @staticmethod
    def _validate_template(template: dict) -> None:
        """Validate template in the source dictionary.

        Parameters
        ----------
        template : dict
            A source config template dictionary

        Raises
        ------
        IncorrectMimeoTemplate
            If the source config doesn't include count or model properties
        """
        if MimeoConfig.TEMPLATES_COUNT_KEY not in template:
            raise InvalidMimeoTemplate(f"No count value in the Mimeo Template: {template}")
        if MimeoConfig.TEMPLATES_MODEL_KEY not in template:
            raise InvalidMimeoTemplate(f"No model data in the Mimeo Template: {template}")


class MimeoModel(MimeoDTO):
    """A MimeoDTO class representing Mimeo Model.

    It is a python representation of a Mimeo Model configuration node.

    Attributes
    ----------
    root_name : str
        A root node's tag
    root_data : dict
        A template data
    context_name : str
        A context name (root_name by default)
    """

    def __init__(self, model: dict):
        """Initialize MimeoModel class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        model : dict
            A source config model dictionary
        """
        super().__init__(model)
        self.root_name = MimeoModel._get_root_name(model)
        self.root_data = model.get(self.root_name)
        self.context_name = MimeoModel._get_context_name(model, self.root_name)

    @staticmethod
    def _get_root_name(model: dict) -> str:
        """Extract a root name from the source dictionary.

        Parameters
        ----------
        model : dict
            A source config model dictionary

        Returns
        -------
        str
            The configured root node's tag

        Raises
        ------
        IncorrectMimeoModel
            If the source config has no or more than one root nodes
        """
        model_keys = [key for key in filter(MimeoModel._is_not_configuration_key, iter(model))]
        if len(model_keys) == 1:
            return model_keys[0]
        if len(model_keys) == 0:
            raise InvalidMimeoModel(f"No root data in Mimeo Model: {model}")
        elif len(model_keys) > 1:
            raise InvalidMimeoModel(f"Multiple root data in Mimeo Model: {model}")

    @staticmethod
    def _get_context_name(model: dict, root_name: str) -> str:
        """Extract a context name from the source dictionary.

        Parameters
        ----------
        model : dict
            A source config model dictionary
        root_name : str
            The configured root node's tag

        Returns
        -------
        str
            The configured context name.
            If the 'context' setting is missing returns root name by default

        Raises
        ------
        IncorrectMimeoModel
            If the source config has a context name not being a string value
        """
        context_name = model.get(MimeoConfig.MODEL_CONTEXT_KEY, root_name)
        if isinstance(context_name, str):
            return context_name
        else:
            raise InvalidMimeoModel(f"Invalid context name in Mimeo Model (not a string value): {model}")

    @staticmethod
    def _is_not_configuration_key(dict_key: str) -> bool:
        """Verify if the dictionary key is a configuration one.

        Parameters
        ----------
        dict_key : str
            A dictionary key to verify

        Returns
        -------
        bool
            True if the key is 'context', otherwise False
        """
        return dict_key not in [MimeoConfig.MODEL_CONTEXT_KEY]
