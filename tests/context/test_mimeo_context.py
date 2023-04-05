import pytest

from mimeo.context import MimeoContext
from mimeo.context.exc import MinimumIdentifierReached


def test_next_id():
    ctx = MimeoContext()
    assert ctx.next_id() == 1
    assert ctx.next_id() == 2
    assert ctx.next_id() == 3


def test_curr_id():
    ctx = MimeoContext()
    ctx.next_id()
    assert ctx.curr_id() == 1

    ctx.next_id()
    assert ctx.curr_id() == 2

    ctx.next_id()
    assert ctx.curr_id() == 3


def test_prev_id():
    ctx = MimeoContext()
    ctx.next_id()
    ctx.next_id()
    ctx.next_id()
    ctx.next_id()
    assert ctx.prev_id() == 3
    assert ctx.prev_id() == 2
    assert ctx.prev_id() == 1


def test_prev_id_below_zero():
    ctx = MimeoContext()
    with pytest.raises(MinimumIdentifierReached) as err:
        ctx.prev_id()

    assert err.value.args[0] == "There's no previous ID!"


def test_next_iteration():
    ctx = MimeoContext()
    assert ctx.next_iteration() == 1
    assert ctx.next_iteration() == 2
    assert ctx.next_iteration() == 3


def test_curr_iteration():
    ctx = MimeoContext()
    ctx.next_iteration()
    assert ctx.curr_iteration() == 1

    ctx.next_iteration()
    assert ctx.curr_iteration() == 2

    ctx.next_iteration()
    assert ctx.curr_iteration() == 3
