from utils.test import UnitTestState


def test_add_state():
    x = UnitTestState(
        data={"a": 1},
        responses={"b": 2},
        messages={"c": 2, "z": 5},
    )
    y = UnitTestState(
        data={"a": 3},
        responses={"c": 8},
        messages={"c": 3},
    )

    expected = UnitTestState(
        data={"a": 3},
        responses={"b": 2, "c": 8},
        messages={"c": 3, "z": 5},
    )
    assert expected == x + y


def test_add_state_with_none():
    x = UnitTestState(
        data={"a": 1},
        messages={"c": 2, "z": 5},
    )
    y = UnitTestState(
        data={"a": 3},
        responses={"c": 8},
        messages={"c": 3},
    )

    expected = UnitTestState(
        data={"a": 3},
        responses={"c": 8},
        messages={"c": 3, "z": 5},
    )
    assert expected == x + y


def test_iadd_state():
    x = UnitTestState(
        data={"a": 1},
        responses={"b": 2},
        messages={"c": 2, "z": 5},
    )
    y = UnitTestState(
        data={"a": 3},
        responses={"c": 8},
        messages={"c": 3},
    )
    expected = UnitTestState(
        data={"a": 3},
        responses={"b": 2, "c": 8},
        messages={"c": 3, "z": 5},
    )
    x += y
    assert expected == x


def test_iadd_state_with_none():
    x = UnitTestState(
        data={"a": 1},
        messages={"c": 2, "z": 5},
    )
    y = UnitTestState(
        data={"a": 3},
        responses={"c": 8},
        messages={"c": 3},
    )

    expected = UnitTestState(
        data={"a": 3},
        responses={"c": 8},
        messages={"c": 3, "z": 5},
    )
    x += y
    assert expected == x
