from logging import Filter, LogRecord, INFO, DEBUG


class InfoFilter(Filter):

    def filter(self, record: LogRecord):
        return record.levelno >= INFO


class DebugFilter(Filter):

    def filter(self, record: LogRecord):
        return record.levelno <= DEBUG
