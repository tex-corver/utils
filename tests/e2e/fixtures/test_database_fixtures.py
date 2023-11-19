import logging

logger = logging.getLogger(__file__)


def test_database_fixture(sql_database):
    logger.info(sql_database)
