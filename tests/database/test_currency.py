from mimeo.database import Currency


def test_currency():
    currency = Currency("INR", "Indian Rupee", ["India", "Bhutan"])
    assert currency.code == "INR"
    assert currency.name == "Indian Rupee"
    assert currency.countries == ["India", "Bhutan"]


def test_str():
    currency = Currency("INR", "Indian Rupee", ["India", "Bhutan"])
    exp_str = ("{'code': 'INR', 'name': 'Indian Rupee',"
               " 'countries': ['India', 'Bhutan']}")
    assert currency.__str__() == exp_str


def test_repr():
    currency = Currency("INR", "Indian Rupee", ["India", "Bhutan"])
    exp_repr = ("Currency(code='INR', name='Indian Rupee', "
                "countries=['India', 'Bhutan'])")
    assert currency.__repr__() == exp_repr
