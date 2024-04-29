from __future__ import annotations

import math
from typing import Generic, TypeVar, Union
from typing_extensions import Self

from ._utils import cached


__all__ = ["Quantity", "Mul", "Div", "Unit"]


class Quantity:
    """
    Represents a measurable quantity, like mass or acceleration.

    FIXME: Correct docstring

    In order to be able to represent compound quantities (like speed, which is distance divided by
    time), this is a generic class that accepts an arbitrary number of type arguments. Each type
    argument represents either a multiplication or, through the use of `Inv`, a division.

    Examples:

    ```
    Distance = Quantity[DISTANCE]  # just distance
    Area = Quantity[DISTANCE, DISTANCE]  # distance squared
    Speed = Quantity[DISTANCE, Inv[DURATION]]  # distance divided by time
    ```

    Unfortunately this isn't ideal: Because type checkers care about the order of the arguments,
    they treat `Quantity[A, B]` as different from `Quantity[B, A]`.
    """

    def __init__(self, value: float, unit: Unit[Self]):
        self._value = value
        self.unit = unit

    def to(self, unit: Unit[Self]) -> Self:
        return Quantity(self.to_number(unit), unit)  # type: ignore

    def to_number(self, unit: Unit[Self]) -> float:
        return self._value * (self.unit.multiplier / unit.multiplier)

    def __eq__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        num = self.to_number(quantity.unit)  # type: ignore
        return math.isclose(num, quantity._value)

    def __lt__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        num = self.to_number(quantity.unit)  # type: ignore
        return num < quantity._value and not math.isclose(num, quantity._value)

    def __le__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        num = self.to_number(quantity.unit)  # type: ignore
        return num < quantity._value or math.isclose(num, quantity._value)

    def __gt__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        num = self.to_number(quantity.unit)  # type: ignore
        return num > quantity._value and not math.isclose(num, quantity._value)

    def __ge__(self, quantity: object, /) -> bool:
        if not isinstance(quantity, __class__):
            return NotImplemented

        num = self.to_number(quantity.unit)  # type: ignore
        return num > quantity._value or math.isclose(num, quantity._value)

    def __add__(self, quantity: Self) -> Self:
        return Quantity(
            self._value + quantity.to_number(self.unit),
            self.unit,  # type: ignore
        )  # type: ignore

    def __sub__(self, quantity: Self) -> Self:
        return Quantity(
            self._value - quantity.to_number(self.unit),
            self.unit,  # type: ignore
        )  # type: ignore

    def __mul__(self, quantity: Quantity) -> Self:
        return Quantity(
            self._value * quantity._value,
            self.unit * quantity.unit,  # type: ignore
        )  # type: ignore

    def __truediv__(self, quantity: Quantity) -> Self:
        return Quantity(
            self._value / quantity._value,
            self.unit / quantity.unit,  # type: ignore
        )  # type: ignore

    def __repr__(self) -> str:
        return f"{self._value}{self.unit.symbol}"


Q = TypeVar("Q", bound=Quantity)
Q2 = TypeVar("Q2", bound=Quantity)


class _Mul(Generic[Q, Q2], Quantity): ...


# Make multiplication commutative, otherwise type checkers would complain every time you do a
# multiplication in the "wrong" order. For example:
#
# electric_charge: Mul[Duration, ElectricCurrent] = ampere(1) * second(1)
Mul = Union[_Mul[Q, Q2], _Mul[Q2, Q]]


class Div(Generic[Q, Q2], Quantity): ...


class Unit(Generic[Q]):
    """
    Represents a unit of measurement for a certain `Quantity`.

    To create your own unit, simply create an instance of this class. Make sure to pass the
    corresponding `Quantity` as a type argument as seen here:

    ```
    seconds = Unit[Duration]("s", 1)
    minutes = Unit[Duration]("min", 60)
    ```
    """

    def __init__(self, symbol: str, multiplier: float):
        self.symbol = symbol
        self.multiplier = multiplier

    @cached
    def __mul__(self, other: Unit[Q2]) -> Unit[Mul[Q, Q2]]:
        return Unit(
            f"{self.symbol}*{other.symbol}",
            self.multiplier * other.multiplier,
        )

    @cached
    def __truediv__(self, other: Unit[Q2]) -> Unit[Div[Q, Q2]]:
        return Unit(f"{self.symbol}/{other.symbol}", self.multiplier / other.multiplier)

    def __call__(self, value: float) -> Q:
        return Quantity(value, self)  # type: ignore

    def __rmul__(self, value: float) -> Q:
        return Quantity(value, self)  # type: ignore
