#!venv/bin/python3
from argparse import ArgumentParser
from pathlib import Path

FILE_DELIMITER = "-"


class GetPlaceParser(ArgumentParser):

    def __init__(self):
        super().__init__()
        self.add_argument(
            "-p",
            "--position",
            nargs="+",
            type=int,
            required=True,
            help="take positions to move examples forward")
        self.add_argument(
            "-d",
            "--directory",
            type=str,
            default="examples/2-mimeo-utils/",
            help="take a directory of examples to move")


def main():
    parser = GetPlaceParser()
    args = parser.parse_args()
    positions = _get_sorted_and_unique_positions(args.position)
    for position in positions:
        print(f"\nGetting place for example {position}.")
        with Path(args.directory) as examples_dir:
            for file in _get_sorted_files(examples_dir):
                file_name_components = file.name.split(FILE_DELIMITER)
                example_num = int(file_name_components[0])
                if example_num < position:
                    break
                new_file_name = _get_new_file_name(file_name_components)
                new_file_path = Path(file).with_name(new_file_name)
                print(f"{file} -> {new_file_path}")
                Path(file).rename(new_file_path)


def _get_sorted_and_unique_positions(
        positions: list
) -> list:
    positions = [*set(positions)]
    positions.sort()
    return positions


def _get_sorted_files(
        path: Path
) -> list:
    files = list(path.iterdir())
    files.sort(reverse=True)
    return files


def _get_new_file_name(
        file_name_components: list[str]
) -> str:
    example_num = int(file_name_components[0])
    new_example_num = example_num + 1
    new_file_name_components = [f"{new_example_num:02d}", *file_name_components[1:]]
    new_file_name = FILE_DELIMITER.join(new_file_name_components)
    return new_file_name


if __name__ == "__main__":
    main()
