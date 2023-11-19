import pytest
import random
import uuid

import logging
import logging.config
import os
import yaml
import pathlib
from utils import configuration
import uuid

PROJECT_PATH = pathlib.Path(os.path.abspath(__file__)).parents[1]
os.environ["PROJECT_PATH"] = str(PROJECT_PATH)
project_path = os.environ["PROJECT_PATH"]
configuration.load_config_from_files(config_path=str(PROJECT_PATH / ".configs"))
logger = logging.getLogger(__file__)


@pytest.fixture
def random_dict() -> dict[str, any]:
    dict_a = {
        key: value
        for key in [str(uuid.uuid4()) for _ in range(10)]
        for value in [random.randint(1, 100000) for _ in range(10)]
    }
    nested_dict = {
        "1-layer": dict_a.copy(),
        "2-layers": {
            f"{str(uuid.uuid4())}": dict_a.copy(),
        },
    }
    dict_a["nested_dict"] = nested_dict
    yield dict_a


@pytest.fixture
def config_path() -> str:
    config_path = f"{project_path}/.configs"
    yield config_path


@pytest.fixture
def config() -> dict[str, any]:
    config = configuration.get_config()
    yield config
