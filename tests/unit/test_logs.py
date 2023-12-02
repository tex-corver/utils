import logging
import json
import os
import random
import pytest

from utils import logs, configuration


@pytest.fixture(scope="function")
def persistent_log_handler():
    yield logs.PersistentLogHandler(mode="w")


@pytest.fixture
def log_record():
    return logs.LogRecord(
        "test",
        logging.INFO,
        "/path/to/module",
        42,
        "Test message",
        args=(),
        exc_info=None,
    )


def test_log_context_init(log_record: logs.LogRecord):
    context = logs.LogContext(**log_record.__dict__)
    required_keys = logs.LOG_CONTEXT_KEYS
    for key in required_keys:
        assert hasattr(context, key)


def test_log_metadata_init():
    metadata = logs.LogMetadata()
    print(metadata)


@pytest.fixture(autouse=True, scope="function")
def teardown(persistent_log_handler: logs.PersistentLogHandler):
    yield
    logging.setLoggerClass(logging.Logger)
    with open(persistent_log_handler.baseFilename, "w") as f:
        pass


class TestLogRecord:
    def test_log_record_init(self, log_record: logs.LogRecord):
        test_log_context_init(log_record)
        test_log_metadata_init()


class TestPersistentLogHandler:
    def _test_log_contains_keys(self, content: dict[str, any]):
        keys = {"context", "metadata", "message", "args", "exc_info", "stack_info"}
        for key in keys:
            assert key in content, f"{key} not in log"

    def test_log_text_only(
        self,
        persistent_log_handler: logs.PersistentLogHandler,
        # teardown,
    ):
        logging.setLoggerClass(logging.Logger)
        logger = logging.getLogger("test_log_text_only")
        handler = persistent_log_handler
        logger.addHandler(handler)
        logger.info("only text")
        with open(handler.baseFilename, "r") as f:
            text = f.read()
            content = json.loads(text)
            self._test_log_contains_keys(content)

    def test_log_with_arguments(
        self,
        persistent_log_handler: logs.PersistentLogHandler,
        teardown,
    ):
        logging.setLoggerClass(logging.Logger)
        logger = logging.getLogger("test_log_with_arguments")
        handler = persistent_log_handler
        logger.addHandler(handler)
        x = 5
        logger.info("test %s", x)
        with open(handler.baseFilename, "r") as f:
            text = f.read()
            content = json.loads(text)
            self._test_log_contains_keys(content)  #


class TestLogger:
    def test_init(
        self,
        # teardown,
    ):
        logger = logs.Logger("test_logger_init")
        found = {
            logs.PersistentLogHandler: False,
            logs.TemporaryLogHandler: False,
        }
        for handler in logger.handlers:
            found[type(handler)] = True
        for key, val in found.items():
            assert val, f"logger is missing {key} handler"

    def test_log_text_only(
        self,
        # teardown,
    ):
        logging.setLoggerClass(logs.Logger)
        logger = logging.getLogger("test_logger_log")
        logger.info("test text")

    def test_log_with_arguments(self):
        logging.setLoggerClass(logs.Logger)
        logger = logging.getLogger("test_logger_log")
        x = random.randint(0, 100)
        logger.info("test %s", x)


# def test_temporary_log():
#     logger = logging.getLogger("test-temporary-log")
#     assert isinstance(logger, logs.Logger)
#     logger.info("test text")
# logger.info(logger.handlers)
