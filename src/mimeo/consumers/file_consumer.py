from pathlib import Path

from mimeo.config.mimeo_config import MimeoOutputDetails
from mimeo.consumers import Consumer


class FileConsumer(Consumer):

    def __init__(self, output_details: MimeoOutputDetails):
        self.directory = output_details.directory_path
        self.output_path_tmplt = f"{self.directory}/{output_details.file_name_tmplt}"
        self.__directory_created = False
        self.__count = 0

    def consume(self, data: str) -> None:
        if not self.__directory_created:
            Path(self.directory).mkdir(parents=True, exist_ok=True)
        self.__count += 1
        with open(self.output_path_tmplt.format(self.__count), "w") as output_file:
            output_file.write(data)
