#!venv/bin/python3
import pandas
import utils

SOURCE_URL = "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv"
TARGET_FILE = utils.MIMEO_RESOURCES_FORENAMES


def main():
    print("Getting forenames data.")
    source_data_path = utils.download_file(SOURCE_URL)
    adjust_data(source_data_path)


def adjust_data(source_data_file: str):
    print(f"Adjusting source data [{source_data_file}].")
    source_df = pandas.read_csv(source_data_file)
    forenames_df = modify_source_data(source_df)

    utils.dump_to_database(forenames_df, TARGET_FILE)
    utils.overwrite_num_of_records(utils.MIMEO_DB_FORENAMES, forenames_df)
    utils.remove_file(source_data_file)


def modify_source_data(source_df: pandas.DataFrame):
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
