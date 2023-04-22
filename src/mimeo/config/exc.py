class UnsupportedPropertyValue(Exception):

    def __init__(self, prop: str, val: str, supported_values: tuple):
        super().__init__(f"Provided {prop} [{val}] is not supported! "
                         f"Supported values: [{', '.join(supported_values)}].")


class MissingRequiredProperty(Exception):
    pass


class InvalidIndent(Exception):
    pass


class InvalidVars(Exception):
    pass


class IncorrectMimeoModel(Exception):
    pass


class IncorrectMimeoTemplate(Exception):
    pass


class IncorrectMimeoConfig(Exception):
    pass
