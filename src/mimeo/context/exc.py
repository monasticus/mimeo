class MinimumIdentifierReached(Exception):
    """
    Raised when using MimeoContext.prev_id() method
    and id is equal to 0.
    """

    def __init__(self):
        """Extends Exception constructor with a constant message"""

        super().__init__("There's no previous ID!")


class UninitializedContextIteration(Exception):
    """
    Raised while attempting to access the current iteration
    without prior initialization.
    """

    def __init__(self, context_name: str):
        """Extends Exception constructor with a custom message.

        Parameters
        ----------
        context_name : str
            A current context name
        """

        super().__init__(f"No iteration has been initialized for the current context [{context_name}]")


class ContextIterationNotFound(Exception):
    """
    Raised while attempting to access an iteration that does not exist.
    """

    def __init__(self, iteration_id: int, context_name: str):
        """Extends Exception constructor with a custom message.

        Parameters
        ----------
        iteration_id : int
            A current context name
        context_name : str
            A current context name
        """

        super().__init__(f"No iteration with id [{iteration_id}] "
                         f"has been initialized for the current context [{context_name}]")


class InvalidSpecialFieldName(Exception):
    """
    Raised while attempting to save a special field and provided name
    is not a string value.
    """

    def __init__(self):
        """Extends Exception constructor with a constant message"""

        super().__init__("A special field name needs to be a string value!")


class InvalidSpecialFieldValue(Exception):
    """
    Raised while attempting to save a special field and provided value
    is non-atomic one.
    """

    def __init__(self, field_value):
        """Extends Exception constructor with a custom message.

        Parameters
        ----------
        field_value : str
            A special field value
        """

        super().__init__(f"Provided field value [{field_value}] is invalid (use any atomic value)!")


class SpecialFieldNotFound(Exception):
    """
    Raised while attempting to access a special field that
    does not exist.
    """

    def __init__(self, field_name: str):
        """Extends Exception constructor with a custom message.

        Parameters
        ----------
        field_name : str
            A special field name
        """

        super().__init__(f"Special Field [{field_name}] has not been found!")


class VarNotFound(Exception):
    """
    Raised while attempting to access a variable that does not exist.
    """

    def __init__(self, variable_name: str):
        """Extends Exception constructor with a custom message.

        Parameters
        ----------
        variable_name : str
            A variable name
        """

        super().__init__(f"Provided variable [{variable_name}] is not defined!")
