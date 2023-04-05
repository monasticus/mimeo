from mimeo.context import MimeoIteration
from mimeo.context.exc import (ContextIterationNotFound,
                               MinimumIdentifierReached,
                               UninitializedContextIteration)


class MimeoContext:

    def __init__(self, name: str):
        self.name = name
        self.__id = 0
        self.__iterations = []

    def next_id(self) -> int:
        self.__id += 1
        return self.__id

    def curr_id(self) -> int:
        return self.__id

    def prev_id(self) -> int:
        if self.__id > 0:
            self.__id -= 1
            return self.__id
        else:
            raise MinimumIdentifierReached("There's no previous ID!")

    def next_iteration(self) -> MimeoIteration:
        next_iteration_id = 1 if len(self.__iterations) == 0 else self.__iterations[-1].id + 1
        next_iteration = MimeoIteration(next_iteration_id)
        self.__iterations.append(next_iteration)
        return next_iteration

    def curr_iteration(self) -> MimeoIteration:
        if len(self.__iterations) > 0:
            return self.__iterations[-1]
        else:
            raise UninitializedContextIteration(f"No iteration has been initialized for the current context [{self.name}]")

    def get_iteration(self, iteration_id: int) -> MimeoIteration:
        iteration = next(filter(lambda i: i.id == iteration_id, self.__iterations), None)
        if iteration is not None:
            return iteration
        else:
            raise ContextIterationNotFound(f"No iteration with id [{iteration_id}] "
                                           f"has been initialized for the current context [{self.name}]")
