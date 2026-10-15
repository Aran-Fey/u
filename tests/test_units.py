import pytest

import u


def test_ordering():
    assert u.m < u.km
    assert u.hertz <= 1 / u.seconds
    assert u.hours > u.seconds


def test_equality():
    assert u.hertz == 1 / u.seconds


def test_unit_math_gives_predefined_units():
    assert 1 / u.seconds == u.hertz
    assert u.mega(1 / u.seconds) == u.megahertz
    assert repr((1 / u.seconds)(5)) == "5 Hz"


@pytest.mark.parametrize(
    "symbol, expected_unit",
    [
        ("m/(s*A)", u.m / u.s / u.A),
        ("kg/(m*s²)", u.kg / u.m / u.s**2),
        (" m / ( s * A ) ", u.m / u.s / u.A),
        ("(m*s)²", u.m**2 * u.s**2),
        ("m/(s*A)²", u.m / u.s**2 / u.A**2),
        ("1/(s*A)", 1 / (u.s * u.A)),
        # The old style without parentheses still works
        ("m/s/A", u.m / u.s / u.A),
        ("m/s*A", u.m / u.s * u.A),
        # Prefixes applied to parenthesized groups
        ("k(m²)", u.kilo(u.m2)),
        ("k(m²)*s", u.kilo(u.m2) * u.s),
        ("k(m/(s*A))", u.kilo(u.m / u.s / u.A)),
    ],
)
def test_parse_compound_unit(symbol: str, expected_unit: u.Unit):
    assert u.Unit.parse(symbol) == expected_unit


@pytest.mark.parametrize(
    "symbol", ["m/(s", "m)", "(m*s", "()", "m/", "m//s", "k()", "x(m)", "s(m)"]
)
def test_parse_invalid_compound_unit(symbol: str):
    with pytest.raises(ValueError):
        u.Unit.parse(symbol)


@pytest.mark.parametrize(
    "unit, expected_symbol",
    [
        # Created in "unusual" order first, to make sure the symbol doesn't depend on that
        (u.m * u.K, "K*m"),
        (u.K * u.m, "K*m"),
        (u.s * u.m, "m*s"),
        (u.m / (u.mol * u.K), "m/(K*mol)"),
        (u.m / (u.K * u.mol), "m/(K*mol)"),
        (u.mol * u.K**2 / u.m, "K²*mol/m"),
        (1 / (u.mol * u.K), "K⁻¹*mol⁻¹"),
        # Registered units keep their symbol
        ((1 / u.s) * u.m, "m/s"),
        (u.m * u.kg / u.s**2, "N"),
    ],
)
def test_generated_symbols_are_sorted(unit: u.Unit, expected_symbol: str):
    # Numerator first, then denominator, each sorted by code point
    assert unit.symbol == expected_symbol


ROUND_TRIP_UNITS = [
    u.m / (u.kg * u.A),
    u.m**2 / (u.s * u.A * u.K),
    1 / (u.s * u.A),
    u.kilo(u.m2) * u.s,
    u.kilo(u.m2) / (u.s * u.A),
]


@pytest.mark.parametrize("unit", ROUND_TRIP_UNITS, ids=lambda unit: unit.symbol)
def test_generated_symbols_can_be_parsed(unit: u.Unit):
    assert u.Unit.parse(unit.symbol) == unit


@pytest.mark.parametrize("unit", ROUND_TRIP_UNITS, ids=lambda unit: unit.symbol)
def test_prefixed_generated_symbols_can_be_parsed(unit: u.Unit):
    # This also makes sure that the prefix never ends up in the denominator
    prefixed = u.kilo(unit)

    assert prefixed(1) == unit(1000)
    assert u.Unit.parse(prefixed.symbol) == prefixed
