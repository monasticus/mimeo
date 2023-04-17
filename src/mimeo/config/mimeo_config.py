import re

from mimeo.exceptions import (IncorrectMimeoConfig, IncorrectMimeoModel,
                              IncorrectMimeoTemplate, InvalidIndent,
                              InvalidVars, MissingRequiredProperty,
                              UnsupportedAuthMethod,
                              UnsupportedOutputDirection,
                              UnsupportedOutputFormat,
                              UnsupportedRequestMethod)
from mimeo.logging import setup_logging

# setup logging when mimeo is used as a python library
setup_logging()


class MimeoDTO:
    """A superclass for all Mimeo configuration DTOs

    It is meant to store a source dictionary for logging purposes.

    Methods
    -------
    __str__
        Returns the stringified source dictionary of a DTO
    """

    def __init__(self, source: dict):
        """
        Parameters
        ----------
        source : dict
            The source dictionary for a Mimeo DTO
        """
        self._source = source

    def __str__(self):
        """Returns the stringified source dictionary of a DTO"""
        return str(self._source)


class MimeoConfig(MimeoDTO):
    """A MimeoDTO class representing Mimeo Configuration

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
    OUTPUT_DETAILS_METHOD : str
        A Mimeo Configuration http method key
    OUTPUT_DETAILS_PROTOCOL : str
        A Mimeo Configuration http protocol key
    OUTPUT_DETAILS_HOST : str
        A Mimeo Configuration http host key
    OUTPUT_DETAILS_PORT : str
        A Mimeo Configuration http port key
    OUTPUT_DETAILS_ENDPOINT : str
        A Mimeo Configuration http endpoint key
    OUTPUT_DETAILS_AUTH : str
        A Mimeo Configuration http auth key
    OUTPUT_DETAILS_USERNAME : str
        A Mimeo Configuration http username key
    OUTPUT_DETAILS_PASSWORD : str
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
    OUTPUT_DETAILS_METHOD = "method"
    OUTPUT_DETAILS_PROTOCOL = "protocol"
    OUTPUT_DETAILS_HOST = "host"
    OUTPUT_DETAILS_PORT = "port"
    OUTPUT_DETAILS_ENDPOINT = "endpoint"
    OUTPUT_DETAILS_AUTH = "auth"
    OUTPUT_DETAILS_USERNAME = "username"
    OUTPUT_DETAILS_PASSWORD = "password"
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

    SUPPORTED_OUTPUT_FORMATS = ("xml",)

    def __init__(self, config: dict):
        """Extends MimeoDTO constructor

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
        """Extracts an output format from the source dictionary

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
        UnsupportedOutputFormat
            If the customized output format is not supported
        """

        output_format = config.get(MimeoConfig.OUTPUT_FORMAT_KEY, "xml")
        if output_format in MimeoConfig.SUPPORTED_OUTPUT_FORMATS:
            return output_format
        else:
            raise UnsupportedOutputFormat(f"Provided format [{output_format}] is not supported!")

    @staticmethod
    def _get_indent(config: dict) -> int:
        """Extracts an indent value from the source dictionary

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
            raise InvalidIndent(f"Provided indent [{indent}] is negative!")

    @staticmethod
    def _get_vars(config: dict) -> dict:
        """Extracts variables from the source dictionary

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
        """Extracts Mimeo Templates from the source dictionary

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
            raise IncorrectMimeoConfig(f"No templates in the Mimeo Config: {config}")
        elif not isinstance(templates, list):
            raise IncorrectMimeoConfig(f"_templates_ property does not store an array: {config}")
        else:
            return [MimeoTemplate(template) for template in config.get(MimeoConfig.TEMPLATES_KEY)]

    @staticmethod
    def _is_mimeo_util_object(obj: dict) -> bool:
        """Verifies if the object is a Mimeo Util

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
    """A MimeoDTO class representing Mimeo Output Details configuration

    It is a python representation of a Mimeo Output Details configuration node.

    Attributes
    ----------
    FILE_DIRECTION : str
        The 'file' output direction
    STD_OUT_DIRECTION : str
        The 'stdout' output direction
    HTTP_DIRECTION : str
        The 'http' output direction
    REQUEST_POST : str
        The 'POST' http request method
    REQUEST_PUT : str
        The 'PUT' http request method
    AUTH_BASIC : str
        The 'basic' http auth method
    AUTH_DIGEST : str
        The 'digest' http auth method
    SUPPORTED_OUTPUT_DIRECTIONS : set
        List of supported output directions
    SUPPORTED_REQUEST_METHODS : set
        List of supported http request methods
    SUPPORTED_AUTH_METHODS : set
        List of supported auth request methods
    REQUIRED_HTTP_DETAILS : set
        List of required http request output direction details

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

    FILE_DIRECTION = "file"
    STD_OUT_DIRECTION = "stdout"
    HTTP_DIRECTION = "http"

    REQUEST_POST = "POST"
    REQUEST_PUT = "PUT"

    AUTH_BASIC = "basic"
    AUTH_DIGEST = "digest"

    SUPPORTED_OUTPUT_DIRECTIONS = (STD_OUT_DIRECTION, FILE_DIRECTION, HTTP_DIRECTION)
    SUPPORTED_REQUEST_METHODS = (REQUEST_POST, REQUEST_PUT)
    SUPPORTED_AUTH_METHODS = (AUTH_BASIC, AUTH_DIGEST)
    REQUIRED_HTTP_DETAILS = (MimeoConfig.OUTPUT_DETAILS_HOST,
                             MimeoConfig.OUTPUT_DETAILS_ENDPOINT,
                             MimeoConfig.OUTPUT_DETAILS_USERNAME,
                             MimeoConfig.OUTPUT_DETAILS_PASSWORD)

    def __init__(self, output_format: str, output_details: dict):
        """Extends MimeoDTO constructor

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
        """Extracts output direction from the source dictionary

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
        UnsupportedOutputDirection
            If the configured output direction is not supported
        """

        direction = output_details.get(MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY, MimeoOutputDetails.FILE_DIRECTION)
        if direction in MimeoOutputDetails.SUPPORTED_OUTPUT_DIRECTIONS:
            return direction
        else:
            raise UnsupportedOutputDirection(f"Provided direction [{direction}] is not supported!")

    @staticmethod
    def _validate_output_details(direction: str, output_details: dict) -> None:
        """Validates output details in the source dictionary
        according to the configured output direction

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            missing_details = []
            for detail in MimeoOutputDetails.REQUIRED_HTTP_DETAILS:
                if detail not in output_details:
                    missing_details.append(detail)
            if len(missing_details) > 0:
                missing_details_str = ', '.join(missing_details)
                raise MissingRequiredProperty(f"Missing required fields is HTTP output details: {missing_details_str}")

    @staticmethod
    def _get_directory_path(direction: str, output_details: dict) -> str:
        """Extracts an output directory path from the source dictionary
        when the output direction is 'file'.

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

        if direction == MimeoOutputDetails.FILE_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_DIRECTORY_PATH_KEY, "mimeo-output")

    @staticmethod
    def _get_file_name_tmplt(direction: str, output_details: dict, output_format: str):
        """Generates an output file name template based on the source dictionary
        when the output direction is 'file'.

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

        if direction == MimeoOutputDetails.FILE_DIRECTION:
            file_name = output_details.get(MimeoConfig.OUTPUT_DETAILS_FILE_NAME_KEY, "mimeo-output")
            return f"{file_name}-{'{}'}.{output_format}"

    @staticmethod
    def _get_method(direction: str, output_details: dict) -> str:
        """Extracts an HTTP request method from the source dictionary
        when the output direction is 'http'.

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            method = output_details.get(MimeoConfig.OUTPUT_DETAILS_METHOD, "POST")
            if method in MimeoOutputDetails.SUPPORTED_REQUEST_METHODS:
                return method
            else:
                raise UnsupportedRequestMethod(f"Provided request method [{method}] is not supported!")

    @staticmethod
    def _get_protocol(direction: str, output_details: dict) -> str:
        """Extracts an HTTP protocol from the source dictionary
        when the output direction is 'http'.

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PROTOCOL, "http")

    @staticmethod
    def _get_host(direction: str, output_details: dict) -> str:
        """Extracts an HTTP host from the source dictionary
        when the output direction is 'http'.

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_HOST)

    @staticmethod
    def _get_port(direction: str, output_details: dict) -> str:
        """Extracts an HTTP port from the source dictionary
        when the output direction is 'http'.

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PORT)

    @staticmethod
    def _get_endpoint(direction: str, output_details: dict) -> str:
        """Extracts an HTTP endpoint from the source dictionary
        when the output direction is 'http'.

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_ENDPOINT)

    @staticmethod
    def _get_auth(direction: str, output_details: dict) -> str:
        """Extracts an HTTP auth method from the source dictionary
        when the output direction is 'http'.

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            auth = output_details.get(MimeoConfig.OUTPUT_DETAILS_AUTH, "basic")
            if auth in MimeoOutputDetails.SUPPORTED_AUTH_METHODS:
                return auth
            else:
                raise UnsupportedAuthMethod(f"Provided auth [{auth}] is not supported!")

    @staticmethod
    def _get_username(direction: str, output_details: dict) -> str:
        """Extracts a username from the source dictionary
        when the output direction is 'http'.

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_USERNAME)

    @staticmethod
    def _get_password(direction: str, output_details: dict) -> str:
        """Extracts a password from the source dictionary
        when the output direction is 'http'.

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

        if direction == MimeoOutputDetails.HTTP_DIRECTION:
            return output_details.get(MimeoConfig.OUTPUT_DETAILS_PASSWORD)


class MimeoTemplate(MimeoDTO):

    def __init__(self, template: dict):
        super().__init__(template)
        MimeoTemplate.__validate_template(template)
        self.count = template.get(MimeoConfig.TEMPLATES_COUNT_KEY)
        self.model = MimeoModel(template.get(MimeoConfig.TEMPLATES_MODEL_KEY))

    @staticmethod
    def __validate_template(template: dict):
        if MimeoConfig.TEMPLATES_COUNT_KEY not in template:
            raise IncorrectMimeoTemplate(f"No count value in the Mimeo Template: {template}")
        if MimeoConfig.TEMPLATES_MODEL_KEY not in template:
            raise IncorrectMimeoTemplate(f"No model data in the Mimeo Template: {template}")


class MimeoModel(MimeoDTO):

    def __init__(self, model: dict):
        super().__init__(model)
        self.root_name = MimeoModel.__get_root_name(model)
        self.root_data = model.get(self.root_name)
        self.context_name = MimeoModel.__get_context_name(model, self.root_name)

    @staticmethod
    def __get_root_name(model: dict) -> str:
        model_keys = [key for key in filter(MimeoModel.__is_not_metadata_key, iter(model))]
        if len(model_keys) == 1:
            return model_keys[0]
        if len(model_keys) == 0:
            raise IncorrectMimeoModel(f"No root data in Mimeo Model: {model}")
        elif len(model_keys) > 1:
            raise IncorrectMimeoModel(f"Multiple root data in Mimeo Model: {model}")

    @staticmethod
    def __is_not_metadata_key(dict_key: str) -> bool:
        return dict_key not in [MimeoConfig.MODEL_CONTEXT_KEY]

    @staticmethod
    def __get_context_name(model: dict, root_name: str) -> str:
        context_name = model.get(MimeoConfig.MODEL_CONTEXT_KEY, root_name)
        if isinstance(context_name, str):
            return context_name
        else:
            raise IncorrectMimeoModel(f"Invalid context name in Mimeo Model (not a string value): {model}")
