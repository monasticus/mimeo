"""The Mimeo Utils Exceptions module.

It contains all custom exceptions related to Mimeo Utils:
    * InvalidMimeoUtil
        A custom Exception class for an invalid Mimeo Util.
    * InvalidValue
        A custom Exception class for an invalid value in Mimeo Util.
    * NotASpecialField
        A custom Exception class for a field used as a special.
"""


class InvalidMimeoUtil(Exception):
    """A custom Exception class for an invalid Mimeo Util.

    Raised when Mimeo Util node has missing _name property, or it
    does not match any Mimeo Util.
    """

    pass


class InvalidValue(Exception):
    """A custom Exception class for an invalid value in Mimeo Util.

    Raised when Mimeo Util node is incorrectly parametrized.
    """

    pass


class NotASpecialField(Exception):
    """A custom Exception class for a field used as a special.

    Raised while attempting to retrieve special field name when it is
    not a special one.
    """

    def __init__(self, field_name: str):
        """Initialize NotASpecialField exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        field_name : str
            A field name
        """
        super().__init__(f"Provided field [{field_name}] is not a special one (use {'{:NAME:}'})!")
