"""The Mimeo Utils Exceptions module.

It contains all custom exceptions related to Mimeo Utils:
    * InvalidMimeoUtilError
        A custom Exception class for an invalid Mimeo Util.
    * InvalidMimeoUtilError.Code
        A custom Enum class storing error codes for InvalidMimeoUtilError.
    * InvalidValueError
        A custom Exception class for an invalid value in Mimeo Util.
    * NotASpecialFieldError
        A custom Exception class for a field used as a special.
"""


from __future__ import annotations

from enum import Enum


class InvalidMimeoUtilError(Exception):
    """A custom Exception class for an invalid Mimeo Util.

    Raised when Mimeo Util node has missing _name property, or it
    does not match any Mimeo Util.
    """

    class Code(Enum):
        """An Enumeration class for InvalidMimeoUtilError error codes.

        Attributes
        ----------
        ERR_1: int
            An error code for a missing Mimeo Util name in configuration
        ERR_2: int
            An error code for an unsupported Mimeo Util
        """

        ERR_1 = "MISSING_MIMEO_UTIL"
        ERR_2 = "UNSUPPORTED_MIMEO_UTIL"

    def __init__(
            self,
            code: InvalidMimeoUtilError.Code,
            details: dict | str,
    ):
        """Initialize InvalidMimeoUtilError exception with details.

        Extends Exception constructor with a custom message. The message depends on
        an internal InvalidMimeoUtilError code.

        Parameters
        ----------
        code : InvalidMimeoUtilError.Code
            An internal error code
        details : dict | str
            A Mimeo Util config for ERR_1, and a _name param for ERR_2
        """
        msg = self._get_msg(code, details)
        super().__init__(msg)

    @classmethod
    def _get_msg(
            cls,
            code: InvalidMimeoUtilError.Code,
            details: dict | str,
    ):
        """Return a custom message based on an error code.

        Parameters
        ----------
        code : InvalidMimeoUtilError.Code
            An internal error code
        details : dict | str
            A Mimeo Util config for ERR_1, and a _name param for ERR_2

        Returns
        -------
        str
            A custom error message

        Raises
        ------
        ValueError
            If the code argument is not InvalidMimeoUtilError.Code enum
        """
        if code == cls.Code.ERR_1:
            return f"Missing Mimeo Util name in configuration [{details}]!"
        if code == cls.Code.ERR_2:
            return f"No such Mimeo Util [{details}]!"

        msg = "Provided error code is not a InvalidMimeoUtilError.Code enum!"
        raise ValueError(msg)


class InvalidValueError(Exception):
    """A custom Exception class for an invalid value in Mimeo Util.

    Raised when Mimeo Util node is incorrectly parametrized.
    """


class NotASpecialFieldError(Exception):
    """A custom Exception class for a field used as a special.

    Raised while attempting to retrieve special field name when it is
    not a special one.
    """

    def __init__(
            self,
            field_name: str,
    ):
        """Initialize NotASpecialFieldError exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        field_name : str
            A field name
        """
        msg = f"Provided field [{field_name}] is not a special one (use {'{:NAME:}'})!"
        super().__init__(msg)
