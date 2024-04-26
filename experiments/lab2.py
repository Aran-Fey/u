from __future__ import annotations

from typing import Any, LiteralString, Self, overload


class Quantity[Id: LiteralString]:
    pass


class Unit[M: Quantity]:
    def __init__(self, Quantity: type[M], symbol: str, multiplier: float):
        self.Quantity = Quantity
        self.symbol = symbol
        self.multiplier = multiplier

    @overload
    def __mul__[M1: Quantity, S: Quantity, M2: Quantity](
        self: Unit[M1 | S], other_unit: Unit[M2 | S]
    ) -> Unit[M1 | M2]: ...

    @overload
    def __mul__[M1: Quantity, M2: Quantity](
        self: Unit[M1], other_unit: Unit[M2]
    ) -> Unit[M1 | M2]: ...

    def __mul__(self, other_unit): ...

    def __truediv__(self, other_unit) -> Unit: ...

    def __call__(self, value: float) -> M:
        return self.Quantity(value)


Duration = Quantity["Duration"]

seconds = Unit(Duration, "s", 1)


Distance = Quantity["Distance"]

meters = Unit(Distance, "m", 1)


Area = CombinedQuantity[Distance * Distance]
Velocity = CombinedQuantity[Distance / Duration]


m: Distance = meters(1)

meters_squared = meters * meters
a: Area = meters_squared(4)
