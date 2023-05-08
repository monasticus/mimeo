from mimeo.database import Country


def test_country():
    country = Country("GBR", "GB", "United Kingdom")
    assert country.iso_3 == "GBR"
    assert country.iso_2 == "GB"
    assert country.name == "United Kingdom"


def test_str():
    country = Country("GBR", "GB", "United Kingdom")
    exp_str = "{'iso_3': 'GBR', 'iso_2': 'GB', 'name': 'United Kingdom'}"
    assert country.__str__() == exp_str


def test_repr():
    country = Country("GBR", "GB", "United Kingdom")
    exp_repr = "Country('GBR', 'GB', 'United Kingdom')"
    assert country.__repr__() == exp_repr
