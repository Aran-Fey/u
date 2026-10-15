import pytest

import u


def test_prefix_on_base_unit():
    km = u.kilo(u.meters)

    assert km.symbol == "km"
    assert km.multiplier == 1000
    assert km(1) == u.meters(1_000)


def test_prefix_on_registered_compound_unit():
    assert u.kilo(u.hertz)(1) == u.hertz(1_000)


def test_prefix_on_compound_unit():
    with pytest.raises(ValueError):
        u.kilo(u.square_meters)


# The micro prefix is commonly written as "µ" (MICRO SIGN), "μ" (GREEK SMALL LETTER MU) or "u"
MICRO_SPELLINGS = ["\N{MICRO SIGN}", "\N{GREEK SMALL LETTER MU}", "u"]


@pytest.mark.parametrize("micro", MICRO_SPELLINGS, ids=ascii)
@pytest.mark.parametrize(
    "unit_symbol, expected_unit",
    [("s", u.microseconds), ("m", u.micrometers), ("g", u.micrograms)],
)
def test_parse_micro_spellings(micro: str, unit_symbol: str, expected_unit: u.Unit):
    assert u.Unit.parse(micro + unit_symbol) == expected_unit
    assert u.Quantity.parse(f"5{micro}{unit_symbol}") == expected_unit(5)


@pytest.mark.parametrize("micro", MICRO_SPELLINGS, ids=ascii)
def test_format_with_micro_spellings(micro: str):
    assert f"{u.ms(1):{micro}s}" == "1000 µs"


def test_micro_sign_is_used_for_output():
    assert str(u.microseconds(5)) == "5 µs"
    assert u.micro.symbol == "\N{MICRO SIGN}"


def test_u_is_not_a_unit_on_its_own():
    with pytest.raises(ValueError):
        u.Unit.parse("u")


@pytest.mark.parametrize(
    "alias, unit",
    [
        ("us", u.microseconds),
        ("usec", u.microseconds),
        ("um", u.micrometers),
        ("ug", u.micrograms),
    ],
)
def test_ascii_micro_aliases(alias: str, unit: u.Unit):
    assert getattr(u, alias) is unit
