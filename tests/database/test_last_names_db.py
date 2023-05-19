from pathlib import Path

from mimeo.database import LastNamesDB
from mimeo.database.exc import InvalidIndexError
from tests.utils import assert_throws


def test_get_last_names():
    db = LastNamesDB()

    last_names = db.get_last_names()
    assert len(last_names) == LastNamesDB.NUM_OF_RECORDS

    last_names.pop(0)
    assert len(last_names) == LastNamesDB.NUM_OF_RECORDS - 1

    last_names = db.get_last_names()
    assert len(last_names) == LastNamesDB.NUM_OF_RECORDS


def test_get_last_name_at():
    with Path("src/mimeo/resources/surnames.txt").open() as last_names:
        last_name_1_source = next(last_names).rstrip()
        last_name_2_source = next(last_names).rstrip()

    db = LastNamesDB()

    last_name_1 = db.get_last_name_at(0)
    assert last_name_1 == last_name_1_source

    last_name_2 = db.get_last_name_at(1)
    assert last_name_2 == last_name_2_source


@assert_throws(err_type=InvalidIndexError,
               msg="Provided index [{i}] is out or the range: 0-151669!",
               i=151670)
def test_get_last_name_at_out_of_range():
    db = LastNamesDB()
    db.get_last_name_at(151670)
