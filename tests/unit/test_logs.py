import logging
import os
import pytest

from utils import logs, configuration


@pytest.fixture
def persistent_log_handler():
    return logs.PersistentLogHandler(mode="w")


class TestPersistentLogHandler:
    def test_persistent_log_handler(
        self,
        persistent_log_handler: logs.PersistentLogHandler,
    ):
        logging.setLoggerClass(logging.Logger)
        logger = logging.getLogger("test-persistent-log-handler")
        handler = persistent_log_handler
        logger.addHandler(handler)
        for handler in logger.handlers:
            print(handler, flush=True)
            logger.info(handler)
            # assert isinstance(handler, logs.PersistentLogHandler)
        logger.info("test text")


# def test_temporary_log():
#     logger = logging.getLogger("test-temporary-log")
#     assert isinstance(logger, logs.Logger)
#     logger.info("test text")
# logger.info(logger.handlers)
