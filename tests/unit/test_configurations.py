import os
from typing import Any

import pytest
from icecream import ic

from utils import configuration

config_path: str = f'{os.environ.get("PROJECT_PATH")}/.configs'


@pytest.fixture
def teardown():
    yield


def assert_config(config: dict[str, Any]):
    assert "database" in config


def test_get_config_before_load_config():
    config = configuration.get_config()
    assert_config(config)


def test_get_config():
    config = configuration.load_config(config_path=config_path)
    assert_config(config)


def test_get_config_when_load_config_used_from_another_file():
    config = configuration.get_config()
    assert_config(config)


def test_override_config():
    config_path = f'{os.environ.get("PROJECT_PATH")}/tests/data/configs'
    new_config = configuration.load_config(config_path)
    ic(new_config)
    assert "not_database" in new_config
    assert "database" not in new_config
