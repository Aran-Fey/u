from __future__ import annotations

import collections
import functools
import math
import re
import sys
import types
import typing as t

import u

from ._utils import is_union
from .quantity_caps import QUANTITY, DIV, MUL, _MUL


__all__ = ["Quantity"]


Q_co = t.TypeVar("Q_co", bound=QUANTITY, covariant=True)
Q2 = t.TypeVar("Q2", bound=QUANTITY)


NUMBER_WITH_UNIT_REGEX = re.compile(r"([+-]?[0-9._]+)(.*)")


if sys.version_info >= (3, 9, 2):
    GenericAlias = types.GenericAlias
else:
    GenericAlias = t._GenericAlias


class QuantityAlias(GenericAlias):
    @functools.cached_property
    def exponents(self) -> t.Mapping[t.Type[QUANTITY], int]:
        [quantity] = t.get_args(self)

        while is_union(quantity):
            quantity = t.get_args(quantity)[0]

        exponents = collections.Counter()
        _add_exponents(quantity, exponents)
        return exponents


def _add_exponents(quantity, exponents: collections.Counter[t.Type[QUANTITY]]) -> None:
    # `quantity` can be:
    #
    # 1. A parameterized MUL or DIV
    # 2. A subclass of `QUANTITY`
    # 3. A Union
    if isinstance(quantity, type):
        exponents[quantity] += 1
        return

    origin = t.get_origin(quantity)
    args = t.get_args(quantity)

    if origin is t.Union:
        # If it's a Union, then the subtypes must all be equivalent. So we simply pick one and
        # recurse.
        quantity = args[0]
        _add_exponents(quantity, exponents)
    elif origin is _MUL:
        _add_exponents(args[0], exponents)
        _add_exponents(args[1], exponents)
    else:
        _add_exponents(args[0], exponents)

        exps = collections.Counter()
        _add_exponents(args[1], exps)
        exponents -= exps


class QuantityMeta(type(t.Generic)):
    @property
    def exponents(cls) -> t.Mapping[t.Type[QUANTITY], int]:
        # This implementation is only relevant for un-parameterized `Quantity`. Parameterized
        # quantities are implemented in `QuantityAlias`.
        return {}


class Quantity(t.Generic[Q_co], metaclass=QuantityMeta):
    """
    Represents a measurable quantity, like mass or distance.

    # FIXME: Fix docstring

    To create a new Quantity, simply make a subclass:

    ```
    class Tastiness(u.Quantity):
        pass
    ```

    To derive a new Quantity from existing ones, use `u.Mul`, `u.Div` and `u.Square`:

    ```
    Area = u.Square[u.Distance]
    ElectricCharge = u.Mul[u.Duration, u.ElectricCurrent]
    Speed = u.Div[u.Distance, u.Duration]
    ```

    Unfortunately type checkers don't understand math, which can sometimes lead to unexpected
    problems:

    ```
    BadAcceleration = u.Div[u.Distance, u.Square[u.Duration]]

    # Type checking error! The type checker thinks that m/s/s
    # is not compatible with Distance/Duration²
    accel: BadAcceleration = (u.m / u.s / u.s)(3)
    ```

    In cases like this, you must define your Quantity as a `u.AnyOf`:

    ```
    GoodAcceleration = u.AnyOf[
        u.Div[u.Distance, u.Square[u.Duration]],
        u.Div[u.Div[u.Distance, u.Duration], u.Duration],
    ]
    ```
    """

    if not t.TYPE_CHECKING:

        def __class_getitem__(cls, subtype):
            return QuantityAlias(cls, subtype)

    def __init__(self, value: float, unit: u.Unit[Q_co]):
        self._value = value
        self.unit = unit

    def to(self, unit: u.Unit[Q_co]) -> Quantity[Q_co]:
        return Quantity(self.to_number(unit), unit)

    def to_number(self, unit: u.Unit[Q_co]) -> float:
        return self._value * (self.unit.multiplier / unit.multiplier)

    @classmethod
    def parse(cls, text: str) -> Quantity[Q_co]:
        match = NUMBER_WITH_UNIT_REGEX.match(text)
        if not match:
            raise ValueError(f"Cannot parse {text!r} as a Quantity")

        number_str, unit_str = match.groups()
        number = float(number_str)
        unit = u.Unit.parse(unit_str, cls)

        return cls(number, unit)

    @classmethod
    def typecheck(cls, other: Quantity) -> t.TypeGuard[Quantity[Q_co]]:
        return cls.exponents == type(other).exponents

    def is_compatible_with(self, other: Quantity) -> t.TypeGuard[Quantity[Q_co]]:
        return type(self).exponents == type(other).exponents

    def __eq__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        if not self.is_compatible_with(quantity):
            return False

        num = self.to_number(quantity.unit)
        return math.isclose(num, quantity._value)

    def __lt__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        if not self.is_compatible_with(quantity):
            return False

        num = self.to_number(quantity.unit)
        return num < quantity._value and not math.isclose(num, quantity._value)

    def __le__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        if not self.is_compatible_with(quantity):
            return False

        num = self.to_number(quantity.unit)
        return num < quantity._value or math.isclose(num, quantity._value)

    def __gt__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        if not self.is_compatible_with(quantity):
            return False

        num = self.to_number(quantity.unit)
        return num > quantity._value and not math.isclose(num, quantity._value)

    def __ge__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        if not self.is_compatible_with(quantity):
            return False

        num = self.to_number(quantity.unit)
        return num > quantity._value or math.isclose(num, quantity._value)

    def __add__(self, quantity: Quantity[Q_co]) -> Quantity[Q_co]:
        return Quantity(
            self._value + quantity.to_number(self.unit),
            self.unit,
        )

    def __sub__(self, quantity: Quantity[Q_co]) -> Quantity[Q_co]:
        return Quantity(
            self._value - quantity.to_number(self.unit),
            self.unit,
        )

    def __mul__(self, quantity: Quantity[Q2]) -> Quantity[MUL[Q_co, Q2]]:
        return Quantity(
            self._value * quantity._value,
            self.unit * quantity.unit,
        )

    @t.overload
    def __truediv__(self, number: float, /) -> Quantity[Q_co]: ...

    @t.overload
    def __truediv__(self, quantity: Quantity[Q2], /) -> Quantity[DIV[Q_co, Q2]]: ...

    def __truediv__(self, other: t.Union[float, Quantity[Q2]]) -> Quantity:
        if isinstance(other, Quantity):
            return Quantity(
                self._value / other._value,
                self.unit / other.unit,
            )
        else:
            return Quantity(self._value / other, self.unit)

    @t.overload
    def __rtruediv__(self, number: float, /) -> Quantity[DIV[u.ONE, Q_co]]: ...

    @t.overload
    def __rtruediv__(self, quantity: Quantity[Q2], /) -> Quantity[DIV[Q2, Q_co]]: ...

    def __rtruediv__(self, other: t.Union[float, Quantity[Q2]]) -> Quantity[DIV]:
        if isinstance(other, Quantity):
            return Quantity(
                other._value / self._value,
                other.unit / self.unit,
            )
        else:
            return Quantity(
                other / self._value,
                u.one / self.unit,
            )

    def __repr__(self) -> str:
        return f"{self._value}{self.unit.symbol}"
