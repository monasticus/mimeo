import pytest

from mimeo.database import LastNamesDB
from mimeo.database.exc import InvalidIndex


def test_get_last_names():
    last_names = LastNamesDB.get_last_names()
    assert len(last_names) == LastNamesDB.NUM_OF_RECORDS

    last_names.pop(0)
    assert len(last_names) == LastNamesDB.NUM_OF_RECORDS - 1

    last_names = LastNamesDB.get_last_names()
    assert len(last_names) == LastNamesDB.NUM_OF_RECORDS


def test_get_last_name_at():
    with open("src/mimeo/resources/surnames.txt") as last_names:
        last_name_1_source = next(last_names).rstrip()
        last_name_2_source = next(last_names).rstrip()

    db = LastNamesDB()

    last_name_1 = db.get_last_name_at(0)
    assert last_name_1 == last_name_1_source

    last_name_2 = db.get_last_name_at(1)
    assert last_name_2 == last_name_2_source


def test_get_last_name_at_out_of_range():
    db = LastNamesDB()

    with pytest.raises(InvalidIndex) as err:
        db.get_last_name_at(151670)

    assert err.value.args[0] == "Provided index [151670] is out or the range: 0-151669!"
