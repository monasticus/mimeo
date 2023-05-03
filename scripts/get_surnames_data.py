#!venv/bin/python3
import pandas

import utils

SOURCE_URL = "https://raw.githubusercontent.com/fivethirtyeight/data/master/most-common-name/surnames.csv"
TARGET_FILE = utils.MIMEO_RESOURCES_SURNAMES


def main():
    print("Getting surnames data.")
    source_data_path = utils.download_file(SOURCE_URL)
    adjust_data(source_data_path)


def adjust_data(source_data_file: str):
    print(f"Adjusting source data [{source_data_file}].")
    source_df = pandas.read_csv(source_data_file)
    surnames_df = modify_source_data(source_df)

    utils.dump_to_database(surnames_df, TARGET_FILE)
    utils.overwrite_num_of_records(utils.MIMEO_DB_SURNAMES, surnames_df)
    utils.remove_file(source_data_file)


def modify_source_data(source_df: pandas.DataFrame):
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
    print("Surnames data has been prepared.")
    return surnames_df


if __name__ == "__main__":
    main()
