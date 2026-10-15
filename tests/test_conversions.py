import decimal
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
    ids=lambda value: value.symbol if isinstance(value, u.Unit) else repr(value),
)
def test_to_number(value: u.Quantity, unit: u.Unit, expected_result: float):
    result = value.to_number(unit)
    assert result == pytest.approx(expected_result)


def test_to_number_error():
    with pytest.raises(ValueError):
        u.hours(3).to_number(u.meters)  # type: ignore


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
        (u.inches(63360), "1 mi"),
        (u.centimeters(160934.4), "1.6 km"),
        (u.kilometers(0), "0 m"),
        (u.meters(7), "7 m"),
        (u.kilometers(3.5), ["3.5 km", "3500 m"]),
        (u.meters(1289), ["1.3 km", "1289 m"]),
        (u.seconds(3600), "1 h"),
        (u.hertz(70_000), "70 kHz"),
        (u.coulombs(20_000), "20 kC"),
        ((1 / u.m)(5), "5 m⁻¹"),
        (u.hours(1000), ["1000 h", "41.7 d", "6.0 wk"]),
        (u.square_meters(3), "3 m²"),
        (u.mps(3000), "3 km/s"),
        (u.kph(3), "3 km/h"),
        (u.mps(1 / 60), ["1 m/min", "16.7 mm/s"]),
        ((u.bytes / u.second)(10_000), "10 kB/s"),
        (u.square_meters(3_000_000), "3 km²"),
        (u.meters(-3), "-3 m"),
        (u.meters(-3000), "-3 km"),
        (u.seconds(0.0015), "1.5 ms"),
        (u.seconds(0.000002), "2 µs"),
        (u.seconds(-0.0015), "-1.5 ms"),
    ],
    ids=lambda value: repr(value),
)
def test_str(value: u.Quantity, expected_result: t.Union[str, t.Sequence[str]]):
    if isinstance(expected_result, str):
        assert str(value) == expected_result
    else:
        assert str(value) in expected_result


@pytest.mark.parametrize(
    "value, format_, expected_result",
    [
        (u.kilometers(0), "", "0 m"),
        (u.kilometers(0), "dm", "0 dm"),
        (u.kilometers(5), "m", "5000 m"),
        (u.kilometers(1.234), "+.2f km", "+1.23 km"),
        (u.kilometers(1), "m:dam", "100 dam"),
        (u.meters(1), "dam:km", "0.1 dam"),
        (u.meters(1), "0.2f dam:km", "0.10 dam"),
        (u.seconds(90), "", "90 s"),
        (u.seconds(90), ":", "1:30"),
        (u.seconds(90), "MM:SS", "01:30"),
        (u.seconds(90), "H:MM:SS", "0:01:30"),
        (u.seconds(90), "HH:MM:SS", "00:01:30"),
        (u.seconds(90.12345), ".2f :", "1:30.12"),
        (u.seconds(90.12345), ":", "1:30.12345"),
        (u.seconds(3725), ":", "1:02:05"),
        (u.seconds(5), "SS", "05"),
        (u.seconds(5), "M:SS", "0:05"),
        (u.seconds(61.5), "MM:SS", "01:01.5"),
        (u.minutes(1.5), "MM:SS", "01:30"),
        (u.hours(1), "H:MM:SS", "1:00:00"),
        (u.ms(1500), "M:SS", "0:01.5"),
        (u.seconds(decimal.Decimal("90.5")), ":", "1:30.5"),
    ],
    ids=lambda value: repr(value),
)
def test_format(value: u.Quantity, format_: str, expected_result: t.Union[str, t.Sequence[str]]):
    result = format(value, format_)

    if isinstance(expected_result, str):
        assert result == expected_result
    else:
        assert result in expected_result


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


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("30", u.seconds(30)),
        ("1:30", u.seconds(90)),
        ("1:02:05", u.seconds(3725)),
        ("30.5", u.seconds(30.5)),
        ("1:30.5", u.seconds(90.5)),
        ("1:02:05.25", u.seconds(3725.25)),
        ("0:00.001", u.ms(1)),
        ("1:59.999", u.seconds(119.999)),
        # The leading number isn't capped
        ("90", u.seconds(90)),
        ("90:00", u.minutes(90)),
        ("100:00:00", u.hours(100)),
    ],
)
def test_parse_colon_duration(text: str, expected_result: u.Duration):
    assert u.Duration.parse(text) == expected_result


@pytest.mark.parametrize(
    "text",
    [
        "1:2:3:4",
        "1.5:30",
        "1:30.",
        "1:30.5.5",
        ":30",
        "1::30",
        "1:3x",
        "1:-30",
        "1:30e1",
        # Numbers after the first one must be between 00 and 59...
        "1:60",
        "1:75",
        "1:60:00",
        "1:00:60",
        # ... and have exactly 2 digits
        "1:5",
        "1:005",
        "1:7.5",
        "1:5:00",
    ],
)
def test_parse_invalid_colon_duration(text: str):
    with pytest.raises(ValueError):
        u.Duration.parse(text)


@pytest.mark.parametrize(
    "value",
    [u.seconds(90.12345), u.seconds(3725.5), u.ms(1500), u.minutes(2.25), u.hours(100)],
    ids=repr,
)
@pytest.mark.parametrize("format_", [":", "SS", "M:SS", "MM:SS", "H:MM:SS", "HH:MM:SS"])
def test_colon_duration_round_trip(value: u.Duration, format_: str):
    assert u.Duration.parse(format(value, format_)) == value
