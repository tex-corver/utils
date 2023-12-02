import dataclasses
import json
import logging
import os

from . import configuration
from .values import parsers

config = configuration.get_config()

LOG_METADATA_ENV = [
    "APPLICATION",
    "SERVICE",
    "ENVIRONMENT",
]

LOG_KEY_MAPPERS = {
    "levelname": "level_name",
    "filename": "file_name",
    "levelno": "level_no",
    "lineno": "line_no",
    "thread_name": "MainThread",
    "pathname": "path_name",
}

DEFAULT_FILE_NAME = f"{os.environ.get('SERVICE', '')}.log"


def standardize_log_keys(d: dict[str, any]) -> dict[str, any]:
    d_ = {
        parsers.string_to_snake_case(LOG_KEY_MAPPERS.get(key, key)): val
        for key, val in d.items()
    }
    return d_


@dataclasses.dataclass(init=False)
class LogContext:
    application: str
    service: str
    environment: str


class InlineLogFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%", metadata=None):
        super().__init__(fmt, datefmt, style)
        self.metadata = metadata

    def format(self, record: logging.LogRecord):
        record.message = record.getMessage()
        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
        else:
            record.exc_text = ""
        if record.stack_info:
            record.stack_info = self.formatStack(record.stack_info)
        return record.__dict__


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.message = record.getMessage()
        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)
        else:
            record.exc_text = ""
        if record.stack_info:
            record.stack_info = self.formatStack(record.stack_info)
        d = standardize_log_keys(record.__dict__)
        return parsers.prettier_dict(d)


class PersistentLogHandler(logging.FileHandler):
    def __init__(
        self,
        file_name: str = DEFAULT_FILE_NAME,
        mode: str = "a",
        encoding: str = None,
        delay: str = False,
        errors: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(file_name, mode, encoding, delay, errors, *args, **kwargs)
        json_formatter = JsonFormatter()
        self.setFormatter(json_formatter)


class TemporaryLogHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Logger(logging.Logger):
    def __init__(self, name: str, file_name: str = DEFAULT_FILE_NAME):
        super().__init__(name)
        handlers = [TemporaryLogHandler(), PersistentLogHandler(file_name)]
        for handler in handlers:
            self.addHandler(handler)

    def _log(
        self,
        level,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=2,
        **kwargs,
    ):
        if extra is None:
            extra = {}
        super()._log(
            level,
            msg,
            args,
            exc_info,
            extra,
            stack_info,
            stacklevel,
            **kwargs,
        )


logging.setLoggerClass(Logger)
