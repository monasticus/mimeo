"""The Scripts Utils module.

This module contains all functions and constants being useful in
retrieving data to Mimeo Database.

It exports the following constants:
    * MIMEO_DB_PACKAGE
        A Mimeo Database package path
    * MIMEO_DB_CITIES
        A Mimeo Cities module file name
    * MIMEO_DB_COUNTRIES
        A Mimeo Countries module file name
    * MIMEO_DB_CURRENCIES
        A Mimeo Currencies module file name
    * MIMEO_DB_FORENAMES
        A Mimeo First Names module file name
    * MIMEO_DB_SURNAMES
        A Mimeo Last Names module file name
    * MIMEO_RESOURCES_PACKAGE
        A Mimeo Resources package path
    * MIMEO_RESOURCES_CITIES
        A cities CSV file name
    * MIMEO_RESOURCES_COUNTRIES
        A countries CSV file name
    * MIMEO_RESOURCES_CURRENCIES
        A currencies CSV file name
    * MIMEO_RESOURCES_FORENAMES
        A forenames CSV file name
    * MIMEO_RESOURCES_SURNAMES
        A surnames text file name

It exports the following functions:
    * download_file
        Download a file from `url`.
    * extract_zip_data
        Extract data from ZIP file.
    * remove_file
        Remove a file if it exists.
    * adjust_data
        Adjust source data for Mimeo usage.
    * dump_to_database
        Save data frame to a file.
    * overwrite_num_of_records
        Overwrite a number of records in Mimeo Database package.
    * apply_ascii_encoding_on_column
        Apply ASCII encoding on a specific data frame's column.
    * apply_ascii_encoding
        Apply ASCII encoding.
"""
from __future__ import annotations

import re
import unicodedata
import zipfile
from pathlib import Path
from typing import Callable

import pandas
from requests import Session

MIMEO_DB_PACKAGE = "src/mimeo/database"
MIMEO_DB_CITIES = "cities.py"
MIMEO_DB_COUNTRIES = "countries.py"
MIMEO_DB_CURRENCIES = "currencies.py"
MIMEO_DB_FORENAMES = "first_names.py"
MIMEO_DB_SURNAMES = "last_names.py"

MIMEO_RESOURCES_PACKAGE = "src/mimeo/resources"
MIMEO_RESOURCES_CITIES = "cities.csv"
MIMEO_RESOURCES_COUNTRIES = "countries.csv"
MIMEO_RESOURCES_CURRENCIES = "currencies.csv"
MIMEO_RESOURCES_FORENAMES = "forenames.csv"
MIMEO_RESOURCES_SURNAMES = "surnames.txt"


def download_file(url: str) -> str:
    """Download a file from `url`.

    Parameters
    ----------
    url : str
        URL to download data from.

    Returns
    -------
    target_path : str
        A file name (same as the source file)
    """
    print(f"Downloading a file from {url}.")
    target_path = url.split("/")[-1]
    remove_file(target_path)

    with Session() as sess:
        resp = sess.get(url, stream=True)
        with Path(target_path).open("wb") as output:
            for chunk in resp.iter_content(chunk_size=128):
                output.write(chunk)
    print(f"Writing a file: {target_path}")
    return target_path


def extract_zip_data(zip_path: str, files_to_extract: list = None):
    """Extract data from ZIP file.

    Parameters
    ----------
    zip_path : str
        A ZIP file path
    files_to_extract : list
        A list of files to extract from zip
    """
    print(f"Extracting files {files_to_extract} from {zip_path}.")
    for file_name in files_to_extract:
        file_path = f"{file_name}"
        remove_file(file_path)

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(members=files_to_extract)


def remove_file(
        file_path: str,
):
    """Remove a file if it exists."""
    if Path(file_path).exists():
        print(f"Removing file: {file_path}.")
        Path(file_path).unlink()


def adjust_data(
        source_data_path: str,
        target_db: str,
        target_file_name: str,
        modify: Callable,
):
    """Adjust source data for Mimeo usage.

    Once data is modified, it saves it and overwrites number of records
    in a corresponding Mimeo Database module. The source file is
    removed at the end.

    Parameters
    ----------
    source_data_path : str
        A source file path
    target_db : str
        A module of Mimeo Database package to update number of records
    target_file_name : str
        A target file name
    modify : Callable
        A function modifying source data
    """
    print(f"Adjusting source data [{source_data_path}].")
    source_df = pandas.read_csv(source_data_path)
    target_df = modify(source_df)

    dump_to_database(target_df, target_file_name)
    overwrite_num_of_records(target_db, target_df)
    remove_file(source_data_path)


def dump_to_database(data_frame: pandas.DataFrame, target_file: str):
    """Save data frame to a file.

    If the `target_file` is not a CSV file, then header will not be
    included.

    Parameters
    ----------
    data_frame : pandas.DataFrame
        A data frame to dump
    target_file
        A target file name
    """
    target_path = f"{MIMEO_RESOURCES_PACKAGE}/{target_file}"
    print(f"Saving data to {target_path}")
    data_frame.to_csv(target_path, index=False, header=target_file.endswith(".csv"))


def overwrite_num_of_records(mimeo_db: str, data_frame: pandas.DataFrame):
    """Overwrite a number of records in Mimeo Database package.

    Parameters
    ----------
    mimeo_db : str
        A module of Mimeo Database package
    data_frame : pandas.DataFrame
        A data frame to count number of records
    """
    print(f"Updating number of records in {mimeo_db}")
    num_of_records = len(data_frame.index)
    if mimeo_db in [MIMEO_DB_CITIES, MIMEO_DB_COUNTRIES, MIMEO_DB_CURRENCIES,
                    MIMEO_DB_FORENAMES, MIMEO_DB_SURNAMES]:
        mimeo_db_path = f"{MIMEO_DB_PACKAGE}/{mimeo_db}"
        with Path(mimeo_db_path).open() as module_file:
            module = module_file.read()

        curr_num_of_records = re.compile("NUM_OF_RECORDS = (.*)").findall(module)[0]
        if int(curr_num_of_records) == num_of_records:
            print(f"Number of records [{num_of_records}] has not been changed.")
        else:
            module = re.sub(r"NUM_OF_RECORDS = .*",
                            f"NUM_OF_RECORDS = {num_of_records}",
                            module)
            with Path(mimeo_db_path).open("w") as module_file:
                module_file.write(module)
            print("Number of records has been updated "
                  f"[{curr_num_of_records} -> {num_of_records}].")
    else:
        print("Number of records has not been overwritten "
              f"as {mimeo_db} is not a registered Mimeo Database.")


def apply_ascii_encoding_on_column(
        data_frame: pandas.DataFrame,
        column_name: str,
) -> pandas.Series:
    """Apply ASCII encoding on a specific data frame's column."""
    return data_frame[column_name].apply(apply_ascii_encoding)


def apply_ascii_encoding(
        value: str,
) -> str:
    """Apply ASCII encoding."""
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
