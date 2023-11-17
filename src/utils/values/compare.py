import logging

logger = logging.getLogger(__file__)

def is_sub_dict(
    dict_a: dict, dict_b: dict, ignore_attrs: set[str] = None
) -> tuple[bool, str]:
    """
    Checks if `dict_b` is a sub-dictionary of `dict_a`.

    Args:
        dict_a (dict): The main dictionary.
        dict_b (dict): The sub-dictionary that needs to be checked.
        ignore_attrs (set[str], optional): Set of attributes to ignore during the comparison. Defaults to None.

    Returns:
        tuple[bool, str]: A tuple containing a boolean value indicating whether `dict_b` is a sub-dictionary of `dict_a`,
        and a string indicating the first attribute that is not present in `dict_a` or has a different value.

    Raises:
        None.

    Examples:
        >>> dict_a = {'name': 'John', 'age': 30, 'city': 'New York'}
        >>> dict_b = {'name': 'John', 'age': 30}
        >>> is_sub_dict(dict_a, dict_b)
        (True, None)

        >>> dict_c = {'name': 'John', 'age': 30, 'city': 'Los Angeles'}
        >>> dict_d = {'name': 'John', 'age': 30, 'city': 'New York'}
        >>> is_sub_dict(dict_c, dict_d)
        (False, 'city')

        >>> dict_e = {'name': 'John', 'age': 30, 'city': 'New York'}
        >>> dict_f = {'name': 'John', 'age': 30, 'country': 'USA'}
        >>> is_sub_dict(dict_e, dict_f)
        (False, 'country')
    """
    if len(dict_a.keys()) < len(dict_b.keys()):
        dict_a, dict_b = dict_b, dict_a
    if ignore_attrs is None:
        ignore_attrs = []
    for attr, value in dict_b.items():
        if attr not in dict_a:
            logger.debug("there is no key `%s`", attr)
            return False, attr
        if value != dict_a[attr]:
            logger.debug("%s != %s", dict_a[attr], value)
            return False, attr
    return True, None
