#!venv/bin/python3
"""The Surnames Data Collector module.

This module is meant to be executed as a script, but you can also
import its main() function to achieve the same goal.
The goal is to collect surnames data and adjust to the Mimeo usage.
Result of this script is src/mimeo/resources/surnames.txt file
and number of records updated in src/mimeo/database/last_names.py.
All source files are removed.
"""
import pandas
import utils

SOURCE_URL = "https://raw.githubusercontent.com/fivethirtyeight/data/master/most-common-name/surnames.csv"


def main():
    """Get surnames data."""
    print("Getting surnames data.")
    source_data_path = utils.download_file(SOURCE_URL)
    utils.adjust_data(source_data_path, utils.MIMEO_DB_SURNAMES, utils.MIMEO_RESOURCES_SURNAMES, _modify_source_data)


def _modify_source_data(source_df: pandas.DataFrame) -> pandas.DataFrame:
    """Modify source data frame.

    This function introduces following modifications:
    * removes all columns except 'name'
    * drops duplicates
    * applies sorting
    * capitalizes values

    Parameters
    ----------
    source_df : pandas.DataFrame
        A source data frame

    Returns
    -------
    surnames_df : pandas.DataFrame
        A modified data frame
    """
    columns_order = ["name"]
    sort_column = "name"

    surnames_df = (
        source_df
        .loc[:, columns_order]
        .dropna()
        .sort_values(sort_column))
    surnames_df["name"] = surnames_df["name"].str.title()
    print("Surnames data has been prepared.")
    return surnames_df


if __name__ == "__main__":
    main()
