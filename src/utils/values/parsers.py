import json
from datetime import datetime
import enum


def prettier_dict(d: dict[any, any], indent: int = 4, sort_keys: bool = True) -> str:
    """Returns a pretty-printed string representation of a nested dictionary.

    Args:
        d (dict[any, any]): The dictionary to be pretty-printed.

    Returns:
        str: A string representation of the dictionary with nested elements indented and keys sorted.

    Examples:
        >>> my_dictionary = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
        >>> prettier_dict(my_dictionary)
        '{\n    "a": 1,\n    "b": {\n        "c": 2,\n        "d": {\n            "e": 3\n        }\n    }\n}'

    Note:
        This function uses the `json.dumps` method with the `indent=4` and `sort_keys=True` arguments to achieve the pretty-printing.

    Raises:
        None.
    """
    return json.dumps(d, indent=indent, sort_keys=sort_keys)


def jsonify_datetime(src_datetime: datetime, datetime_format: str = "%Y-%m-%d %H:%M:%S.%f") -> str:
    """Converts a datetime object to a string representation in JSON format.

    Args:
        src_datetime (datetime): The datetime object to be converted.
        datetime_format (str, optional): The format string to use for the datetime conversion. Defaults to "%Y-%m-%d %H:%M:%S.%f".

    Returns:
        str: A string representation of the datetime object in JSON format.

    Examples:
        >>> import datetime
        >>> my_datetime = datetime.datetime(2023, 8, 10, 10, 30, 0)
        >>> jsonify_datetime(my_datetime)
        '2023-08-10 10:30:00.000000'

        >>> jsonify_datetime(my_datetime, "%Y-%m-%dT%H:%M:%S")
        '2023-08-10T10:30:00'

    Note:
        If the `datetime_format` argument is not provided, the function will default to "%Y-%m-%d %H:%M:%S.%f".
        The function uses the `strftime` method of the datetime object to format the datetime as a string.

    Raises:
        None.
    """
    if datetime_format is None:
        datetime_format = "%Y-%m-%dT%H:%M:%S"
    return src_datetime.strftime(datetime_format)


def jsonify_enum(src_enum: enum.Enum) -> str:
    """Converts an enumeration value to its string representation.

    Args:
        src_enum (enum.Enum): The enumeration value to be converted.

    Returns:
        str: A string representation of the enumeration value.

    Examples:
        >>> from enum import Enum
        >>> class MyEnum(Enum):
        ...     VALUE1 = "First Value"
        ...     VALUE2 = "Second Value"
        ...
        >>> my_enum_value = MyEnum.VALUE1
        >>> jsonify_enum(my_enum_value)
        'First Value'

    Note:
        This function assumes that the enumeration values have a `value` attribute that represents their string representation.
        It simply returns the `value` attribute of the enumeration value.

    Raises:
        None.
    """
    return src_enum.value


def jsonify_dict(
    src_dict: dict[str, any],
    hidden_attrs: set[str] = None,
    datetime_format: str = None,
) -> dict[str, any]:
    """Converts a dictionary to a JSON-like dictionary representation, with support for datetime and
    enumeration values.

    Args:
        src_dict (dict[str, any]): The dictionary to be converted.
        hidden_attrs (set[str], optional): A set of attribute names to be excluded from the resulting dictionary. Defaults to None.
        datetime_format (str, optional): The format string to use for datetime conversion. Defaults to None.

    Returns:
        dict[str, any]: A dictionary representing the converted input dictionary, with datetime and enumeration values converted to their string representations.

    Examples:
        >>> from datetime import datetime
        >>> from enum import Enum
        >>> class MyEnum(Enum):
        ...     VALUE1 = "First Value"
        ...     VALUE2 = "Second Value"
        ...
        >>> my_dict = {"key1": 123, "key2": datetime(2023, 8, 10, 10, 30, 0), "key3": MyEnum.VALUE1}
        >>> jsonify_dict(my_dict)
        {'key1': 123, 'key2': '2023-08-10 10:30:00.000000', 'key3': 'First Value'}

    Note:
        - The resulting dictionary will exclude attributes specified in the `hidden_attrs` set and attributes starting with an underscore.
        - If a value in the input dictionary is of type `datetime`, it will be converted using the `jsonify_datetime` function.
        - If a value in the input dictionary is of type `enum.Enum`, it will be converted using the `jsonify_enum` function.

    Raises:
        None.
    """
    if hidden_attrs is None:
        hidden_attrs = []
    data = {
        key: val
        for key, val in src_dict.items()
        if key not in hidden_attrs and not key.startswith("_")
    }
    for attr, value in data.items():
        if isinstance(value, datetime):
            data[attr] = jsonify_datetime(value, datetime_format)
        if isinstance(value, enum.Enum):
            data[attr] = jsonify_enum(value)
    return data
