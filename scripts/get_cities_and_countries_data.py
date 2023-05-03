#!venv/bin/python3
import unicodedata

import pandas
import utils

SOURCE_URL = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75.zip"
SOURCE_DATA_FILE = "worldcities.csv"
TARGET_CITIES_FILE = utils.MIMEO_RESOURCES_CITIES
TARGET_COUNTRIES_FILE = utils.MIMEO_RESOURCES_COUNTRIES


def main():
    print("Getting cities and countries data.")
    zip_path = utils.download_file(SOURCE_URL)
    utils.extract_zip_data(zip_path, [SOURCE_DATA_FILE])
    utils.remove_file(zip_path)

    adjust_data(SOURCE_DATA_FILE)


def adjust_data(source_data_file: str):
    print(f"Adjusting source data [{source_data_file}].")
    source_df = pandas.read_csv(source_data_file)
    source_df = prepare_data(source_df)

    cities_df = modify_source_data_for_cities(source_df)
    utils.dump_to_database(cities_df, TARGET_CITIES_FILE)
    utils.overwrite_num_of_records(utils.MIMEO_DB_CITIES, cities_df)

    countries_df = modify_source_data_for_countries(source_df)
    utils.dump_to_database(countries_df, TARGET_COUNTRIES_FILE)
    utils.overwrite_num_of_records(utils.MIMEO_DB_COUNTRIES, countries_df)

    utils.remove_file(source_data_file)


def prepare_data(source_df: pandas.DataFrame) -> pandas.DataFrame:
    print("Pre-processing source data.")
    columns_to_remove = ["lat", "lng", "admin_name", "capital", "population"]
    for col in columns_to_remove:
        del source_df[col]

    return source_df


def modify_source_data_for_cities(source_df: pandas.DataFrame):
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


def modify_source_data_for_countries(source_df: pandas.DataFrame):
    columns_to_remove = ["city", "city_ascii", "id"]
    columns_mapping = {
        "iso3": "ISO_3",
        "iso2": "ISO_2",
        "country": "NAME"
    }
    columns_order = ["ISO_3", "ISO_2", "NAME"]
    sort_column = "ISO_3"

    countries_df = source_df.copy()
    for col in columns_to_remove:
        del countries_df[col]

    countries_df = (
        countries_df
        .drop_duplicates()
        .rename(columns=columns_mapping)
        .loc[:, columns_order]
        .sort_values(sort_column))
    countries_df["NAME"] = countries_df["NAME"].apply(ascii_encoding)
    print("Countries data has been prepared.")
    return countries_df


def ascii_encoding(value: str):
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode()


if __name__ == "__main__":
    main()
