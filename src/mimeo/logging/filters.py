from logging import DEBUG, INFO, Filter, LogRecord


class InfoFilter(Filter):

    def filter(self, record: LogRecord):
        return record.levelno >= INFO


class DebugFilter(Filter):

    def filter(self, record: LogRecord):
        return record.levelno <= DEBUG
