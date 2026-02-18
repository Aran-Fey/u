import u


def test_getitem():
    r = u.Quantity[u.DURATION]
    print(r.exponents)


def test_equality():
    assert u.minutes(60) == u.hours(1)
