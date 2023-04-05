from mimeo.context.exc import MinimumIdentifierReached


class MimeoContext:

    def __init__(self):
        self.__id = 0

    def next_id(self):
        self.__id += 1
        return self.__id

    def curr_id(self):
        return self.__id

    def prev_id(self):
        if self.__id > 0:
            self.__id -= 1
            return self.__id
        else:
            raise MinimumIdentifierReached("There's no previous ID!")
