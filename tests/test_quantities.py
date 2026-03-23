import u


def test_getitem():
    r = u.Quantity[u.DURATION]
    print(r.exponents)


def test_equality():
    assert u.minutes(60) == u.hours(1)


def test_hashing():
    mapping = {u.minutes(60): "foo"}
    assert mapping[u.hours(1)] == "foo"
