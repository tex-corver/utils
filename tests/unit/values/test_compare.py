import random
import uuid
from typing import Any

from utils import values


def prepare_dicts(random_dict: dict[str, Any]):
    dict_a = random_dict
    return dict_a, dict_a.copy()


class TestCompare:
    def test_is_sub_dict(self, random_dict: dict[str, Any]):
        # Arrange
        dict_a, dict_b = prepare_dicts(random_dict)
        # Act
        result, key = values.is_sub_dict(dict_a, dict_b)
        # Assert
        assert result
        assert key is None

    def test_not_sub_dict(self, random_dict: dict[str, Any]):
        # Arrange
        dict_a, dict_b = prepare_dicts(random_dict)
        diff_key = str(uuid.uuid4())
        dict_a[diff_key] = random.randint(1, 100000)
        dict_b[diff_key] = dict_a[diff_key] + 1
        # Act
        result, key = values.is_sub_dict(dict_a, dict_b)
        # Assert
        assert not result
        assert key == diff_key
