import random
import string
from abc import ABCMeta, abstractmethod


class MimeoUtil(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'KEY') and
                hasattr(subclass, 'render') and
                callable(subclass.render) and
                NotImplemented)

    @abstractmethod
    def render(self):
        raise NotImplementedError


class RandomStringUtil(MimeoUtil):

    KEY = "random_str"

    def __init__(self, **kwargs):
        self.__length = kwargs.get("length", 20)

    def render(self):
        return "".join(random.choice(string.ascii_letters) for _ in range(self.__length))


class RandomIntegerUtil(MimeoUtil):

    KEY = "random_int"

    def __init__(self, **kwargs):
        self.__limit = kwargs.get("limit", 100)

    def render(self):
        return random.randrange(self.__limit)


class RandomItemUtil(MimeoUtil):

    KEY = "random_item"

    def __init__(self, **kwargs):
        self.__items = kwargs.get("items", [])

    def render(self):
        length = len(self.__items)
        return "" if length == 0 else self.__items[random.randrange(0, length)]
