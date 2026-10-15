import decimal
import typing as t

import pytest

import u


def test_getitem():
    r = u.Quantity[u.DURATION]
    print(r.exponents)


def test_getitem_with_1_tuple():
    # `X[A]` and `X[(A,)]` are equivalent for regular generics, and `typing` relies on that
    assert u.Quantity[(u.DURATION,)] is u.Duration
    assert u.Quantity[(u.DIV[u.DISTANCE, u.DURATION],)] is u.Speed


def test_annotated():
    annotated = t.Annotated[u.Duration, "metadata"]

    assert t.get_args(annotated) == (u.Duration, "metadata")


def test_get_type_hints():
    def func(
        duration: u.Duration,
        speed: u.Speed,
        annotated: t.Annotated[u.Duration, "metadata"],
    ) -> None: ...

    hints = t.get_type_hints(func, include_extras=True)

    assert hints["duration"] is u.Duration
    assert hints["speed"] is u.Speed
    assert t.get_args(hints["annotated"])[0] is u.Duration


def test_equality():
    assert u.minutes(60) == u.hours(1)


def test_hashing():
    mapping = {u.minutes(60): "foo"}
    assert mapping[u.hours(1)] == "foo"


@pytest.mark.parametrize(
    "a, b",
    [
        (u.minutes(1), u.seconds(60)),
        (u.hours(1.5), u.minutes(90)),
        (u.kilometers(1), u.meters(1000)),
        (u.seconds(decimal.Decimal("1.5")), u.milli(u.seconds)(1500)),
        (u.kph(3.6), u.mps(1)),
        (u.seconds(0), u.hours(0)),
    ],
    ids=repr,
)
def test_equal_quantities_have_equal_hashes(a: u.Quantity, b: u.Quantity):
    assert a == b
    assert b == a
    assert hash(a) == hash(b)
    assert len({a, b}) == 1


def test_zero_has_same_hash_as_0():
    assert u.seconds(0) == 0
    assert hash(u.seconds(0)) == hash(0)


def test_different_quantities_with_same_value_are_unequal():
    assert u.seconds(1) != u.meters(1)
    assert len({u.seconds(1), u.meters(1)}) == 2


@pytest.mark.parametrize(
    "quantity, expected",
    [
        (u.Quantity[u.DIV[u.DURATION, u.DURATION]], u.One),
        (u.Quantity[u.DIV[u.MUL[u.DISTANCE, u.DURATION], u.DURATION]], u.Distance),
        (u.Quantity[u.MUL[u.DURATION, u.DIV[u.ONE, u.DURATION]]], u.One),
    ],
    ids=repr,
)
def test_cancelled_exponents_are_removed(quantity: type[u.Quantity], expected: type[u.Quantity]):
    assert quantity is expected
    assert quantity.exponents == expected.exponents


def test_ratio_of_same_quantity_is_dimensionless():
    ratio = u.minutes(1) / u.seconds(1)

    assert ratio.quantity is u.One
    assert u.One.typecheck(ratio)
    assert ratio.to_number(u.one) == 60


def test_cancelled_units_are_compatible():
    assert (u.m * u.s / u.s).is_compatible_with(u.Distance)

    distance = u.m2(6) / u.m(2)
    assert u.Distance.typecheck(distance)
    assert distance.to_number(u.m) == 3
