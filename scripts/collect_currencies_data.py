#!venv/bin/python3
"""The Currencies Data Collector module.

This module is meant to be executed as a script, but you can also
import its main() function to achieve the same goal.
The goal is to collect currencies data and adjust to the Mimeo usage.
Result of this script is src/mimeo/resources/currencies.csv file
and number of records updated in src/mimeo/database/currencies.py.
All source files are removed.
"""

from __future__ import annotations

import pandas
import utils

SOURCE_URL = "https://raw.githubusercontent.com/datasets/currency-codes/master/data/codes-all.csv"


def main():
    """Get currencies data."""
    print("Getting currencies data.")
    source_data_path = utils.download_file(SOURCE_URL)
    utils.adjust_data(source_data_path,
                      utils.MIMEO_DB_CURRENCIES,
                      utils.MIMEO_RESOURCES_CURRENCIES,
                      _modify_source_data)


def _modify_source_data(
        source_df: pandas.DataFrame,
) -> pandas.DataFrame:
    """Modify source data frame.

    This function introduces following modifications:
    * applies ASCII encoding on an Entity column
    * customizes Entity and capitalizes Entity values
    * removes rows with Entity starting with 'Zz'
    * removes rows having non-empty WithdrawalDate value
    * renames headers (
      AlphabeticCode -> CODE,
      Currency -> NAME,
      Entity -> COUNTRIES)
    * updates order of columns (CODE, NAME, COUNTRIES) and removes all remaining
    * drops duplicates
    * aggregates rows based on the CODE column
    * applies sorting by CODE column

    Parameters
    ----------
    source_df : pandas.DataFrame
        A source data frame

    Returns
    -------
    currencies_df : pandas.DataFrame
        A modified data frame
    """
    columns_mapping = {
        "AlphabeticCode": "CODE",
        "Currency": "NAME",
        "Entity": "COUNTRIES",
    }
    sort_column = "CODE"

    source_df["Entity"] = (
        utils.apply_ascii_encoding_on_column(source_df, "Entity")
        .map(_apply_specific_countries_modifications)
        .str.title())
    source_df = source_df[~source_df["Entity"].str.startswith("Zz")]
    currencies_df = (
        source_df
        .loc[source_df["WithdrawalDate"].isna()]
        .rename(columns=columns_mapping)
        .loc[:, columns_mapping.values()]
        .drop_duplicates()
        .groupby("CODE")
        .agg({"CODE": "first", "NAME": "first", "COUNTRIES": lambda c: list(c)})
        .reset_index(drop=True)
        .sort_values(sort_column))
    print("Currencies data has been prepared.")
    return currencies_df


def _apply_specific_countries_modifications(
        country: str,
) -> str:
    """Modify a country name.

    This function introduces following modifications:
    * gets rid of " (THE)" suffix
    * replaces an extended form of the United Kingdom name

    Parameters
    ----------
    country : str
        A country name

    Returns
    -------
    country : str
        A modified country name
    """
    country = country.replace(
        " (THE)",
        "")
    country = country.replace(
        "UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND",
        "UNITED KINGDOM")
    return country


if __name__ == "__main__":
    main()
