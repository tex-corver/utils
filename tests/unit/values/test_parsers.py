from utils import parsers
import logging
from datetime import datetime
import enum

logger = logging.getLogger(__file__)


class TestParser:
    def test_prettier_dict(
        self,
        random_dict: dict[str, any],
    ):
        logger.info(parsers.prettier_dict(random_dict))


class TestEnum(enum.Enum):
    VALUE1 = "value1"
    VALUE2 = "value2"


def test_jsonify_dict():
    # Arrange
    test_dict = {
        "key1": "value1",
        "_key2": "value2",
        "key3": datetime(2022, 1, 1),
        "key4": TestEnum.VALUE1,
        "hidden_key": "hidden_value",
    }
    expected_dict = {"key1": "value1", "key3": "2022-01-01T00:00:00", "key4": "value1"}
    hidden_attrs = {"hidden_key"}

    # Act
    result_dict = parsers.jsonify_dict(test_dict, hidden_attrs)

    # Assert
    assert result_dict == expected_dict


def test_string_converter():
    s = "MainThread"
    result = parsers.string_to_snake_case(s)
    logger.info(result)
