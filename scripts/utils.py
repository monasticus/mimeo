import os
import re
import zipfile

import pandas
from requests import Session

MIMEO_DB_PACKAGE = "src/mimeo/database"
MIMEO_DB_CITIES = "cities.py"
MIMEO_DB_COUNTRIES = "countries.py"
MIMEO_DB_FORENAMES = "first_names.py"
MIMEO_DB_SURNAMES = "last_names.py"

MIMEO_RESOURCES_PACKAGE = "src/mimeo/resources"
MIMEO_RESOURCES_CITIES = "cities.csv"
MIMEO_RESOURCES_COUNTRIES = "countries.csv"
MIMEO_RESOURCES_FORENAMES = "forenames.csv"
MIMEO_RESOURCES_SURNAMES = "surnames.txt"


def download_file(url: str):
    print(f"Downloading file from {url}.")
    target_path = url.split("/")[-1]
    remove_file(target_path)

    with Session() as sess:
        resp = sess.get(url, stream=True)
        with open(target_path, "wb") as output:
            for chunk in resp.iter_content(chunk_size=128):
                output.write(chunk)
    print(f"Writing file: {target_path}")
    return target_path


def extract_zip_data(zip_path: str, files_to_extract: list):
    print(f"Extracting files {files_to_extract} from {zip_path}.")
    for file_name in files_to_extract:
        file_path = f"{file_name}"
        remove_file(file_path)

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(members=files_to_extract)


def remove_file(file_path: str):
    if os.path.exists(file_path):
        print(f"Removing file: {file_path}.")
        os.remove(file_path)


def dump_to_database(data_frame: pandas.DataFrame, target_file: str):
    target_path = f"{MIMEO_RESOURCES_PACKAGE}/{target_file}"
    print(f"Saving data to {target_path}")
    data_frame.to_csv(target_path, index=False, header=target_file.endswith(".csv"))


def overwrite_num_of_records(mimeo_db: str, data_frame: pandas.DataFrame):
    print(f"Updating number of records in {mimeo_db}")
    num_of_records = len(data_frame.index)
    if mimeo_db in [MIMEO_DB_CITIES, MIMEO_DB_COUNTRIES, MIMEO_DB_FORENAMES, MIMEO_DB_SURNAMES]:
        mimeo_db_path = f"{MIMEO_DB_PACKAGE}/{mimeo_db}"
        with open(mimeo_db_path, "r") as module_file:
            module = module_file.read()

        curr_num_of_records = re.compile("NUM_OF_RECORDS = (.*)").findall(module)[0]
        if int(curr_num_of_records) == num_of_records:
            print(f"Number of records [{num_of_records}] has not been changed.")
        else:
            module = re.sub(r"NUM_OF_RECORDS = .*", f"NUM_OF_RECORDS = {num_of_records}", module)
            with open(mimeo_db_path, "w") as module_file:
                module_file.write(module)
            print(f"Number of records has been updated [{curr_num_of_records} -> {num_of_records}].")
    else:
        print(f"Number of records has not been overwritten as {mimeo_db} is not a registered Mimeo Database.")
