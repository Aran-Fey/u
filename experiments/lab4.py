from __future__ import annotations

from typing import *


class Div[T]:
    pass


class Quantity[*Ts]:
    def __init__(self, value: float, unit: Unit[Quantity[*Ts]]):
        self._value = value
        self._unit = unit

    def as_number(self, unit: Unit[Self]) -> float:
        return self._value / unit.multiplier

    def __repr__(self) -> str:
        return f"{self._value}{self._unit.symbol}"


type Multiply[*Ms] = Quantity[*Ms]
type Divide[M1, M2] = Quantity[M1, Div[M2]]


class Unit[M: Quantity]:
    def __init__(self, symbol: str, multiplier: float):
        self.symbol = symbol
        self.multiplier = multiplier

    def __mul__[*Ts, T](
        self: Unit[Quantity[*Ts]],
        other_unit: Unit[Quantity[T]],
    ) -> Unit[Quantity[*Ts, T]]:
        return Unit(
            f"{self.symbol}*{other_unit.symbol}",
            self.multiplier * other_unit.multiplier,
        )

    def __truediv__[*Ts, T](
        self: Unit[Quantity[*Ts]],
        other_unit: Unit[Quantity[T]],
    ) -> Unit[Quantity[*Ts, Div[T]]]:
        return Unit(
            f"{self.symbol}/{other_unit.symbol}",
            self.multiplier / other_unit.multiplier,
        )

    def __call__(self, value: float) -> M:
        return cast(M, Quantity(value, self))


class DURATION:
    pass


Duration = Quantity[DURATION]

seconds = Unit[Duration]("s", 1)


class DISTANCE:
    pass


Distance = Quantity[DISTANCE]

meters = Unit[Distance]("m", 1)


m: Distance = meters(1)


Area = Multiply[DISTANCE, DISTANCE]
square_meters = meters * meters
a: Area = square_meters(4)

print(a)
print(a.as_number(square_meters))
