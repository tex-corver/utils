import os
from typing import Any

import pytest

from utils import security


@pytest.fixture
def jwt_secret(config: dict[str, Any]):
    yield config["security"]["context"]["secret"]


@pytest.fixture
def jwt_algorithm(config: dict[str, Any]):
    yield config["security"]["context"]["algorithm"]


@pytest.fixture
def jwt_token_factory(jwt_secret: str, jwt_algorithm: str):
    factory = security.JwtTokenFactory(
        secret=jwt_secret,
        algorithm=jwt_algorithm,
    )
    yield factory
