from mimeo.database import FirstName


def test_first_name():
    first_name = FirstName('Dave', 'M')
    assert first_name.name == 'Dave'
    assert first_name.sex == 'M'


def test_str():
    first_name = FirstName('Dave', 'M')
    assert first_name.__str__() == "{'name': 'Dave', 'sex': 'M'}"


def test_repr():
    first_name = FirstName('Dave', 'M')
    assert first_name.__repr__() == "FirstName('Dave', 'M')"
