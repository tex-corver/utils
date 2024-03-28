from loguru import logger

from utils.test.databases import SqlDatabase


def test_database_fixture(sql_database: SqlDatabase):
    logger.info(sql_database)
