import uuid

from mimeo.context.exc import (InvalidSpecialFieldName,
                               InvalidSpecialFieldValue, SpecialFieldNotFound)


class MimeoIteration:

    def __init__(self, identifier: int):
        self.id = identifier
        self.key = str(uuid.uuid4())
        self.__special_fields = {}

    def add_special_field(self, field_name: str, field_value) -> None:
        if not isinstance(field_name, str):
            raise InvalidSpecialFieldName("A special field name needs to be a string value!")
        if isinstance(field_value, dict) or isinstance(field_value, list):
            raise InvalidSpecialFieldValue(f"Provided field value [{field_value}] is invalid (use any atomic value)!")

        self.__special_fields[field_name] = field_value

    def get_special_field(self, field_name: str):
        if field_name not in self.__special_fields:
            raise SpecialFieldNotFound(f"Special Field [{field_name}] has not been found!")

        return self.__special_fields.get(field_name)
