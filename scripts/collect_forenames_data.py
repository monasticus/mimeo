#!venv/bin/python3
"""The Forenames Data Collector module.

This module is meant to be executed as a script, but you can also
import its main() function to achieve the same goal.
The goal is to collect forenames data and adjust to the Mimeo usage.
Result of this script is src/mimeo/resources/forenames.csv file
and number of records updated in src/mimeo/database/first_names.py.
All source files are removed.
"""
from __future__ import annotations

import pandas
import utils

SOURCE_URL: str = "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv"


def main():
    """Get forenames data."""
    print("Getting forenames data.")
    source_data_path = utils.download_file(SOURCE_URL)
    utils.adjust_data(source_data_path,
                      utils.MIMEO_DB_FORENAMES,
                      utils.MIMEO_RESOURCES_FORENAMES,
                      _modify_source_data)


def _modify_source_data(
        source_df: pandas.DataFrame,
) -> pandas.DataFrame:
    """Modify source data frame.

    This function introduces following modifications:
    * renames headers to uppercase (name -> NAME, sex -> SEX)
    * updates order of columns (NAME, SEX) and removes all remaining
    * replaces SEX column values (boy -> M, girl -> F)
    * drops duplicates
    * applies sorting by NAME column

    Parameters
    ----------
    source_df : pandas.DataFrame
        A source data frame

    Returns
    -------
    forenames_df : pandas.DataFrame
        A modified data frame
    """
    columns_mapping = {
        "name": "NAME",
        "sex": "SEX",
    }
    sort_column = "NAME"

    forenames_df = (
        source_df
        .rename(columns=columns_mapping)
        .loc[:, columns_mapping.values()]
        .replace("boy", "M")
        .replace("girl", "F")
        .drop_duplicates()
        .sort_values(sort_column))
    print("Forenames data has been prepared.")
    return forenames_df


if __name__ == "__main__":
    main()
