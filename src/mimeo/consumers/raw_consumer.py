from mimeo.consumers import Consumer


class RawConsumer(Consumer):
    """A Consumer implementation for printing produced data in the standard output

    This Consumer is instantiated for the 'stdout' output direction
    and prints data produced by Mimeo in the standard output.

    Methods
    -------
    consume
        Consumes data generated by printing it in the standard output
    """

    def consume(self, data: str) -> None:
        """Consumes data generated by printing it in the standard output

        It is an implementation of Consumer's abstract method.

        Parameters
        ----------
        data : str
            Stringified data generated by Mimeo
        """

        print(data)
