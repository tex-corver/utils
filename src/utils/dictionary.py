from typing import Any


def filter_dict(
    orginal_dict: dict[Any, Any],
    ignore_keys: set[Any] | None = None,
):
    """filter_dict.

    Args:
        orginal_dict (dict[Any, Any]): orginal_dict
        ignore_keys (set[Any] | None): ignore_keys
    """
    ignore_keys = ignore_keys or set()
    return {key: value for key, value in orginal_dict.items() if key not in ignore_keys}


def is_subdict(
    dict_a: dict[Any, Any],
    dict_b: dict[Any, Any],
    ignore_keys: set[Any] | None = None,
):
    """is_subdict.

    Args:
        dict_a (dict[Any, Any]): dict_a
        dict_b (dict[Any, Any]): dict_b
        ignore_keys (set[Any] | None): ignore_keys
    """
    ignore_keys = ignore_keys or set()
    dict_a = filter_dict(dict_a, ignore_keys)
    dict_b = filter_dict(dict_b, ignore_keys)

    # Note: The `<=` operator checks if all items in `dict_a` are present in `dict_b`.
    return dict_a.items() <= dict_b.items()


def is_equal(
    dict_a: dict[Any, Any],
    dict_b: dict[Any, Any],
    ignore_keys: set[Any] | None = None,
):
    """is_equal.

    Args:
        dict_a (dict[Any, Any]): dict_a
        dict_b (dict[Any, Any]): dict_b
        ignore_keys (set[Any] | None): ignore_keys
    """
    dict_a = filter_dict(dict_a, ignore_keys)
    dict_b = filter_dict(dict_b, ignore_keys)

    return dict_a == dict_b


def merge_dicts(
    dict_a: dict[Any, Any],
    dict_b: dict[Any, Any],
    ignore_keys: set[Any] | None = None,
):
    """merge_dicts.

    Args:
        dict_a (dict[Any, Any]): dict_a
        dict_b (dict[Any, Any]): dict_b
        ignore_keys (set[Any] | None): ignore_keys
    """
    dict_a = filter_dict(dict_a, ignore_keys)
    dict_b = filter_dict(dict_b, ignore_keys)

    return {**dict_a, **dict_b}
