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
