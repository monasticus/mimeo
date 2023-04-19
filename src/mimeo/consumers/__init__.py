"""
The consumers package contains classes corresponding
to the Mimeo Config output directions.

This package exports the following classes:
- Consumer:
    An abstract class for data consumers in Mimeo
- ConsumerFactory:
    A Factory class used to instantiate Consumer based on Mimeo Config.
- RawConsumer:
    A Consumer printing produced data in the standard output
    Corresponds to the 'stdout' output direction
- FileConsumer:
    A Consumer saving produced data in the filesystem
    Corresponds to the 'file' output direction
- HttpConsumer:
    A Consumer sending produced data in HTTP requests
    Corresponds to the 'http' output direction

To use this package, simply import the desired class:
    from mimeo.consumers import ConsumerFactory

"""

from .consumer import Consumer
from .file_consumer import FileConsumer
from .raw_consumer import RawConsumer
from .http_consumer import HttpConsumer
from .consumer_factory import ConsumerFactory
