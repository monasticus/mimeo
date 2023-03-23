from mimeo.database import Country


def test_country():
    country = Country('GBR', 'GB', 'United Kingdom')
    assert country.iso_3 == 'GBR'
    assert country.iso_2 == 'GB'
    assert country.name == 'United Kingdom'


def test_str():
    country = Country('GBR', 'GB', 'United Kingdom')
    assert country.__str__() == "{'iso_3': 'GBR', 'iso_2': 'GB', 'name': 'United Kingdom'}"


def test_repr():
    country = Country('GBR', 'GB', 'United Kingdom')
    assert country.__repr__() == "Country('GBR', 'GB', 'United Kingdom')"
