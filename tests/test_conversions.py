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
        (u.meters(7), "7 m"),
        (u.kilometers(3.5), "3.5 km"),
        (u.meters_per_second(5), "5 m/s"),
        (u.square_meters(3), "3 m²"),
        (((u.meters / u.second) / u.second)(2), "2 m/s²"),
        ((u.meters / u.second**2)(4), "4 m/s²"),
        ((1 / u.meters)(5), "5 m⁻¹"),
    ],
)
def test_repr(value: u.Quantity, expected_result: str):
    assert repr(value) == expected_result


@pytest.mark.parametrize(
    "value, expected_result",
    [
        (u.kilometers(0), "0 m"),
        (u.meters(7), "7 m"),
        (u.kilometers(3.5), ["3.5 km", "3500 m"]),
        (u.meters(1289), ["1.3 km", "1289 m"]),
        (u.seconds(3600), "1 h"),
        (u.hertz(70_000), "70 kHz"),
        (u.coulombs(20_000), "20 kC"),
        ((1 / u.m)(5), "5 m⁻¹"),
        (u.hours(1000), ["1000 h", "41.7 d"]),
        (u.square_meters(3), "3 m²"),
        (u.mps(3000), "3 km/s"),
        (u.kph(3), "3 km/h"),
        (u.mps(1 / 60), ["1 m/min", "16.7 mm/s"]),
        ((u.bytes / u.second)(10_000), "10 kB/s"),
        (u.square_meters(3_000_000), "3 km²"),
    ],
    ids=lambda value: repr(value),
)
def test_str(value: u.Quantity, expected_result: t.Union[str, t.Sequence[str]]):
    if isinstance(expected_result, str):
        assert str(value) == expected_result
    else:
        assert str(value) in expected_result


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
        ("3C", u.ElectricCharge, u.coulombs(3)),
    ],
)
def test_parse(text: str, quantity: type[u.Quantity], expected_result: u.Quantity):
    assert quantity.parse(text) == expected_result


@pytest.mark.parametrize(
    "text, quantity",
    [
        ("7m", u.Speed),
        ("6 km", u.Area),
        ("5m/s", u.Frequency),
        ("3m²", u.Acceleration),
        ("8s⁻¹", u.ElectricCharge),
    ],
)
def test_parse_as_wrong_quantity(text: str, quantity: type[u.Quantity]):
    with pytest.raises(ValueError):
        quantity.parse(text)
