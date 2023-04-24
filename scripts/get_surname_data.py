#!venv/bin/python3
import os

import pandas
from requests import Session


def main():
    source_url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/most-common-name/surnames.csv"
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
    create_last_names_data(source_df, data_dir)

    os.remove(file_name)


def create_last_names_data(source_df: pandas.DataFrame, data_dir: str):
    source_df["name"] = source_df["name"].str.title()
    columns_mapping = {
        "name": "NAME",
    }
    columns_order = ["NAME"]
    sort_column = "NAME"

    surnames_df = (
        source_df
        .rename(columns=columns_mapping)
        .loc[:, columns_order]
        .dropna()
        .sort_values(sort_column))

    surnames_file_name = "surnames.txt"
    surnames_df.to_csv(f"{data_dir}/{surnames_file_name}", index=False, header=False)


def remove_file_safely(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


if __name__ == "__main__":
    main()
