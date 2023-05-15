"""The Countries module.

It exports classes related to currencies CSV data:
    * Currency
        DTO class representing a single row in currencies CSV data.
"""
from __future__ import annotations


class Currency:
    """DTO class representing a single row in currencies CSV data.

    Attributes
    ----------
    code : str
        A currency code
    name : str
        A currency name
    countries : list
        A countries using the currency
    """

    def __init__(
            self,
            code: str,
            name: str,
            countries: list,
    ):
        """Initialize Currency class.

        Parameters
        ----------
        code : str
            A currency code
        name : str
            A currency name
        countries : list
            A countries using the currency
        """
        self.code = code
        self.name = name
        self.countries = countries

    def __str__(
            self,
    ) -> str:
        """Stringify the Currency instance.

        Returns
        -------
        str
            A stringified `dict` representation of the Currency instance
        """
        return str({
            "code": self.code,
            "name": self.name,
            "countries": self.countries,
        })

    def __repr__(
            self,
    ) -> str:
        """Represent the Currency instance.

        Returns
        -------
        str
            A python representation of the Currency instance
        """
        return (f"Currency("
                f"code='{self.code}', "
                f"name='{self.name}', "
                f"countries={self.countries})")
