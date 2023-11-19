import random
import logging
from utils import security
import jwt

logger = logging.getLogger(__file__)


def prepare_jwt_data() -> dict[str, any]:
    data = {
        "a": random.randint(1, 1000),
        "b": random.randint(1, 1000),
        "c": random.randint(1, 1000),
        "d": random.randint(1, 1000),
    }
    return data


def encode_data(
    jwt_token_factory: security.JwtTokenFactory,
) -> tuple[dict[str, any], security.JwtToken]:
    data = prepare_jwt_data()
    token = jwt_token_factory.encode(data)
    return data, token


class TestJwtFactory:
    def test_encode_token_successfully(
        self,
        jwt_secret: str,
        jwt_algorithm: str,
        jwt_token_factory: security.JwtTokenFactory,
    ):
        data, token = encode_data(jwt_token_factory)
        jwt_token_from_lib = jwt.encode(data, jwt_secret, jwt_algorithm)
        assert token.token == jwt_token_from_lib

    def test_decode_token_successfully(
        self,
        jwt_secret: str,
        jwt_algorithm: str,
        jwt_token_factory: security.JwtTokenFactory,
    ):
        data, token = encode_data(jwt_token_factory)
        decoded_data = jwt_token_factory.decode(token)
        decoded_data_from_lib = jwt.decode(token.token, jwt_secret, jwt_algorithm)
        assert data == decoded_data
        assert decoded_data_from_lib == decoded_data

    def test_decode_token_string_successfully(
        self,
        jwt_secret: str,
        jwt_algorithm: str,
        jwt_token_factory: security.JwtTokenFactory,
    ):
        data, token = encode_data(jwt_token_factory)
        logger.debug(type(token))
        decoded_data = jwt_token_factory.decode(token.token)
        logger.debug(type(token))
        decoded_data_from_lib = jwt.decode(token.token, jwt_secret, jwt_algorithm)
        assert data == decoded_data
        assert decoded_data_from_lib == decoded_data
