#!venv/bin/python3
"""The Cities & Countries Data Collector module.

This module is meant to be executed as a script, but you can also
import its main() function to achieve the same goal.
The goal is to collect cities and countries data and adjust to
the Mimeo usage. Result of this script is cities.csv and countries.csv
files under src/mimeo/resources package, and number of records
updated in cities.py and countries.py of src/mimeo/database package.
All source files are removed.
"""
import unicodedata

import pandas
import utils

SOURCE_URL = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75.zip"
SOURCE_DATA_FILE = "worldcities.csv"
TARGET_CITIES_FILE = utils.MIMEO_RESOURCES_CITIES
TARGET_COUNTRIES_FILE = utils.MIMEO_RESOURCES_COUNTRIES


def main():
    """Get cities and countries data."""
    print("Getting cities and countries data.")
    zip_path = utils.download_file(SOURCE_URL)
    utils.extract_zip_data(zip_path, [SOURCE_DATA_FILE])
    utils.remove_file(zip_path)

    _adjust_data(SOURCE_DATA_FILE)


def _adjust_data(source_data_path: str):
    """Adjust source data for Mimeo usage.

    This function creates two files based on the source data. First,
    all useless columns are removed and then data is adjusted for
    cities and countries separately. Once data is modified, it saves it
    and overwrites number of records in corresponding Mimeo Database
    modules. The source file is removed at the end.

    Parameters
    ----------
    source_data_path : str
        A source file path
    """
    print(f"Adjusting source data [{source_data_path}].")
    source_df = pandas.read_csv(source_data_path)
    source_df = _preprocess_source_data(source_df)

    cities_df = _modify_source_data_for_cities(source_df)
    utils.dump_to_database(cities_df, TARGET_CITIES_FILE)
    utils.overwrite_num_of_records(utils.MIMEO_DB_CITIES, cities_df)

    countries_df = _modify_source_data_for_countries(source_df)
    utils.dump_to_database(countries_df, TARGET_COUNTRIES_FILE)
    utils.overwrite_num_of_records(utils.MIMEO_DB_COUNTRIES, countries_df)

    utils.remove_file(source_data_path)


def _preprocess_source_data(source_df: pandas.DataFrame) -> pandas.DataFrame:
    """Pre-process source data frame.

    This function introduces following modifications:
    * removes columns not being used nighter in cities nor countries

    Parameters
    ----------
    source_df : pandas.DataFrame
        A source data frame

    Returns
    -------
    source_df : pandas.DataFrame
        A modified data frame
    """
    print("Pre-processing source data.")
    columns_to_remove = ["lat", "lng", "admin_name", "capital", "population"]
    for col in columns_to_remove:
        del source_df[col]

    return source_df


def _modify_source_data_for_cities(source_df: pandas.DataFrame) -> pandas.DataFrame:
    """Modify source data frame.

    This function introduces following modifications:
    * renames headers (
      id -> ID,
      city -> CITY,
      city_ascii -> CITY_ASCII,
      iso3 -> COUNTRY)
    * updates order of columns (ID, CITY, CITY_ASCII, COUNTRY) and
      removes all remaining
    * applies sorting by ID column

    Parameters
    ----------
    source_df : pandas.DataFrame
        A source data frame

    Returns
    -------
    cities_df : pandas.DataFrame
        A modified data frame
    """
    columns_mapping = {
        "id": "ID",
        "city": "CITY",
        "city_ascii": "CITY_ASCII",
        "iso3": "COUNTRY"
    }
    columns_order = ["ID", "CITY", "CITY_ASCII", "COUNTRY"]
    sort_column = "ID"

    cities_df = (
        source_df
        .copy()
        .rename(columns=columns_mapping)
        .loc[:, columns_order]
        .sort_values(sort_column))
    print("Cities data has been prepared.")
    return cities_df


def _modify_source_data_for_countries(source_df: pandas.DataFrame) -> pandas.DataFrame:
    """Modify source data frame.

    This function introduces following modifications:
    * removes columns used only for cities (city, city_ascii, name)
    * drops duplicates
    * renames headers to uppercase (
      iso3 -> ISO_3,
      iso2 -> ISO_2,
      country -> NAME)
    * updates order of columns (ISO_3, ISO_2, NAME) and removes all
      remaining
    * applies sorting by ISO_3 column

    Parameters
    ----------
    source_df : pandas.DataFrame
        A source data frame

    Returns
    -------
    countries_df : pandas.DataFrame
        A modified data frame
    """
    columns_to_remove = ["city", "city_ascii", "id"]
    columns_mapping = {
        "iso3": "ISO_3",
        "iso2": "ISO_2",
        "country": "NAME"
    }
    sort_column = "ISO_3"

    countries_df = source_df.copy()
    for col in columns_to_remove:
        del countries_df[col]

    countries_df = (
        countries_df
        .drop_duplicates()
        .rename(columns=columns_mapping)
        .loc[:, columns_mapping.values()]
        .sort_values(sort_column))
    countries_df["NAME"] = countries_df["NAME"].apply(_ascii_encoding)
    print("Countries data has been prepared.")
    return countries_df


def _ascii_encoding(value: str):
    """Apply ASCII encoding."""
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode()


if __name__ == "__main__":
    main()
