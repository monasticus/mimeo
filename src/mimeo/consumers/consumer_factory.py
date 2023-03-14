from mimeo.config.mimeo_config import MimeoConfig
from mimeo.consumers import Consumer, FileConsumer, RawConsumer
from mimeo.exceptions import UnsupportedOutputDirection


class ConsumerFactory:

    FILE_DIRECTION = "file"
    STD_OUT_DIRECTION = "stdout"

    @staticmethod
    def get_consumer(mimeo_config: MimeoConfig) -> Consumer:
        direction = mimeo_config.output_details.direction
        if direction == ConsumerFactory.STD_OUT_DIRECTION:
            return RawConsumer()
        elif direction == ConsumerFactory.FILE_DIRECTION:
            return FileConsumer(mimeo_config.output_details)
        else:
            raise UnsupportedOutputDirection(f"Provided direction [{direction}] is not supported!")
