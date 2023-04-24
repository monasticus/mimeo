class UnsupportedPropertyValue(Exception):
    """
    Raised when a Mimeo Configuration property points to a value
    not being supported by Mimeo.
    """

    def __init__(self, prop: str, val: str, supported_values: tuple):
        """Extends Exception constructor with a custom message.

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
    """
    Raised when a Mimeo Configuration does not contain a required
    property.
    """

    pass


class InvalidIndent(Exception):
    """
    Raised when a configured indent is negative.
    """

    def __init__(self, indent: int):
        """Extends Exception constructor with a custom message.

        Parameters
        ----------
        indent : int
            A configured indent
        """

        super().__init__(f"Provided indent [{indent}] is negative!")


class InvalidVars(Exception):
    """
    Raised when vars are not configured properly.
    """

    pass


class InvalidMimeoModel(Exception):
    """
    Raised when a Mimeo Model is not configured properly.
    """

    pass


class InvalidMimeoTemplate(Exception):
    """
    Raised when a Mimeo Template is not configured properly.
    """

    pass


class InvalidMimeoConfig(Exception):
    """
    Raised when a Mimeo Configuration is not configured properly.
    """

    pass
