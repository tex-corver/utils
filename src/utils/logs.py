from collections.abc import Mapping
import logging
from utils.values import parsers
import datetime

logger = logging.getLogger(__name__)


class PrettyLogRecord(logging.LogRecord):
    """
    Custom LogRecord class that provides a formatted message for logging.

    Inherits from `logging.LogRecord`.

    Args:
        name (str): The name of the logger.
        level (int): The logging level of the message.
        pathname (str): The full pathname of the source file.
        lineno (int): The line number where the logging call occurred.
        msg (object): The log message.
        args: The arguments to substitute into the log message.
        exc_info: Exception information.
        func (str, optional): The name of the function where the logging call occurred. Defaults to None.
        extra (Mapping[str, object], optional): Extra attributes to include in the log record. Defaults to {}.
        sinfo (str, optional): Stack information. Defaults to None.

    Attributes:
        extra (Mapping[str, object]): Extra attributes included in the log record.

    Methods:
        getMessage(): Returns the formatted log message.

    """

    def __init__(
        self,
        name: str,
        level: int,
        pathname: str,
        lineno: int,
        msg: object,
        args,
        exc_info,
        func: str | None = None,
        extra={},
        sinfo: str | None = None,
    ) -> None:
        """
        Initialize an instance of PrettyLogRecord.

        Args:
            name (str): The name of the logger.
            level (int): The logging level of the message.
            pathname (str): The full pathname of the source file.
            lineno (int): The line number where the logging call occurred.
            msg (object): The log message.
            args: The arguments to substitute into the log message.
            exc_info: Exception information.
            func (str, optional): The name of the function where the logging call occurred. Defaults to None.
            extra (Mapping[str, object], optional): Extra attributes to include in the log record. Defaults to {}.
            sinfo (str, optional): Stack information. Defaults to None.

        """
        super().__init__(
            name, level, pathname, lineno, msg, args, exc_info, func, sinfo
        )
        self.extra = extra

    def getMessage(self) -> str:
        """
        Get the formatted log message.

        Returns:
            str: The formatted log message.

        """
        _msg = str(self.msg)
        if type(self.msg) is dict and self.levelno == logger.debug:
            d = {
                key: parsers.jsonify_datetime(src_datetime=value)
                if isinstance(value, datetime.datetime)
                else value
                for key, value in dict(self.msg).items()
            }
            extra = self.extra if self.extra is not None else {}
            _msg = parsers.prettier_dict(
                d, indent=extra.get("indent", 4), sort_keys=extra.get("sort_keys", True)
            )
        else:
            if self.args:
                _msg = _msg % self.args
        return _msg


class PrettyLogger(logging.Logger):
    """
    Custom logger class that provides a formatted log message.

    Inherits from `logging.Logger`.

    Args:
        name (str): The name of the logger.
        level (int, optional): The logging level of the logger. Defaults to 0.

    Methods:
        makeRecord(): Create a log record with the provided information.
        debug(): Log a message with the DEBUG level.

    """

    def __init__(self, name: str, level=0) -> None:
        """
        Initialize an instance of PrettyLogger.

        Args:
            name (str): The name of the logger.
            level (int, optional): The logging level of the logger. Defaults to 0.

        """
        super().__init__(name, level)

    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args,
        exc_info,
        func: str | None = None,
        extra: Mapping[str, object] | None = None,
        sinfo: str | None = None,
    ) -> logging.LogRecord:
        """
        Create a log record with the provided information.

        Args:
            name (str): The name of the logger.
            level (int): The logging level of the message.
            fn (str): The full pathname of the source file.
            lno (int): The line number where the logging call occurred.
            msg (object): The log message.
            args: The arguments to substitute into the log message.
            exc_info: Exception information.
            func (str, optional): The name of the function where the logging call occurred. Defaults to None.
            extra ({
                "name": "str",
                "level": "int",
                "fn": "str",
                "lno": "int",
                "msg": "object",
                "args": "Any",
                "exc_info": "Any",
                "func": "str | None = None",
                "extra": "Mapping[str, object] | None = None",
                "sinfo": "str | None = None"
            }

        Returns:
            logging.LogRecord: The created log record.

        """
        rv = PrettyLogRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )
        if extra is not None:
            for key in extra:
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError(
                        "Attempt to overwrite %r in %s" % (key, rv.__class__.name)
                    )
                rv.__dict__[key] = extra[key]
        return rv

    def debug(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None
    ) -> None:
        """
        Log a message with the DEBUG level.

        Args:
            msg (object): The log message.
            *args (object): The arguments to substitute into the log message.
            exc_info: Exception information.
            stack_info (bool, optional): Include stack information. Defaults to False.
            stacklevel (int, optional): The level in the stack frame to log. Defaults to 1.
            extra (Mapping[str, object], optional): Extra attributes to include in the log record. Defaults to None.

        Returns:
            None

        """
        return super().debug(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra
        )
