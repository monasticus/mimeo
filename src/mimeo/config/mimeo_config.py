"""The Mimeo Configuration module.

It contains classes representing Mimeo Configuration components
at all levels. All of them are Data Transfer Objects:
    * MimeoDTO
        A superclass for all Mimeo configuration DTOs
    * MimeoConfig
        A MimeoDTO class representing Mimeo Configuration
    * MimeoOutput
        A MimeoDTO class representing Mimeo Output Details
    * MimeoTemplate
        A MimeoDTO class representing Mimeo Template
    * MimeoModel
        A MimeoDTO class representing Mimeo Model
"""
from __future__ import annotations

import re

from mimeo.config import constants as cc
from mimeo.config.exc import (InvalidIndentError, InvalidMimeoConfigError,
                              InvalidMimeoModelError,
                              InvalidMimeoTemplateError, InvalidVarsError,
                              MissingRequiredPropertyError,
                              UnsupportedPropertyValueError)
from mimeo.logging import setup_logging

# setup logging when mimeo is used as a python library
setup_logging()


class MimeoDTO:
    """A superclass for all Mimeo configuration DTOs.

    It is meant to store a source dictionary for logging purposes.

    Methods
    -------
    __str__
        Return the stringified source dictionary of a DTO.
    """

    def __init__(
            self, source: dict,
    ):
        """Initialize MimeoDTO class.

        Parameters
        ----------
        source : dict
            The source dictionary for a Mimeo DTO
        """
        self._source = source

    def __str__(
            self,
    ):
        """Return the stringified source dictionary of a DTO."""
        return str(self._source)


class MimeoConfig(MimeoDTO):
    """A MimeoDTO class representing Mimeo Configuration.

    It is a python representation of a Mimeo Configuration file / dictionary.

    output : MimeoOutput, default {}
        A Mimeo Output Details settings
    vars : dict, default {}
        A Mimeo Configuration vars setting
    templates : list
        A Mimeo Templates setting
    """

    def __init__(
            self,
            config: dict,
    ):
        """Initialize MimeoConfig class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        config : dict
            A source config dictionary
        """
        super().__init__(config)
        self.output = MimeoOutput(config.get(cc.OUTPUT_KEY, {}))
        self.vars = self._get_vars(config)
        self.templates = self._get_templates(config)

    @classmethod
    def _get_vars(
            cls,
            config: dict,
    ) -> dict:
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
        InvalidVarsError
            If (1) the vars key does not point to a dictionary or
            (2) some variable's name does not start with a letter,
            is not SNAKE_UPPER_CASE with possible digits or
            (3) some variable's value points to non-atomic value nor Mimeo Util
        """
        variables = config.get(cc.VARS_KEY, {})
        if not isinstance(variables, dict):
            raise InvalidVarsError(InvalidVarsError.Code.ERR_1, vars=variables)
        for var, val in variables.items():
            if isinstance(val, (list, dict)) and not cls._is_mimeo_util_object(val):
                raise InvalidVarsError(InvalidVarsError.Code.ERR_2, var=var)
            if not re.match(r"^[A-Z][A-Z_0-9]*$", var):
                raise InvalidVarsError(InvalidVarsError.Code.ERR_3, var=var)
        return variables

    @classmethod
    def _get_templates(
            cls,
            config: dict,
    ) -> list:
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
        InvalidMimeoConfigError
            If (1) the source dictionary does not include the _templates_ key or
            (2) the _templates_ key does not point to a list
        """
        templates = config.get(cc.TEMPLATES_KEY)
        if templates is None:
            raise InvalidMimeoConfigError(InvalidMimeoConfigError.Code.ERR_1,
                                          config=config)
        if not isinstance(templates, list):
            raise InvalidMimeoConfigError(InvalidMimeoConfigError.Code.ERR_2,
                                          config=config)
        return [MimeoTemplate(template)
                for template in config.get(cc.TEMPLATES_KEY)]

    @classmethod
    def _is_mimeo_util_object(
            cls,
            obj: dict,
    ) -> bool:
        """Verify if the object is a Mimeo Util.

        Parameters
        ----------
        obj : dict
            An object to verify

        Returns
        -------
        bool
            True if the object is a dictionary having only one key: _mimeo_util.
            Otherwise, False.
        """
        return (isinstance(obj, dict) and
                len(obj) == 1 and
                cc.MODEL_MIMEO_UTIL_KEY in obj)


class MimeoOutput(MimeoDTO):
    """A MimeoDTO class representing Mimeo Output Details.

    It is a python representation of a Mimeo Output Details configuration node.

    Attributes
    ----------
    direction : str, default 'file'
        The configured output direction
    format : str, default 'xml'
        A Mimeo Configuration output format setting
    xml_declaration : bool, default False
        A Mimeo Configuration xml declaration setting
    indent : int, default 0
        A Mimeo Configuration indent setting
    directory_path : str, default 'mimeo-output'
        The configured file output directory
    file_name : str, default 'mimeo-output-{}.{output_format}'
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
    username : str
        The configured http output username
    password : str
        The configured http output password
    """

    def __init__(
            self,
            output: dict,
    ):
        """Initialize MimeoOutput class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        output : dict
            A source config output details dictionary
        """
        super().__init__(output)
        self.direction = self._get_direction(output)
        self._validate_output(self.direction, output)
        self.format = self._get_format(output)
        self.xml_declaration = output.get(cc.OUTPUT_XML_DECLARATION_KEY, False)
        self.indent = self._get_indent(output)
        self.directory_path = self._get_directory_path(self.direction, output)
        self.file_name = self._get_file_name(self.direction, output, self.format)
        self.method = self._get_method(self.direction, output)
        self.protocol = self._get_protocol(self.direction, output)
        self.host = self._get_host(self.direction, output)
        self.port = self._get_port(self.direction, output)
        self.endpoint = self._get_endpoint(self.direction, output)
        self.username = self._get_username(self.direction, output)
        self.password = self._get_password(self.direction, output)

    @staticmethod
    def _get_direction(
            output: dict,
    ) -> str:
        """Extract output direction from the source dictionary.

        Parameters
        ----------
        output : dict
            A source config output details dictionary

        Returns
        -------
        direction : str
            The configured output direction

        Raises
        ------
        UnsupportedPropertyValueError
            If the configured output direction is not supported
        """
        direction = output.get(cc.OUTPUT_DIRECTION_KEY, cc.OUTPUT_DIRECTION_FILE)
        if direction not in cc.SUPPORTED_OUTPUT_DIRECTIONS:
            raise UnsupportedPropertyValueError(
                cc.OUTPUT_DIRECTION_KEY,
                direction,
                cc.SUPPORTED_OUTPUT_DIRECTIONS)
        return direction

    @staticmethod
    def _get_format(
            config: dict,
    ) -> str:
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
        UnsupportedPropertyValueError
            If the customized output format is not supported
        """
        output_format = config.get(cc.OUTPUT_FORMAT_KEY, cc.OUTPUT_FORMAT_XML)
        if output_format not in cc.SUPPORTED_OUTPUT_FORMATS:
            raise UnsupportedPropertyValueError(
                cc.OUTPUT_FORMAT_KEY,
                output_format,
                cc.SUPPORTED_OUTPUT_FORMATS)
        return output_format

    @staticmethod
    def _get_indent(
            config: dict,
    ) -> int:
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
        InvalidIndentError
            If the customized indent is lower than zero
        """
        indent = config.get(cc.OUTPUT_INDENT_KEY, 0)
        if indent < 0:
            raise InvalidIndentError(indent)
        return indent

    @staticmethod
    def _get_directory_path(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an output directory path from the source dictionary.

        It is extracted only when the output direction is 'file'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured output directory path when the output direction is 'file'.
            Otherwise, None. If the 'directory_path' setting is missing returns
            'mimeo-output' by default.
        """
        if direction == cc.OUTPUT_DIRECTION_FILE:
            return output.get(cc.OUTPUT_DIRECTORY_PATH_KEY, "mimeo-output")
        return None

    @staticmethod
    def _get_file_name(
            direction: str,
            output: dict,
            output_format: str,
    ) -> str | None:
        """Generate an output file name template based on the source dictionary.

        It is generated only when the output direction is 'file'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured output file name template when the output direction is
            'file'. Otherwise, None. If the 'file_name' setting is missing returns
            'mimeo-output-{}.{output_format}' by default.
        """
        if direction == cc.OUTPUT_DIRECTION_FILE:
            file_name = output.get(cc.OUTPUT_FILE_NAME_KEY, "mimeo-output")
            return f"{file_name}-{'{}'}.{output_format}"
        return None

    @staticmethod
    def _get_method(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP request method from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        method: str | None
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None. If the 'method' setting is missing returns
            'POST' by default.

        Raises
        ------
        UnsupportedPropertyValueError
            If the configured request method is not supported
        """
        method = None
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            method = output.get(cc.OUTPUT_METHOD_KEY, cc.OUTPUT_HTTP_REQUEST_POST)
            if method not in cc.SUPPORTED_REQUEST_METHODS:
                raise UnsupportedPropertyValueError(
                    cc.OUTPUT_METHOD_KEY,
                    method,
                    cc.SUPPORTED_REQUEST_METHODS)
        return method

    @staticmethod
    def _get_protocol(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP protocol from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None. If the 'protocol' setting is missing returns
            'http' by default.

        Raises
        ------
        UnsupportedPropertyValueError
            If the configured request protocol is not supported
        """
        protocol = None
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            protocol = output.get(cc.OUTPUT_PROTOCOL_KEY, cc.OUTPUT_PROTOCOL_HTTP)
            if protocol not in cc.SUPPORTED_REQUEST_PROTOCOLS:
                raise UnsupportedPropertyValueError(
                    cc.OUTPUT_PROTOCOL_KEY,
                    protocol,
                    cc.SUPPORTED_REQUEST_PROTOCOLS)
        return protocol

    @staticmethod
    def _get_host(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP host from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured HTTP host when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_HOST_KEY)
        return None

    @staticmethod
    def _get_port(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP port from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured HTTP port when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_PORT_KEY)
        return None

    @staticmethod
    def _get_endpoint(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract an HTTP endpoint from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured HTTP request method when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_ENDPOINT_KEY)
        return None

    @staticmethod
    def _get_username(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract a username from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured username when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_USERNAME_KEY)
        return None

    @staticmethod
    def _get_password(
            direction: str,
            output: dict,
    ) -> str | None:
        """Extract a password from the source dictionary.

        It is extracted only when the output direction is 'http'.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Returns
        -------
        str | None
            The configured password when the output direction is 'http'.
            Otherwise, None.
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            return output.get(cc.OUTPUT_PASSWORD_KEY)
        return None

    @staticmethod
    def _validate_output(
            direction: str,
            output: dict,
    ) -> None:
        """Validate output details in the source dictionary.

        The validation is being done according to the configured output
        direction.

        Parameters
        ----------
        direction : str
            The configured output direction
        output : dict
            A source config output details dictionary

        Raises
        ------
        MissingRequiredPropertyError
            If the output details doesn't include all required settings
            for the direction
        """
        if direction == cc.OUTPUT_DIRECTION_HTTP:
            missing_details = []
            for detail in cc.REQUIRED_HTTP_DETAILS:
                if detail not in output:
                    missing_details.append(detail)
            if len(missing_details) > 0:
                raise MissingRequiredPropertyError(missing_details)


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

    def __init__(
            self,
            template: dict,
    ):
        """Initialize MimeoTemplate class.

        Extends MimeoDTO constructor.

        Parameters
        ----------
        template : dict
            A source config template dictionary
        """
        super().__init__(template)
        self._validate_template(template)
        self.count = template.get(cc.TEMPLATES_COUNT_KEY)
        self.model = MimeoModel(template.get(cc.TEMPLATES_MODEL_KEY))

    @staticmethod
    def _validate_template(
            template: dict,
    ) -> None:
        """Validate template in the source dictionary.

        Parameters
        ----------
        template : dict
            A source config template dictionary

        Raises
        ------
        InvalidMimeoTemplateError
            If the source config doesn't include count or model properties
        """
        if cc.TEMPLATES_COUNT_KEY not in template:
            prop_name = "count"
            raise InvalidMimeoTemplateError(prop_name, template)
        if cc.TEMPLATES_MODEL_KEY not in template:
            prop_name = "model"
            raise InvalidMimeoTemplateError(prop_name, template)


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

    def __init__(
            self,
            model: dict,
    ):
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
    def _get_root_name(
            model: dict,
    ) -> str:
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
        InvalidMimeoModelError
            If the source config has no or more than one root nodes
        """
        model_keys = list(filter(MimeoModel._is_not_configuration_key, iter(model)))
        if len(model_keys) == 0:
            raise InvalidMimeoModelError(InvalidMimeoModelError.Code.ERR_1, model=model)
        if len(model_keys) > 1:
            raise InvalidMimeoModelError(InvalidMimeoModelError.Code.ERR_2, model=model)
        return model_keys[0]

    @staticmethod
    def _get_context_name(
            model: dict,
            root_name: str,
    ) -> str:
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
        InvalidMimeoModelError
            If the source config has a context name not being a string value
        """
        context_name = model.get(cc.MODEL_CONTEXT_KEY, root_name)
        if not isinstance(context_name, str):
            raise InvalidMimeoModelError(InvalidMimeoModelError.Code.ERR_3, model=model)
        return context_name

    @staticmethod
    def _is_not_configuration_key(
            dict_key: str,
    ) -> bool:
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
        return dict_key not in [cc.MODEL_CONTEXT_KEY]
