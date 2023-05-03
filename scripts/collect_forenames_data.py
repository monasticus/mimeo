#!venv/bin/python3
"""The Forenames Data Collector module.

This module is meant to be executed as a script, but you can also
import its main() function to achieve the same goal.
The goal is to collect forenames data and adjust to the Mimeo usage.
Result of this script is src/mimeo/resources/forenames.csv file
and number of records updated in src/mimeo/database/first_names.py.
All source files are removed.
"""
import pandas
import utils

SOURCE_URL = "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv"
TARGET_FILE = utils.MIMEO_RESOURCES_FORENAMES


def main():
    """Get forenames data."""
    print("Getting forenames data.")
    source_data_path = utils.download_file(SOURCE_URL)
    _adjust_data(source_data_path)


def _adjust_data(source_data_path: str):
    """Adjust source data for Mimeo usage.

    Once data is modified, it saves it and overwrites number of records
    in a corresponding Mimeo Database module. The source file is
    removed at the end.

    Parameters
    ----------
    source_data_path : str
        A source file path
    """
    print(f"Adjusting source data [{source_data_path}].")
    source_df = pandas.read_csv(source_data_path)
    forenames_df = _modify_source_data(source_df)

    utils.dump_to_database(forenames_df, TARGET_FILE)
    utils.overwrite_num_of_records(utils.MIMEO_DB_FORENAMES, forenames_df)
    utils.remove_file(source_data_path)


def _modify_source_data(source_df: pandas.DataFrame):
    """Modify source data frame.

    This function introduces following modifications:
    * renames headers to uppercase (name -> NAME, sex -> SEX)
    * updates order of columns (NAME, SEX)
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
        "sex": "SEX"
    }
    columns_order = ["NAME", "SEX"]
    sort_column = "NAME"

    forenames_df = (
        source_df
        .rename(columns=columns_mapping)
        .loc[:, columns_order]
        .replace("boy", "M")
        .replace("girl", "F")
        .drop_duplicates()
        .sort_values(sort_column))
    print("Forenames data has been prepared.")
    return forenames_df


if __name__ == "__main__":
    main()
