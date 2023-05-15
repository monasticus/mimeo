#!venv/bin/python3
"""The Currencies Data Collector module.

This module is meant to be executed as a script, but you can also
import its main() function to achieve the same goal.
The goal is to collect currencies data and adjust to the Mimeo usage.
Result of this script is src/mimeo/resources/currencies.csv file
and number of records updated in src/mimeo/database/currencies.py.
All source files are removed.
"""

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


def _modify_source_data(source_df: pandas.DataFrame) -> pandas.DataFrame:
    """Modify source data frame.

    This function introduces following modifications:
    * applies ASCII encoding on an Entity column
    * removes rows with Entity starting with 'ZZ'
    * renames headers (
      Entity -> COUNTRY,
      AlphabeticCode -> CODE,
      Currency -> NAME)
    * updates order of columns (COUNTRY, CODE, NAME) and removes all remaining
    * drops duplicates
    * applies sorting by COUNTRY column
    * capitalizes COUNTRY values

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
        "Entity": "COUNTRY",
        "AlphabeticCode": "CODE",
        "Currency": "NAME",
    }
    sort_column = "COUNTRY"

    source_df["Entity"] = utils.apply_ascii_encoding_on_column(source_df, "Entity")
    source_df = source_df[~source_df["Entity"].str.startswith("ZZ")]
    currencies_df = (
        source_df
        .loc[source_df["WithdrawalDate"].isna()]
        .rename(columns=columns_mapping)
        .loc[:, columns_mapping.values()]
        .drop_duplicates()
        .sort_values(sort_column))
    currencies_df["COUNTRY"] = currencies_df["COUNTRY"].str.title()
    print("Forenames data has been prepared.")
    return currencies_df


if __name__ == "__main__":
    main()
