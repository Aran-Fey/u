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
    ],
)
def test_division(result: u.Quantity, expected_result: u.Quantity):
    assert result == expected_result
