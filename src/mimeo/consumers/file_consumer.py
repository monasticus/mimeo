from pathlib import Path

from mimeo.consumers import Consumer
from mimeo.model.mimeo_config import MimeoOutputDetails


class FileConsumer(Consumer):

    def __init__(self, output_details: MimeoOutputDetails):
        self.directory = output_details.directory_path
        self.output_path_tmplt = f"{self.directory}/{output_details.file_name_tmplt}"
        self.directory_created = False
        self.count = 0

    def consume(self, data: str) -> None:
        if not self.directory_created:
            Path(self.directory).mkdir(parents=True, exist_ok=True)
        self.count += 1
        with open(self.output_path_tmplt.format(self.count), "w") as output_file:
            output_file.write(data)
