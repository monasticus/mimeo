from mimeo.config.mimeo_config import MimeoConfig
from mimeo.consumers import Consumer, FileConsumer, HttpConsumer, RawConsumer
from mimeo.exceptions import UnsupportedOutputDirection


class ConsumerFactory:
    """A Factory class used to instantiate Consumer based on Mimeo Config

    Implementation of the Consumer class depends on the output direction configured.

    Attributes
    ----------
    FILE_DIRECTION
        The 'file' output direction
    STD_OUT_DIRECTION
        The 'stdout' output direction
    HTTP_DIRECTION
        The 'http' output direction

    Methods
    -------
    get_consumer(mimeo_config: MimeoConfig) -> Consumer
        Returns a Consumer's implementation instance
        based on Mimeo Config output direction
    """

    FILE_DIRECTION = "file"
    STD_OUT_DIRECTION = "stdout"
    HTTP_DIRECTION = "http"

    @staticmethod
    def get_consumer(mimeo_config: MimeoConfig) -> Consumer:
        """Returns a Consumer's implementation instance
        based on Mimeo Config output direction

        Parameters
        ----------
        mimeo_config : MimeoConfig
            A Mimeo Configuration

        Returns
        -------
        Consumer
            A Consumer's implementation instance

        Raises
        ------
        UnsupportedOutputDirection
            If the output direction is not supported
        """

        direction = mimeo_config.output_details.direction
        if direction == ConsumerFactory.STD_OUT_DIRECTION:
            return RawConsumer()
        elif direction == ConsumerFactory.FILE_DIRECTION:
            return FileConsumer(mimeo_config.output_details)
        elif direction == ConsumerFactory.HTTP_DIRECTION:
            return HttpConsumer(mimeo_config.output_details)
        else:
            raise UnsupportedOutputDirection(f"Provided direction [{direction}] is not supported!")
