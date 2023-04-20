class MinimumIdentifierReached(Exception):
    """
    Raised when using MimeoContext.prev_id() method
    and id is equal to 0.
    """

    pass


class UninitializedContextIteration(Exception):
    """
    Raised while attempting to access the current iteration
    without prior initialization.
    """

    pass


class ContextIterationNotFound(Exception):
    """
    Raised while attempting to access an iteration that does not exist.
    """

    pass


class InvalidSpecialFieldName(Exception):
    """
    Raised while attempting to save a special field and provided name
    is not a string value.
    """

    pass


class InvalidSpecialFieldValue(Exception):
    """
    Raised while attempting to save a special field and provided value
    is non-atomic one.
    """

    pass


class SpecialFieldNotFound(Exception):
    """
    Raised while attempting to access a special field that
    does not exist.
    """

    pass


class VarNotFound(Exception):
    """
    Raised while attempting to access a variable that does not exist.
    """

    pass
