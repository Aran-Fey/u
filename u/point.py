from __future__ import annotations

import functools
import typing as t

from .quantity import Quantity, Q_co


__all__ = ["Point"]


@functools.total_ordering
class Point(t.Generic[Q_co]):
    """
    While `u.Quantity` has the semantics of a "vector" or "distance", `u.Point` has the semantics of
    a "point" or "location": You can't add or multiply points, you can only subtract them and get a
    "distance" as the result, or add a "distance" to get a new "point".

    For example, you would use `u.Quantity[u.DURATION]` to express "the song is 2:37 long", but
    `u.Point[u.DURATION]` to express "the song starts at 3:52 on the CD".
    """

    def __init__(self, quantity: Quantity[Q_co]):
        self._quantity = quantity

    def to_quantity(self) -> Quantity[Q_co]:
        return self._quantity

    def __add__(self, other: Quantity[Q_co]) -> Point[Q_co]:
        return Point(self._quantity + other)

    def __sub__(self, other: Point[Q_co]) -> Quantity[Q_co]:
        return self._quantity - other._quantity

    def __hash__(self) -> int:
        return hash(self._quantity)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, __class__):
            return NotImplemented

        return self._quantity == value._quantity

    def __lt__(self, value: object) -> bool:
        if not isinstance(value, __class__):
            return NotImplemented

        return self._quantity < value._quantity

    def __format__(self, format_spec: str) -> str:
        return format(self._quantity, format_spec)

    def __repr__(self) -> str:
        return f"Point({self._quantity!r})"

    def __str__(self) -> str:
        return str(self._quantity)
