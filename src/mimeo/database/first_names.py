import pandas

from mimeo import tools
from mimeo.database.exc import InvalidIndex, InvalidSex


class FirstName:

    def __init__(self, name: str, sex: str):
        self.name = name
        self.sex = sex

    def __str__(self) -> str:
        return str({
            "name": self.name,
            "sex": self.sex
        })

    def __repr__(self) -> str:
        return f"FirstName('{self.name}', '{self.sex}')"


class FirstNamesDB:

    NUM_OF_RECORDS = 7455
    __SUPPORTED_SEX = ("M", "F")
    __FIRST_NAMES_DB = "forenames.csv"
    __FIRST_NAMES_DF = None
    __FIRST_NAMES = None
    __NAMES_FOR_SEX = {}

    def get_first_name_at(self, index: int) -> FirstName:
        first_names = self.__get_first_names()
        try:
            return first_names[index]
        except IndexError:
            raise InvalidIndex(f"Provided index [{index}] is out or the range: 0-{FirstNamesDB.NUM_OF_RECORDS-1}!")

    def get_first_names_by_sex(self, sex: str) -> list:
        if sex in FirstNamesDB.__SUPPORTED_SEX:
            return self.__get_first_names_by_sex(sex).copy()
        else:
            raise InvalidSex("Invalid sex (use M or F)!")

    @classmethod
    def get_first_names(cls) -> list:
        return cls.__get_first_names().copy()

    @classmethod
    def __get_first_names_by_sex(cls, sex: str) -> list:
        if sex not in cls.__NAMES_FOR_SEX:
            first_names = cls.__get_first_names()
            cls.__NAMES_FOR_SEX[sex] = list(filter(lambda first_name: first_name.sex == sex, first_names))
        return cls.__NAMES_FOR_SEX[sex]

    @classmethod
    def __get_first_names(cls) -> list:
        if cls.__FIRST_NAMES is None:
            cls.__FIRST_NAMES = [FirstName(row.NAME, row.SEX)
                                 for row in cls.__get_first_names_df().itertuples()]
        return cls.__FIRST_NAMES

    @classmethod
    def __get_first_names_df(cls) -> pandas.DataFrame:
        if cls.__FIRST_NAMES_DF is None:
            cls.__FIRST_NAMES_DF = pandas.read_csv(tools.get_resource(FirstNamesDB.__FIRST_NAMES_DB))
        return cls.__FIRST_NAMES_DF
