import logging
import pytest
import os
from .. import databases
from ... import configuration

logger = logging.getLogger(__file__)

@pytest.fixture
def load_config(config_path: str) -> dict[str, any]:
    """
    Pytest fixture that loads the configuration object into the environment.

    This fixture loads the configuration object into the environment by calling `configuration.inject_config_to_env()` and yields the configuration object.

    Returns:
        dict[str, any]: The configuration object.

    Usage:
        This fixture can be used in pytest tests by including it as an argument in the test function.

        Example:
        def test_something(load_config):
    """
    logger.debug(config_path)
    config = configuration.load_config_from_files(config_path=config_path)
    logger.debug(config)

@pytest.fixture
def config() -> dict[str, any]:
    """
    Pytest fixture that provides the configuration object.

    This fixture retrieves the configuration object from the environment variable "CONFIG" and yields it.

    Returns:
        dict[str, any]: The configuration object.

    Usage:
        This fixture can be used in pytest tests by including it as an argument in the test function.

        Example:
        def test_something(config):
            # Use the configuration object within the test
            ...

    """
    config = configuration.get_config()
    logger.debug("config: %s", config)
    yield config

@pytest.fixture
def sql_database_uri(load_config: None) -> str:
    """
    Pytest fixture that provides the SQL database URI.

    This fixture retrieves the SQL database URI from the environment variable "DATABASE_URI" and yields it.

    Returns:
        str: The SQL database URI.

    Usage:
        This fixture can be used in pytest tests by including it as an argument in the test function.

        Example:
        def test_something(sql_database_uri):
            # Use the SQL database URI within the test
            ...

    """
    config = configuration.get_config()
    uri = config.get("database", {}).get("connection").get("uri")
    if uri is None:
        uri = os.environ.get("DATABASE_URI")
    logger.debug("sql_database_uri: %s", uri)
    yield uri


@pytest.fixture
def sql_database(sql_database_uri: str, load_config: None) -> databases.SqlDatabase:
    """
    Pytest fixture that provides a SQL database object.

    This fixture takes the SQL database URI as an argument and creates a `SqlDatabase` object using the provided URI. It yields the `SqlDatabase` object, allowing it to be used in pytest tests.

    Args:
        sql_database_uri (str): The SQL database URI.

    Returns:
        SqlDatabase: The SQL database object.

    Usage:
        This fixture can be used in pytest tests by including it as an argument in the test function.

        Example:
        def test_something(sql_database):
            # Use the SQL database object within the test
            ...

    """
    database = databases.SqlDatabase(uri=sql_database_uri)
    yield database
