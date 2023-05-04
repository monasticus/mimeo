"""The Mimeo Context Exceptions module.

It contains all custom exceptions related to Mimeo Context:
    * MinimumIdentifierReached
        A custom Exception class for reaching minimum identifier.
    * UninitializedContextIteration
        A custom Exception class for uninitialized context's iteration.
    * ContextIterationNotFound
        A custom Exception class for not found context's iteration.
    * InvalidSpecialFieldName
        A custom Exception class for invalid special field's name.
    * InvalidSpecialFieldValue
        A custom Exception class for invalid special field's value.
    * SpecialFieldNotFound
        A custom Exception class for not found special field.
    * VarNotFound
        A custom Exception class for not found var.
"""
from typing import Union


class MinimumIdentifierReached(Exception):
    """A custom Exception class for reaching minimum identifier.

    Raised when using MimeoContext.prev_id() method and id is equal to
    0.
    """

    def __init__(self):
        """Initialize MinimumIdentifierReached exception with details.

        Extends Exception constructor with a constant message.
        """
        super().__init__("There's no previous ID!")


class UninitializedContextIteration(Exception):
    """A custom Exception class for uninitialized context's iteration.

    Raised while attempting to access the current iteration without
    prior initialization.
    """

    def __init__(self, context_name: str):
        """Initialize UninitializedContextIteration exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        context_name : str
            A current context name
        """
        super().__init__(f"No iteration has been initialized for the current context [{context_name}]")


class ContextIterationNotFound(Exception):
    """A custom Exception class for not found context's iteration.

    Raised while attempting to access an iteration that does not exist.
    """

    def __init__(self, iteration_id: int, context_name: str):
        """Initialize ContextIterationNotFound exception with details.

        Extends Exception constructor with a custom message.

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
    """A custom Exception class for invalid special field's name.

    Raised while attempting to save a special field and provided name
    is not a string value.
    """

    def __init__(self):
        """Initialize InvalidSpecialFieldName exception with details.

        Extends Exception constructor with a constant message.
        """
        super().__init__("A special field name needs to be a string value!")


class InvalidSpecialFieldValue(Exception):
    """A custom Exception class for invalid special field's value.

    Raised while attempting to save a special field and provided value
    is non-atomic one.
    """

    def __init__(self, field_value: Union[dict, list]):
        """Initialize InvalidSpecialFieldValue exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        field_value : Union[str, int, bool]
            A special field value
        """
        super().__init__(f"Provided field value [{field_value}] is invalid (use any atomic value)!")


class SpecialFieldNotFound(Exception):
    """A custom Exception class for not found special field.

    Raised while attempting to access a special field that does not
    exist.
    """

    def __init__(self, field_name: str):
        """Initialize SpecialFieldNotFound exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        field_name : str
            A special field name
        """
        super().__init__(f"Special Field [{field_name}] has not been found!")


class VarNotFound(Exception):
    """A custom Exception class for not found var.

    Raised while attempting to access a variable that does not exist.
    """

    def __init__(self, variable_name: str):
        """Initialize VarNotFound exception with details.

        Extends Exception constructor with a custom message.

        Parameters
        ----------
        variable_name : str
            A variable name
        """
        super().__init__(f"Provided variable [{variable_name}] is not defined!")
