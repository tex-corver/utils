import pytest
import os
from utils import security


@pytest.fixture
def jwt_secret(config: dict[str, any]) -> str:
    yield config["security"]["context"]["secret"]


@pytest.fixture
def jwt_algorithm(config: dict[str, any]) -> str:
    yield config["security"]["context"]["algorithm"]


@pytest.fixture
def jwt_token_factory(jwt_secret: str, jwt_algorithm: str):
    factory = security.JwtTokenFactory(
        secret=jwt_secret,
        algorithm=jwt_algorithm,
    )
    yield factory
