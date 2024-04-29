import pytest

import u
from u import Quantity, Unit


@pytest.mark.parametrize(
    "value, unit, expected_result",
    [
        (u.meters(7_000), u.kilometers, 7),
        (u.kilometers(3.5), u.meters, 3_500),
        # (u.celsius(10), u.kelvin, 283.15),
        # (u.kelvin(100), u.celsius, -173.15),
        # (u.kelvin(0), u.fahrenheit, -459.67),
        # (u.fahrenheit(50), u.kelvin, 283.15),
        (u.meters_per_second(1234), u.kilometers / u.seconds, 1.234),
        (u.meters_per_second(1), u.meters / u.minutes, 60),
        (u.kilometers_per_hour(90), u.meters_per_second, 25),
        (u.meters_per_second(30), u.kilometers_per_hour, 108),
        (u.square_meters(1_000_000), u.square_kilometers, 1),
    ],
)
def test_to_number(value: Quantity, unit: Unit, expected_result: float):
    result = value.to_number(unit)
    assert result == pytest.approx(expected_result)


@pytest.mark.parametrize(
    "value, expected_result",
    [
        (u.meters(7), "7m"),
        (u.kilometers(3.5), "3.5km"),
        (u.meters_per_second(5), "5m/s"),
        (u.square_meters(3), "3m²"),
    ],
)
def test_to_string(value: Quantity, expected_result: str):
    assert str(value) == expected_result
