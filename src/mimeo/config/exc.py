"""The Mimeo Configuration Exceptions module.

It contains all custom exceptions related to Mimeo Configuration:
    * UnsupportedPropertyValue
        A custom Exception class for unsupported properties' values.
    * MissingRequiredProperty
        A custom Exception class for missing required properties.
    * InvalidIndent
        A custom Exception class for invalid indent configuration.
    * InvalidVars
        A custom Exception class for invalid vars' configuration.
    * InvalidMimeoModel
        A custom Exception class for invalid model configuration.
    * InvalidMimeoTemplate
        A custom Exception class for invalid template configuration.
    * InvalidMimeoConfig
        A custom Exception class for invalid mimeo configuration.
"""


class UnsupportedPropertyValue(Exception):
    """A custom Exception class for unsupported properties' values.

    Raised when a Mimeo Configuration property points to a value
    not being supported by Mimeo.
    """

    def __init__(self, prop: str, val: str, supported_values: tuple):
        """Initialize UnsupportedPropertyValue exception with details.

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


class MissingRequiredProperty(Exception):
    """A custom Exception class for missing required properties.

    Raised when a Mimeo Configuration does not contain a required
    property.
    """

    pass


class InvalidIndent(Exception):
    """A custom Exception class for invalid indent configuration.

    Raised when a configured indent is negative.
    """

    def __init__(self, indent: int):
        """Initialize InvalidIndent exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        indent : int
            A configured indent
        """
        super().__init__(f"Provided indent [{indent}] is negative!")


class InvalidVars(Exception):
    """A custom Exception class for invalid vars' configuration.

    Raised when vars are not configured properly.
    """

    pass


class InvalidMimeoModel(Exception):
    """A custom Exception class for invalid model configuration.

    Raised when a Mimeo Model is not configured properly.
    """

    pass


class InvalidMimeoTemplate(Exception):
    """A custom Exception class for invalid template configuration.

    Raised when a Mimeo Template is not configured properly.
    """

    pass


class InvalidMimeoConfig(Exception):
    """A custom Exception class for invalid mimeo configuration.

    Raised when a Mimeo Configuration is not configured properly.
    """

    pass
