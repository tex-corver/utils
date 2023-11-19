import pytest
from utils import configuration
import os
import logging

logger = logging.getLogger(__file__)

config_path: str = f'{os.environ.get("PROJECT_PATH")}/.configs'


def assert_config(config: dict[str, any]) -> bool:
    assert "database" in config


def test_get_config():
    config = configuration.load_config_from_files(config_path=config_path)
    assert_config(config)


def test_get_config_when_load_config_used_from_another_file():
    config = configuration.get_config()
    assert_config(config)


def test_override_config():
    config_path = f'{os.environ.get("PROJECT_PATH")}/tests/data/configs'
    new_config = configuration.load_config_from_files(config_path)
    assert "not_database" in new_config
    assert "database" not in new_config


def test_load_config_to_env():
    config = configuration.inject_config_to_env(
        config_path=config_path,
    )
    logger.debug(config)
    assert config is not None
    for key in config:
        assert os.environ.get(key.upper()) is not None
