from mimeo.database import City


def test_city():
    city = City("1234", "London", "London", "GBR")
    assert city.id == 1234
    assert city.name == "London"
    assert city.name_ascii == "London"
    assert city.country == "GBR"


def test_str():
    city = City("1234", "London", "London", "GBR")
    exp_str = "{'id': 1234, 'name': 'London', 'name_ascii': 'London', 'country': 'GBR'}"
    assert city.__str__() == exp_str


def test_repr():
    city = City("1234", "London", "London", "GBR")
    exp_repr = "City(id='1234', name='London', name_ascii='London', country='GBR')"
    assert city.__repr__() == exp_repr
