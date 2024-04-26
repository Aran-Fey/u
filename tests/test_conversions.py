import pytest

import units
from units import Quantity, Unit


@pytest.mark.parametrize(
    "value, unit, expected_result",
    [
        # (units.meters(7_000), units.kilometers, 7),
        # (units.kilometers(3.5), units.meters, 3_500),
        # (units.celsius(10), units.kelvin, 283.15),
        # (units.kelvin(100), units.celsius, -173.15),
        # (units.kelvin(0), units.fahrenheit, -459.67),
        # (units.fahrenheit(50), units.kelvin, 283.15),
        (units.meters_per_second(1234), units.kilometers / units.seconds, 1.234),
        # (units.meters_per_second(1), units.meters / units.minutes, 60),
        # (units.kilometers_per_hour(1), units.meters_per_second, 8 + 1 / 3),
        # (units.meters_per_second(30), units.kilometers_per_hour, 108),
        # (units.square_meters(1_000_000), units.square_kilometers, 1),
    ],
)
def test_conversion(value: Quantity, unit: Unit, expected_result: float):
    result = value.to_number(unit)
    assert result == pytest.approx(expected_result)
