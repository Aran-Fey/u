import typing as t

import pytest

import u


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
def test_to_number(value: u.Quantity, unit: u.Unit, expected_result: float):
    result = value.to_number(unit)
    assert result == pytest.approx(expected_result)


@pytest.mark.parametrize(
    "value, expected_result",
    [
        (u.meters(7), "7m"),
        (u.kilometers(3.5), "3.5km"),
        (u.meters_per_second(5), "5m/s"),
        (u.square_meters(3), "3m²"),
        (((u.meters / u.second) / u.second)(2), "2m/s²"),
        ((u.meters / u.second**2)(4), "4m/s²"),
    ],
)
def test_to_string(value: u.Quantity, expected_result: str):
    assert str(value) == expected_result


@pytest.mark.parametrize(
    "text, quantity, expected_result",
    [
        ("7m", u.Distance, u.m(7)),
        ("6 km", u.Distance, u.km(6)),
        ("3.5km", u.Distance, u.km(3.5)),
        ("5m/s", u.Speed, u.mps(5)),
        ("3m²", u.Area, u.m2(3)),
        ("8s⁻¹", u.Frequency, u.Hz(8)),
        ("2m/s²", u.Acceleration, u.mps2(2)),
        ("4m/s/s", u.Acceleration, u.mps2(4)),
    ],
)
def test_parse(text: str, quantity: t.Type[u.Quantity], expected_result: u.Quantity):
    assert quantity.parse(text) == expected_result
