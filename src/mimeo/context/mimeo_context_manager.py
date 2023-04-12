from mimeo.config import MimeoConfig
from mimeo.context import MimeoContext
from mimeo.context.exc import VarNotFound
from mimeo.meta import Alive, OnlyOneAlive


class MimeoContextManager(Alive, metaclass=OnlyOneAlive):

    __INSTANCES = []

    def __init__(self, mimeo_config: MimeoConfig = None):
        super().__init__()
        self.__mimeo_config = mimeo_config
        self.__vars = {}
        self.__contexts = {}
        self.__current_context = None

    def __enter__(self):
        super().__enter__()
        self.__vars = self.__mimeo_config.vars
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.__vars = None
        self.__contexts = None
        return None

    def get_context(self, context: str) -> MimeoContext:
        super().assert_alive()
        if context not in self.__contexts:
            self.__contexts[context] = MimeoContext(context)
        return self.__contexts[context]

    def get_current_context(self) -> MimeoContext:
        super().assert_alive()
        return self.__current_context

    def set_current_context(self, context: MimeoContext) -> None:
        super().assert_alive()
        self.__current_context = context

    def get_var(self, variable_name: str):
        value = self.__vars.get(variable_name)
        if value is not None:
            return value
        else:
            raise VarNotFound(f"Provided variable [{variable_name}] is not defined!")
