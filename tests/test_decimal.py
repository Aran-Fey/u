from decimal import Decimal

import u


def test_decimal_quantity():
    dec = Decimal("10.5")
    dist = u.meter(dec)

    assert dist.to_decimal(u.meter) == dec


def test_decimal_math():
    q1 = u.meter(Decimal("10.5"))
    q2 = u.meter(Decimal("5.5"))
    res = q1 + q2
    assert res.to_decimal(u.meter) == Decimal("16.0")


def test_mixed_math():
    q1 = u.meter(Decimal("10.5"))
    q2 = u.meter(5.5)
    res = q1 + q2
    assert res.to_decimal(u.meter) == Decimal("16.0")


def test_decimal_conversion():
    q = u.km(Decimal("1"))
    res = q.to_decimal(u.meter)
    assert res == Decimal("1000")
    assert isinstance(res, Decimal)
