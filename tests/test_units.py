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
