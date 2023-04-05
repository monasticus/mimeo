import pytest

from mimeo.context import MimeoContext
from mimeo.context.exc import (ContextIterationNotFound,
                               MinimumIdentifierReached, OutOfStock,
                               UninitializedContextIteration, CountryNotFound)
from mimeo.database import MimeoDB


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


def test_next_country_index():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_COUNTRIES):
        country_index = ctx.next_country_index()
        assert country_index >= 0
        assert country_index < MimeoDB.NUM_OF_COUNTRIES


def test_next_country_index_out_of_stock():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_COUNTRIES):
        ctx.next_country_index()

    with pytest.raises(OutOfStock) as err:
        ctx.next_country_index()
    assert err.value.args[0] == "No more unique values, database contain only 239 countries."


def test_next_city_index_default():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_CITIES):
        city_index = ctx.next_city_index()
        assert city_index >= 0
        assert city_index < MimeoDB.NUM_OF_CITIES


def test_next_city_index_default_out_of_stock():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_CITIES):
        ctx.next_city_index()

    with pytest.raises(OutOfStock) as err:
        ctx.next_city_index()
    assert err.value.args[0] == "No more unique values, database contain only 42905 cities."


def test_next_city_index_custom_country():
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in mimeo_db.get_cities_of("United Kingdom")]
    cities_count = len(cities)

    ctx = MimeoContext("SomeContext")
    for _ in range(cities_count):
        city_index = ctx.next_city_index("United Kingdom")
        assert city_index >= 0
        assert city_index < cities_count


def test_next_city_index_custom_country_default_out_of_stock():
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in mimeo_db.get_cities_of("United Kingdom")]
    cities_count = len(cities)

    ctx = MimeoContext("SomeContext")
    for _ in range(cities_count):
        ctx.next_city_index("United Kingdom")

    with pytest.raises(OutOfStock) as err:
        ctx.next_city_index("United Kingdom")
    assert err.value.args[0] == "No more unique values, database contain only 858 cities of United Kingdom."


def test_next_city_index_non_existing_country():
    ctx = MimeoContext("SomeContext")
    with pytest.raises(CountryNotFound) as err:
        ctx.next_city_index("NEC")

    assert err.value.args[0] == "Mimeo database does not contain any cities of provided country [NEC]."
