"""The Mimeo File Consumer module.

It exports only one class:
    * FileConsumer
        A Consumer implementation saving data in the filesystem.
"""
import logging
from pathlib import Path

from mimeo.config.mimeo_config import MimeoOutput
from mimeo.consumers import Consumer

logger = logging.getLogger(__name__)


class FileConsumer(Consumer):
    """A Consumer implementation saving data in the filesystem.

    This Consumer is instantiated for the 'file' output direction
    and saves data produced by Mimeo as files using Mimeo Output Details.

    Methods
    -------
    consume
        Save data generated by Mimeo into a file.

    Attributes
    ----------
    directory : str
        A directory path to save files within
    output_path_tmplt : str
        An output file path template
        (every file has its index inside the actual path)
    """

    def __init__(self, output: MimeoOutput):
        """Initialize FileConsumer class.

        Parameters
        ----------
        output : MimeoOutput
            Configured Mimeo Output Details
        """
        self.directory = output.directory_path
        self.output_path_tmplt = f"{self.directory}/{output.file_name}"
        self.__count = 0

    def consume(self, data: str) -> None:
        """Save data generated by Mimeo into a file.

        It is an implementation of Consumer's abstract method.
        If the output directory does not exist it is created.
        Every file name has an index inside its path.

        Parameters
        ----------
        data : str
            Stringified data generated by Mimeo
        """
        logger.fine("Consuming data [%s]", data)
        if not Path(self.directory).exists():
            logger.info("Creating output directory [%s]", self.directory)
            Path(self.directory).mkdir(parents=True, exist_ok=True)

        self.__count += 1
        file_name = self.output_path_tmplt.format(self.__count)

        logger.info("Writing data into file [%s]", file_name)
        with Path(file_name).open("w") as output_file:
            output_file.write(data)
