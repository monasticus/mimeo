import uuid

from mimeo.context.exc import MinimumIdentifierReached


class MimeoIteration:

    def __init__(self, identifier: int):
        self.id = identifier
        self.key = str(uuid.uuid4())


class MimeoContext:

    def __init__(self):
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
        return self.__iterations[-1]
