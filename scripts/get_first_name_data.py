#!venv/bin/python3
import os

import pandas
from requests import Session


def main():
    source_url = "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv"
    resource_file = download_csv(source_url)

    extract_path = "src/mimeo/resources"
    modify_data(extract_path, resource_file)


def download_csv(url: str):
    source_path = url.split("/")[-1]
    remove_file_safely(source_path)

    with Session() as sess:
        resp = sess.get(url, stream=True)
        with open(source_path, "wb") as output:
            for chunk in resp.iter_content(chunk_size=128):
                output.write(chunk)

    return source_path


def modify_data(data_dir: str, file_name: str):
    source_df = pandas.read_csv(file_name)
    create_first_names_data(source_df, data_dir)

    os.remove(file_name)


def create_first_names_data(source_df: pandas.DataFrame, data_dir: str):
    columns_mapping = {
        "name": "NAME",
        "sex": "SEX"
    }
    columns_order = ["NAME", "SEX"]
    sort_column = "NAME"

    cities_df = (
        source_df
        .rename(columns=columns_mapping)
        .loc[:, columns_order]
        .replace("boy", "M")
        .replace("girl", "F")
        .drop_duplicates()
        .sort_values(sort_column))

    cities_file_name = "firstnames.csv"
    cities_df.to_csv(f"{data_dir}/{cities_file_name}", index=False)


def remove_file_safely(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


if __name__ == "__main__":
    main()
