from mimeo.context import MimeoContext
from mimeo.context.exc import (ContextIterationNotFoundError,
                               MinimumIdentifierReachedError,
                               UninitializedContextIterationError)
from mimeo.database import MimeoDB
from mimeo.database.exc import (DataNotFoundError, InvalidSexError,
                                OutOfStockError)
from tests.utils import assert_throws


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


@assert_throws(err_type=MinimumIdentifierReachedError,
               msg="There's no previous ID!")
def test_prev_id_below_zero():
    ctx = MimeoContext("SomeContext")
    ctx.prev_id()


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


@assert_throws(err_type=UninitializedContextIterationError,
               msg="No iteration has been initialized for the current context [{ctx}]",
               ctx="SomeContext")
def test_curr_iteration_id_without_initialization():
    ctx = MimeoContext("SomeContext")
    ctx.curr_iteration()


def test_get_iteration():
    ctx = MimeoContext("SomeContext")
    ctx.next_iteration()
    ctx.next_iteration()
    ctx.next_iteration()

    assert ctx.get_iteration(2).id == 2
    assert ctx.get_iteration(1).id == 1
    assert ctx.get_iteration(3).id == 3


@assert_throws(err_type=ContextIterationNotFoundError,
               msg="No iteration with id [{iter}] has been initialized "
                   "for the current context [{ctx}]",
               iter=1, ctx="SomeContext")
def test_get_iteration_id_without_initialization():
    ctx = MimeoContext("SomeContext")
    ctx.get_iteration(1)


def test_clear_iterations():
    ctx = MimeoContext("SomeContext")
    assert ctx.next_iteration().id == 1
    assert ctx.next_iteration().id == 2
    assert ctx.next_iteration().id == 3

    ctx.clear_iterations()
    assert ctx.next_iteration().id == 1
    assert ctx.next_iteration().id == 2
    assert ctx.next_iteration().id == 3


def test_next_country_index():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_COUNTRIES):
        country_index = ctx.next_country_index()
        assert country_index >= 0
        assert country_index < MimeoDB.NUM_OF_COUNTRIES


@assert_throws(err_type=OutOfStockError,
               msg="No more unique values, database contain only {c} countries.",
               c=239)
def test_next_country_index_out_of_stock():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_COUNTRIES):
        ctx.next_country_index()

    ctx.next_country_index()


def test_next_city_index_default():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_CITIES):
        city_index = ctx.next_city_index()
        assert city_index >= 0
        assert city_index < MimeoDB.NUM_OF_CITIES


@assert_throws(err_type=OutOfStockError,
               msg="No more unique values, database contain only {c} cities.",
               c=42904)
def test_next_city_index_default_out_of_stock():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_CITIES):
        ctx.next_city_index()

    ctx.next_city_index()


def test_next_city_index_custom_country():
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in mimeo_db.get_cities_of("United Kingdom")]
    cities_count = len(cities)

    ctx = MimeoContext("SomeContext")
    for _ in range(cities_count):
        city_index = ctx.next_city_index("United Kingdom")
        assert city_index >= 0
        assert city_index < cities_count


@assert_throws(err_type=OutOfStockError,
               msg="No more unique values, database contain only {c} cities of "
                   "{country}.",
               c=858, country="United Kingdom")
def test_next_city_index_custom_country_out_of_stock():
    mimeo_db = MimeoDB()
    cities = [city.name_ascii for city in mimeo_db.get_cities_of("United Kingdom")]
    cities_count = len(cities)

    ctx = MimeoContext("SomeContext")
    for _ in range(cities_count):
        ctx.next_city_index("United Kingdom")

    ctx.next_city_index("United Kingdom")


@assert_throws(err_type=DataNotFoundError,
               msg="Mimeo database doesn't contain any city of the provided "
                   "country [{country}].",
               country="NEC")
def test_next_city_index_non_existing_country():
    ctx = MimeoContext("SomeContext")
    ctx.next_city_index("NEC")


def test_next_currency_index():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_CURRENCIES):
        currency_index = ctx.next_currency_index()
        assert currency_index >= 0
        assert currency_index < MimeoDB.NUM_OF_CURRENCIES


@assert_throws(err_type=OutOfStockError,
               msg="No more unique values, database contain only {c} currencies.",
               c=169)
def test_next_currency_index_out_of_stock():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_CURRENCIES):
        ctx.next_currency_index()

    ctx.next_currency_index()


def test_next_first_name_index_default():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_FIRST_NAMES):
        first_name_index = ctx.next_first_name_index()
        assert first_name_index >= 0
        assert first_name_index < MimeoDB.NUM_OF_FIRST_NAMES


@assert_throws(err_type=OutOfStockError,
               msg="No more unique values, database contain only {c} first names.",
               c=7455)
def test_next_first_name_index_default_out_of_stock():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_FIRST_NAMES):
        ctx.next_first_name_index()

    ctx.next_first_name_index()


def test_next_first_name_index_custom_sex():
    mimeo_db = MimeoDB()
    first_names = [n.name for n in mimeo_db.get_first_names_by_sex("M")]
    first_names_count = len(first_names)

    ctx = MimeoContext("SomeContext")
    for _ in range(first_names_count):
        first_name_index = ctx.next_first_name_index("M")
        assert first_name_index >= 0
        assert first_name_index < first_names_count


@assert_throws(err_type=OutOfStockError,
               msg="No more unique values, database contain only {c} male "
                   "first names.",
               c=3437)
def test_next_first_name_index_male_sex_out_of_stock():
    mimeo_db = MimeoDB()
    first_names = [n.name for n in mimeo_db.get_first_names_by_sex("M")]
    first_names_count = len(first_names)

    ctx = MimeoContext("SomeContext")
    for _ in range(first_names_count):
        ctx.next_first_name_index("M")

    ctx.next_first_name_index("M")


@assert_throws(err_type=OutOfStockError,
               msg="No more unique values, database contain only {c} female "
                   "first names.",
               c=4018)
def test_next_first_name_index_female_sex_out_of_stock():
    mimeo_db = MimeoDB()
    first_names = [n.name for n in mimeo_db.get_first_names_by_sex("F")]
    first_names_count = len(first_names)

    ctx = MimeoContext("SomeContext")
    for _ in range(first_names_count):
        ctx.next_first_name_index("F")

    ctx.next_first_name_index("F")


@assert_throws(err_type=InvalidSexError,
               msg="Invalid sex (use M / F)!")
def test_next_first_name_index_non_existing_sex():
    ctx = MimeoContext("SomeContext")
    ctx.next_first_name_index("N")


def test_next_last_name_index():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_LAST_NAMES):
        last_name_index = ctx.next_last_name_index()
        assert last_name_index >= 0
        assert last_name_index < MimeoDB.NUM_OF_LAST_NAMES


@assert_throws(err_type=OutOfStockError,
               msg="No more unique values, database contain only {c} last names.",
               c=151670)
def test_next_last_name_index_out_of_stock():
    ctx = MimeoContext("SomeContext")
    for _ in range(MimeoDB.NUM_OF_LAST_NAMES):
        ctx.next_last_name_index()

    ctx.next_last_name_index()
