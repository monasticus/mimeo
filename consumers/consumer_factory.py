from consumers import Consumer, FileConsumer
from model.exceptions import UnsupportedOutputDirection
from model.mimeo_config import MimeoConfig


class ConsumerFactory:

    FILE = "file"

    @staticmethod
    def get_consumer(mimeo_config: MimeoConfig) -> Consumer:
        direction = mimeo_config.output_details.direction
        if direction == ConsumerFactory.FILE:
            return FileConsumer(mimeo_config.output_details)
        else:
            raise UnsupportedOutputDirection(f"Provided direction ({direction}) is not supported!")
