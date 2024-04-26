from __future__ import annotations

from typing import *


class Quantity:
    def __init__(self, value: float, unit: Unit[Self]):
        self._value = value
        self._unit = unit

    def to_number(self, unit: Unit[Self]) -> float:
        return self._value * unit.multiplier

    def __repr__(self) -> str:
        return f"{self._value}{self._unit.symbol}"


class Mul[A: "Quantity | Mul | Div", B: Quantity](Quantity): ...


class Div[A: "Quantity | Mul | Div", B: Quantity](Quantity): ...


class One(Quantity):
    """
    Represents the absence of a quantity. Used to create "inverted" quantities like `Frequency =
    Div[One, Duration]`.
    """


class Unit[Q: Quantity | Mul | Div]:
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

    def __mul__[Q2: Quantity](
        self,
        other_unit: Unit[Q2],
    ) -> Unit[Mul[Q, Q2]]:
        return Unit(
            f"{self.symbol}*{other_unit.symbol}",
            self.multiplier * other_unit.multiplier,
        )

    def __call__(self, value: float) -> Q:
        return cast(Q, Quantity(value, self))


class Duration(Quantity):
    pass


class Distance(Quantity):
    pass


meters = Unit[Distance]("m", 1)


d: Distance = meters(3)


Area = Mul[Distance, Distance]
Speed = Div[Distance, Duration]
Accel = Div[Speed, Duration]

square_meters = meters * meters
a: Area = square_meters(4)
print(a)
print(a.to_number(square_meters))
print(a.to_number(meters))
