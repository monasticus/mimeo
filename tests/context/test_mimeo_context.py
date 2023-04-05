import pytest

from mimeo.context import MimeoContext
from mimeo.context.exc import (ContextIterationNotFound,
                               MinimumIdentifierReached,
                               UninitializedContextIteration)


def test_next_id():
    ctx = MimeoContext("SomeContext")
    assert ctx.next_id() == 1
    assert ctx.next_id() == 2
    assert ctx.next_id() == 3


def test_curr_id():
    ctx = MimeoContext("SomeContext")
    ctx.next_id()
    assert ctx.curr_id() == 1

    ctx.next_id()
    assert ctx.curr_id() == 2

    ctx.next_id()
    assert ctx.curr_id() == 3


def test_prev_id():
    ctx = MimeoContext("SomeContext")
    ctx.next_id()
    ctx.next_id()
    ctx.next_id()
    ctx.next_id()
    assert ctx.prev_id() == 3
    assert ctx.prev_id() == 2
    assert ctx.prev_id() == 1


def test_prev_id_below_zero():
    ctx = MimeoContext("SomeContext")
    with pytest.raises(MinimumIdentifierReached) as err:
        ctx.prev_id()

    assert err.value.args[0] == "There's no previous ID!"


def test_next_iteration():
    ctx = MimeoContext("SomeContext")
    assert ctx.next_iteration().id == 1
    assert ctx.next_iteration().id == 2
    assert ctx.next_iteration().id == 3


def test_curr_iteration():
    ctx = MimeoContext("SomeContext")
    ctx.next_iteration()
    assert ctx.curr_iteration().id == 1

    ctx.next_iteration()
    assert ctx.curr_iteration().id == 2

    ctx.next_iteration()
    assert ctx.curr_iteration().id == 3


def test_curr_iteration_id_without_initialization():
    ctx = MimeoContext("SomeContext")
    with pytest.raises(UninitializedContextIteration) as err:
        ctx.curr_iteration()

    assert err.value.args[0] == "No iteration has been initialized for the current context [SomeContext]"


def test_get_iteration():
    ctx = MimeoContext("SomeContext")
    ctx.next_iteration()
    ctx.next_iteration()
    ctx.next_iteration()

    assert ctx.get_iteration(2).id == 2
    assert ctx.get_iteration(1).id == 1
    assert ctx.get_iteration(3).id == 3


def test_get_iteration_id_without_initialization():
    ctx = MimeoContext("SomeContext")
    with pytest.raises(ContextIterationNotFound) as err:
        ctx.get_iteration(1)

    assert err.value.args[0] == "No iteration with id [1] has been initialized for the current context [SomeContext]"
