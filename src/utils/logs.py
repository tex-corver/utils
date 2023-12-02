import dataclasses
import json
import logging
import os

from . import configuration
from .values import parsers

config = configuration.get_config()

LOG_METADATA_KEYS = [
    "application",
    "service",
    "environment",
]

LOG_KEY_MAPPERS = {
    "levelname": "level_name",
    "filename": "file_name",
    "levelno": "level_no",
    "lineno": "line_no",
    "thread_name": "MainThread",
    "pathname": "path_name",
}

LOG_CONTEXT_KEYS = {
    "file_name",
    "func_name",
    "line_no",
    "module",
    "level_no",
}


class DynamicObjectMixin:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        attributes = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attributes})"


@dataclasses.dataclass(init=False)
class LogContext(DynamicObjectMixin):
    file_name: str
    func_name: str
    line_no: int
    module: str
    level_no: int

    def __init__(self, **kwargs):
        """Init LogContext from LogRecord.
        Accepted kwargs:
        - file_name
        - func_name
        - line_no
        - module
        - level_no
        """
        for key, val in kwargs.items():
            standard_key = parsers.string_to_snake_case(LOG_KEY_MAPPERS.get(key, key))
            if standard_key not in LOG_CONTEXT_KEYS:
                # print("not in keys", key)
                continue
            setattr(
                self,
                standard_key,
                val,
            )

    @property
    def json(self):
        return self.__dict__

    def __repr__(self):
        return super().__repr__()


@dataclasses.dataclass(init=False)
class LogMetadata(DynamicObjectMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key in LOG_METADATA_KEYS:
            setattr(self, key.lower(), os.environ.get(key.upper()))

    @property
    def json(self):
        return self.__dict__

    def __repr__(self):
        return super().__repr__()


DEFAULT_FILE_NAME = f"{os.environ.get('SERVICE', '')}.log"


def standardize_log_record(d: dict[str, any]) -> dict[str, any]:
    d_ = {
        parsers.string_to_snake_case(LOG_KEY_MAPPERS.get(key, key)): val
        for key, val in d.items()
    }

    return d_


@dataclasses.dataclass(init=False)
class LogRecord(logging.LogRecord):
    context: LogContext
    metadata: LogMetadata

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata = LogMetadata()
        self.context = LogContext(
            **self.__dict__,
        )

    @property
    def json(self):
        return {
            "context": self.context.json,
            "metadata": self.metadata.json,
            "args": self.args,
            "message": self.getMessage(),
            "exc_info": self.exc_info,
            "stack_info": self.stack_info,
        }

    def __str__(self):
        return parsers.prettier_dict(self.json)

    def __repr__(self):
        return f"{self.__class__.__name__}({parsers.prettier_dict(self.json)})"


logging.setLogRecordFactory(LogRecord)


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
        s = super().format(record)
        # record.message = record.getMessage()
        # if record.exc_info:
        #     record.exc_text = self.formatException(record.exc_info)
        # else:
        #     record.exc_text = ""
        # if record.stack_info:
        #     record.stack_info = self.formatStack(record.stack_info)
        d = standardize_log_record(record.json)
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
