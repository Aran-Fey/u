import operator
import typing as t

import pytest

import u


ORDERING_OPERATORS = [operator.lt, operator.le, operator.gt, operator.ge]


@pytest.mark.parametrize(
    "result, expected_result",
    [
        (u.seconds(10) + u.seconds(5), u.seconds(15)),
        (u.seconds(10) + u.seconds(50), u.minutes(1)),
        (u.hours(0.25) + u.hours(0.5), u.minutes(45)),
    ],
)
def test_addition(result: u.Quantity, expected_result: u.Quantity):
    assert result == expected_result


@pytest.mark.parametrize(
    "result, expected_result",
    [
        (u.seconds(10) - u.seconds(3), u.seconds(7)),
        (u.seconds(70) - u.seconds(10), u.minutes(1)),
        (u.hours(0.75) - u.hours(0.5), u.minutes(15)),
    ],
)
def test_subtraction(result: u.Quantity, expected_result: u.Quantity):
    assert result == expected_result


def test_zero_arithmetic():
    assert u.seconds(3) + 0 == u.seconds(3)
    assert 0 + u.seconds(3) == u.seconds(3)
    assert u.seconds(3) - 0 == u.seconds(3)
    assert 0 - u.seconds(3) == u.seconds(-3)


@pytest.mark.parametrize(
    "op", [operator.add, operator.sub], ids=lambda op: op.__name__
)
@pytest.mark.parametrize("number", [5, 2.5])
def test_arithmetic_with_nonzero_number_raises_type_error(
    op: t.Callable[[t.Any, t.Any], t.Any], number: float
):
    with pytest.raises(TypeError):
        op(u.seconds(3), number)

    with pytest.raises(TypeError):
        op(number, u.seconds(3))


@pytest.mark.parametrize("op", [operator.add, operator.sub], ids=lambda op: op.__name__)
@pytest.mark.parametrize(
    "a, b",
    [(u.seconds(1), u.meters(1)), (u.meters(1), u.seconds(1)), (u.mps(1), u.meters(1))],
    ids=repr,
)
def test_arithmetic_with_incompatible_quantities_raises_type_error(
    op: t.Callable[[t.Any, t.Any], t.Any], a: u.Quantity, b: u.Quantity
):
    with pytest.raises(TypeError):
        op(a, b)


@pytest.mark.parametrize("op", ORDERING_OPERATORS, ids=lambda op: op.__name__)
def test_ordering_incompatible_quantities_raises_type_error(
    op: t.Callable[[t.Any, t.Any], bool],
):
    with pytest.raises(TypeError):
        op(u.seconds(1), u.meters(1))


@pytest.mark.parametrize(
    "op, expected",
    [(operator.lt, True), (operator.le, True), (operator.gt, False), (operator.ge, False)],
    ids=lambda value: getattr(value, "__name__", repr(value)),
)
def test_ordering_compatible_quantities(op: t.Callable[[t.Any, t.Any], bool], expected: bool):
    assert op(u.seconds(59), u.minutes(1)) is expected
    assert op(u.seconds(-1), 0) is expected


def test_equality_of_incompatible_quantities_is_false():
    # Like `1 == "1"`, this is not an error
    assert u.seconds(1) != u.meters(1)
    assert not (u.seconds(1) == u.meters(1))


@pytest.mark.parametrize(
    "result, expected_result",
    [
        (u.meters(10) * u.meters(5), u.square_meters(50)),
        (u.meters(10) * u.meters(5), u.square_meters(50)),
    ],
)
def test_multiplication(result: u.Quantity, expected_result: u.Quantity):
    assert result == expected_result


@pytest.mark.parametrize(
    "result, expected_result",
    [
        (u.meters(10) / u.seconds(5), u.meters_per_second(2)),
        (u.km(10) / u.seconds(5), u.meters_per_second(2000)),
    ],
)
def test_division(result: u.Quantity, expected_result: u.Quantity):
    assert result == expected_result


@pytest.mark.parametrize(
    "unit, expected_exponents",
    [
        (u.meters / u.hour, {u.DISTANCE: 1, u.DURATION: -1}),
        (u.km**2, {u.DISTANCE: 2}),
        (u.minutes * u.amperes, {u.DURATION: 1, u.ELECTRIC_CURRENT: 1}),
        (u.kg / u.second * u.m / u.second, {u.MASS: 1, u.DISTANCE: 1, u.DURATION: -2}),
    ],
)
def test_quantity_exponents_after_unit_math(
    unit: u.Unit, expected_exponents: dict[type[u.QUANTITY], int]
):
    assert dict(unit.quantity.exponents) == expected_exponents


@pytest.mark.parametrize(
    "unit, expected_quantity",
    [
        (u.meters / u.hour, u.Speed),
        (u.km**2, u.Area),
        (u.minutes * u.amperes, u.ElectricCharge),
        (u.kg / u.second * u.m / u.second, u.Force),
    ],
)
def test_quantity_equality_after_unit_math(unit: u.Unit, expected_quantity: type[u.Quantity]):
    assert unit.quantity == expected_quantity
