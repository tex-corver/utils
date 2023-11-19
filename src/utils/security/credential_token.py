import jwt
import logging
import abc
import dataclasses
import os
from typing import Type

from .. import configuration

logger = logging.getLogger(__file__)


@dataclasses.dataclass
class AbstractToken(abc.ABC):
    """Abstract base class for token objects.

    Attributes:
        token (str, optional): The token string. Defaults to None.

    Args:
        data (dict[str, any]): The data dictionary associated with the token.
        token (str): The token string.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Examples:
        >>> token = AbstractToken(data={"key1": "value1", "key2": "value2"}, token="example_token")
        >>> token.token
        'example_token'
        >>> token.data
        {'key1': 'value1', 'key2': 'value2'}

    Note:
        - This class is an abstract base class that can be subclassed to create specific token objects.
        - The `data` dictionary contains additional data associated with the token.
        - The `token` attribute stores the token string.
    """

    # data: dict[str, any]
    token: str = None

    def __init__(self, data: dict[str, any], token: str, *args, **kwargs):
        # self.data = data
        self.token = token


class AbstractTokenFactory(abc.ABC):
    """Abstract base class for token factories.

    Attributes:
        secret (str): The secret used for encoding and decoding tokens.
        algorithm (str): The algorithm used for encoding and decoding tokens.

    Args:
        secret (str): The secret used for encoding and decoding tokens.
        algorithm (str): The algorithm used for encoding and decoding tokens.

    Methods:
        encode(data: str, *args, **kwargs) -> Type[AbstractToken]:
            Encodes the provided data into a token object using the implemented _encode method.

        decode(token: Type[AbstractToken] | str, *args, **kwargs) -> dict[str, any]:
            Decodes the provided token or token object using the implemented _decode method.

        _encode(data: str, *args, **kwargs) -> Type[AbstractToken]:
            Abstract method that should be implemented to encode the data into a token object.

        _decode(token: Type[AbstractToken] | str, *args, **kwargs) -> dict[str, any]:
            Abstract method that should be implemented to decode the token or token object and return the decoded data.

    Note:
        - This class is an abstract base class that can be subclassed to create specific token factory implementations.
        - The `secret` attribute is used for encoding and decoding tokens.
        - The `algorithm` attribute specifies the algorithm used for encoding and decoding tokens.
        - Subclasses must implement the `_encode` and `_decode` methods according to their specific token encoding and decoding logic.
    """

    secret: str
    algorithm: str

    def __init__(self, secret: str, algorithm: str):
        self.secret = secret
        self.algorithm = algorithm

    def encode(self, data: str, *args, **kwargs) -> Type[AbstractToken]:
        """Encodes the provided data into a token object using the implemented _encode method.

        Args:
            data (str): The data to be encoded into a token object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Type[AbstractToken]: The encoded token object.

        Raises:
            None.
        """
        token = self._encode(data, *args, **kwargs)
        return token

    def decode(self, token: Type[AbstractToken] | str, *args, **kwargs) -> dict[str, any]:
        """Decodes the provided token or token object using the implemented _decode method.

        Args:
            token (Type[AbstractToken] | str): The token or token object to be decoded.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, any]: The decoded data.

        Raises:
            None.
        """
        data = self._decode(token, *args, **kwargs)
        return data

    @abc.abstractmethod
    def _encode(self, data: str, *args, **kwargs) -> Type[AbstractToken]:
        """Abstract method that should be implemented to encode the data into a token object.

        Args:
            data (str): The data to be encoded into a token object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Type[AbstractToken]: The encoded token object.

        Raises:
            NotImplementedError: This method is meant to be implemented by subclasses.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _decode(self, token: Type[AbstractToken] | str, *args, **kwargs) -> dict[str, any]:
        """Abstract method that should be implemented to decode the token or token object and return
        the decoded data.

        Args:
            token (Type[AbstractToken] | str): The token or token object to be decoded.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, any]: The decoded data.

        Raises:
            NotImplementedError: This method is meant to be implemented by subclasses.
        """
        raise NotImplementedError


class JwtToken(AbstractToken):
    """Represents a JSON Web Token (JWT) token.

    This class is a subclass of the AbstractToken class and provides functionality specific to JWT tokens.
    JWT tokens are commonly used for authentication and authorization purposes in web applications.

    Attributes:
        token (str): The actual JWT token string.
        expiration (datetime.datetime): The expiration date and time of the token.
        claims (dict): A dictionary containing the claims (payload) of the token.
    """

    pass


class JwtTokenFactory(AbstractTokenFactory):
    """Factory class for creating and decoding JSON Web Tokens (JWTs).

    This class provides methods for encoding data into JWTs and decoding JWTs back into data.
    It inherits from the AbstractTokenFactory class and implements the _encode and _decode methods.

    Args:
        secret (str, optional): The secret key used to sign the JWTs. If not provided, it will be fetched from the environment variable "JWT_SECRET".
        algorithm (str, optional): The algorithm used to sign the JWTs. If not provided, it will be fetched from the environment variable "JWT_ALGORITHM".
        from_env (bool, optional): Determines whether to fetch the secret and algorithm from the environment variables or use the provided values. Defaults to True.

    Raises:
        ValueError: If the secret or algorithm is not provided and cannot be fetched from the environment variables.
    """

    def __init__(
        self,
        secret: str = None,
        algorithm: str = None,
        from_env: bool = False,
    ):
        logger.debug("----init JwtTokenFactory----")
        config = configuration.get_config().get("security", {}).get("context", {})
        logger.info(config)
        if secret is None:
            secret = config.get("secret")
        if algorithm is None:
            algorithm = config.get("algorithm")
        if from_env:
            secret = os.environ.get("JWT_SECRET")
            algorithm = os.environ.get("JWT_ALGORITHM")
        super().__init__(secret, algorithm)
        encode_attributes = {
            "secret": secret,
            "algorithm": algorithm,
        }
        for encode_attribute, value in encode_attributes.items():
            if value is None:
                raise ValueError(f"{encode_attribute} must be set")

    def _encode(self, data: str, *args, **kwargs) -> JwtToken:
        token = jwt.encode(data, self.secret, self.algorithm)
        return JwtToken(data=data, token=token)

    def _decode(self, token: JwtToken | str, *args, **kwargs) -> dict[str, any]:
        if isinstance(token, JwtToken):
            token = token.token
        data = jwt.decode(token, self.secret, self.algorithm)
        return data
