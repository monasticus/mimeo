from abc import ABCMeta, abstractmethod


class Consumer(metaclass=ABCMeta):
    """An abstract class for data consumers in Mimeo

    Its subclasses are meant to be used in the Mimeo processing.
    Every supported output direction has a Consumer representation.

    Methods
    -------
    consume
        Consumes data generated by Mimeo
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Checks if a subclass implements the consume method

        Parameters
        ----------
        subclass : Consumer
            A Consumer subclass

        Returns
        -------
        bool
            True if the subclass includes the consume method

        Raises
        ------
        NotImplemented
            If the Consumer subclass doesn't include the consume method
        """

        return (hasattr(subclass, 'consume') and
                callable(subclass.consume) or
                NotImplemented)

    @abstractmethod
    def consume(self, data: str):
        """Consumes data generated by Mimeo

        It is an abstract method to implement in subclasses

        Parameters
        ----------
        data : str

        Raises
        ------
        NotImplementedError
            if a subclass doesn't implement this method
        """

        raise NotImplementedError
