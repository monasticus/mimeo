from mimeo.database import FirstNamesDB
from mimeo.database.exc import InvalidIndexError, InvalidSexError
from tests.utils import assert_throws


def test_get_first_names():
    first_names = FirstNamesDB.get_first_names()
    assert len(first_names) == FirstNamesDB.NUM_OF_RECORDS

    first_names.pop(0)
    assert len(first_names) == FirstNamesDB.NUM_OF_RECORDS - 1

    first_names = FirstNamesDB.get_first_names()
    assert len(first_names) == FirstNamesDB.NUM_OF_RECORDS


def test_get_first_name_at():
    with open("src/mimeo/resources/forenames.csv") as first_names:
        next(first_names)
        first_name_1_cols = next(first_names).rstrip().split(",")
        first_name_2_cols = next(first_names).rstrip().split(",")

    db = FirstNamesDB()

    first_name_1 = db.get_first_name_at(0)
    assert first_name_1.name == first_name_1_cols[0]
    assert first_name_1.sex == first_name_1_cols[1]

    first_name_2 = db.get_first_name_at(1)
    assert first_name_2.name == first_name_2_cols[0]
    assert first_name_2.sex == first_name_2_cols[1]


@assert_throws(err_type=InvalidIndexError,
               msg="Provided index [{i}] is out or the range: 0-7454!",
               params={"i": 9999})
def test_get_first_name_at_out_of_range():
    db = FirstNamesDB()
    db.get_first_name_at(9999)


def test_get_first_names_by_sex():
    db = FirstNamesDB()
    male_first_names = db.get_first_names_by_sex("M")

    for name in male_first_names:
        assert name.sex == "M"


@assert_throws(err_type=InvalidSexError,
               msg="Invalid sex (use M / F)!")
def test_get_first_names_by_sex_invalid():
    FirstNamesDB().get_first_names_by_sex("N")
