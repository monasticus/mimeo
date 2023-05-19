"""The Mimeo Configuration Exceptions module.

It contains all custom exceptions related to Mimeo Configuration:
    * UnsupportedPropertyValueError
        A custom Exception class for unsupported properties' values.
    * MissingRequiredPropertyError
        A custom Exception class for missing required properties.
    * InvalidIndentError
        A custom Exception class for invalid indent configuration.
    * InvalidVarsError
        A custom Exception class for invalid vars' configuration.
    * InvalidVarsError.Code
        An Enumeration class for InvalidVarsError error codes.
    * InvalidMimeoModelError
        A custom Exception class for invalid model configuration.
    * InvalidMimeoTemplateError
        A custom Exception class for invalid template configuration.
    * InvalidMimeoConfigError
        A custom Exception class for invalid mimeo configuration.
"""


from __future__ import annotations

from enum import Enum


class UnsupportedPropertyValueError(Exception):
    """A custom Exception class for unsupported properties' values.

    Raised when a Mimeo Configuration property points to a value
    not being supported by Mimeo.
    """

    def __init__(
            self, prop: str, val: str, supported_values: tuple,
    ):
        """Initialize UnsupportedPropertyValueError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        prop : str
            A property name
        val : str
            A property value
        supported_values : tuple
            A list of supported values for the property
        """
        super().__init__(f"Provided {prop} [{val}] is not supported! "
                         f"Supported values: [{', '.join(supported_values)}].")


class MissingRequiredPropertyError(Exception):
    """A custom Exception class for missing required properties.

    Raised when a Mimeo Configuration does not contain a required
    property.
    """


class InvalidIndentError(Exception):
    """A custom Exception class for invalid indent configuration.

    Raised when a configured indent is negative.
    """

    def __init__(
            self,
            indent: int,
    ):
        """Initialize InvalidIndentError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        indent : int
            A configured indent
        """
        super().__init__(f"Provided indent [{indent}] is negative!")


class InvalidVarsError(Exception):
    """A custom Exception class for invalid vars' configuration.

    Raised when vars are not configured properly.
    """

    class Code(Enum):
        """An Enumeration class for InvalidVarsError error codes.

        Attributes
        ----------
        ERR_1: str
            An error code for vars not being a dictionary
        ERR_2: str
            An error code for vars with non-atomic values
        ERR_2: str
            An error code for vars with not allowed characters
        """

        ERR_1 = "NOT_A_DICT"
        ERR_2 = "COMPLEX_VALUE"
        ERR_3 = "INVALID_NAME"

    def __init__(
            self,
            code: InvalidVarsError.Code,
            **kwargs,
    ):
        """Initialize InvalidVarsError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal InvalidVarsError code.

        Parameters
        ----------
        code : InvalidVarsError.Code
            An internal error code
        kwargs
            An error details
        """
        msg = self._get_msg(code, kwargs)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: InvalidVarsError.Code,
            details: dict,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : InvalidVarsError.Code
            An internal error code
        details : dict
            An error details

        Returns
        -------
        str
            A custom error message

        Raises
        ------
        ValueError
            If the code argument is not InvalidVarsError.Code enum
        """
        if code == cls.Code.ERR_1:
            return f"vars property does not store an object: {details['vars']}"
        if code == cls.Code.ERR_2:
            return (f"Provided var [{details['var']}] is invalid "
                    f"(you can use ony atomic values and Mimeo Utils)!")
        if code == cls.Code.ERR_3:
            return (f"Provided var [{details['var']}] is invalid "
                    f"(you can use upper-cased name with underscore and digits, "
                    f"starting with a letter)!")

        msg = f"Provided error code is not a {cls.__name__}.Code enum!"
        raise ValueError(msg)


class InvalidMimeoModelError(Exception):
    """A custom Exception class for invalid model configuration.

    Raised when a Mimeo Model is not configured properly.
    """


class InvalidMimeoTemplateError(Exception):
    """A custom Exception class for invalid template configuration.

    Raised when a Mimeo Template is not configured properly.
    """


class InvalidMimeoConfigError(Exception):
    """A custom Exception class for invalid mimeo configuration.

    Raised when a Mimeo Configuration is not configured properly.
    """
