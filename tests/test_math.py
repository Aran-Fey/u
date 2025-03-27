import typing as t

import pytest

import u


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


def test_getitem():
    r = u.Quantity[u.DURATION]
    print(r.exponents)


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
