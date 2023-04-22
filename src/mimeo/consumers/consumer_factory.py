from mimeo.config.exc import UnsupportedPropertyValue
from mimeo.config.mimeo_config import MimeoConfig
from mimeo.consumers import Consumer, FileConsumer, HttpConsumer, RawConsumer


class ConsumerFactory:

    FILE_DIRECTION = MimeoConfig.OUTPUT_DETAILS_DIRECTION_FILE
    STD_OUT_DIRECTION = MimeoConfig.OUTPUT_DETAILS_DIRECTION_STD_OUT
    HTTP_DIRECTION = MimeoConfig.OUTPUT_DETAILS_DIRECTION_HTTP

    @staticmethod
    def get_consumer(mimeo_config: MimeoConfig) -> Consumer:
        direction = mimeo_config.output_details.direction
        if direction == ConsumerFactory.STD_OUT_DIRECTION:
            return RawConsumer()
        elif direction == ConsumerFactory.FILE_DIRECTION:
            return FileConsumer(mimeo_config.output_details)
        elif direction == ConsumerFactory.HTTP_DIRECTION:
            return HttpConsumer(mimeo_config.output_details)
        else:
            raise UnsupportedPropertyValue(MimeoConfig.OUTPUT_DETAILS_DIRECTION_KEY,
                                           direction,
                                           MimeoConfig.SUPPORTED_OUTPUT_DIRECTIONS)
