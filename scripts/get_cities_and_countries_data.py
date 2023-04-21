#!venv/bin/python3
import os
import unicodedata
import zipfile
from pathlib import Path

import pandas
from requests import Session


def main():
    source_url = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75.zip"
    zip_path = download_zip(source_url)

    extract_path = "src/mimeo/resources"
    resource_file = "worldcities.csv"
    extract_data(zip_path, extract_path, [resource_file])

    modify_data(extract_path, resource_file)


def download_zip(url: str):
    zip_path = url.split("/")[-1]
    remove_file_safely(zip_path)

    with Session() as sess:
        resp = sess.get(url, stream=True)
        with open(zip_path, "wb") as output:
            for chunk in resp.iter_content(chunk_size=128):
                output.write(chunk)

    return zip_path


def extract_data(zip_path: str, extract_path: str, extract_files: list):
    Path(extract_path).mkdir(parents=True, exist_ok=True)
    for file_name in extract_files:
        file_path = f"{extract_path}/{file_name}"
        remove_file_safely(file_path)

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(extract_path, extract_files)
    os.remove(zip_path)


def modify_data(data_dir: str, file_name: str):
    resource_path = f"{data_dir}/{file_name}"
    source_df = pandas.read_csv(resource_path)
    source_df = prepare_data(source_df)

    create_cities_data(source_df, data_dir)
    create_countries_data(source_df, data_dir)

    os.remove(resource_path)


def prepare_data(source_df: pandas.DataFrame) -> pandas.DataFrame:
    columns_to_remove = ["lat", "lng", "admin_name", "capital", "population"]
    for col in columns_to_remove:
        del source_df[col]

    return source_df


def create_cities_data(source_df: pandas.DataFrame, data_dir: str):
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

    cities_file_name = "cities.csv"
    cities_df.to_csv(f"{data_dir}/{cities_file_name}", index=False)


def create_countries_data(source_df: pandas.DataFrame, data_dir: str):
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

    countries_file_name = "countries.csv"
    countries_df.to_csv(f"{data_dir}/{countries_file_name}", index=False)


def ascii_encoding(value: str):
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode()


def remove_file_safely(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


if __name__ == "__main__":
    main()
