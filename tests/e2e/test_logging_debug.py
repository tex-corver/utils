import utils
from tests.doubles.fake import make_random
import pytest
import datetime
import logging


@pytest.fixture
def logger():
    logging.setLoggerClass(utils.PrettyLogger)
    logger = logging.getLogger("Test")
    yield logger


def test_log_debug_default(logger, random_dict):
    logger.debug(random_dict)


def test_log_have_datetime(logger):
    logger.debug({"now": datetime.datetime.now()})


def test_log_sort_keys(logger, random_dict):
    logger.debug(random_dict, extra={"sort_keys": True})


# def test_log_origin_name(logger, random_dict):
#     dict_ls = random_dict
#     logger.debug(dict_ls)


def test_log_text_string(logger):
    logger.debug(make_random.make_string())


def test_log_format_string(logger):
    logger.debug("Format: %s", make_random.make_string())


# TODO:
# change file name to log
# print log should have options:
# - indent
# - sort_keys
# - is_json (bool): if True, print object as json format (no attribute with type Python object)
# By default, use pretty_dict as pretty function for log
