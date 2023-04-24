from mimeo import tools
from mimeo.database.exc import InvalidIndex


class LastNamesDB:

    NUM_OF_RECORDS = 151670
    __LAST_NAMES_DB = "surnames.txt"
    __LAST_NAMES = None

    def get_last_name_at(self, index: int) -> str:
        last_names = self.__get_last_names()
        try:
            return last_names[index]
        except IndexError:
            raise InvalidIndex(f"Provided index [{index}] is out or the range: 0-{LastNamesDB.NUM_OF_RECORDS-1}!")

    @classmethod
    def get_last_names(cls) -> list:
        return cls.__get_last_names().copy()

    @classmethod
    def __get_last_names(cls) -> list:
        if cls.__LAST_NAMES is None:
            with tools.get_resource(LastNamesDB.__LAST_NAMES_DB) as last_names:
                cls.__LAST_NAMES = [line.rstrip() for line in last_names.readlines()]
        return cls.__LAST_NAMES
