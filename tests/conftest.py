import os
import pathlib
import random
import uuid
from typing import Any

import pytest
from utils import configuration

PROJECT_PATH = pathlib.Path(os.path.abspath(__file__)).parents[1]
os.environ["PROJECT_PATH"] = str(PROJECT_PATH)
project_path = os.environ["PROJECT_PATH"]


@pytest.fixture
def random_dict():
    dict_a: dict[str, Any] = {
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
def config_path():
    config_path = f"{project_path}/.configs"
    yield config_path


@pytest.fixture
def config():
    config = configuration.get_config()
    yield config
