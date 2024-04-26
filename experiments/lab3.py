from __future__ import annotations

from typing import *


class Quantity[Mul: tuple, Div: tuple]:
    def __mul__(self, other) -> Quantity: ...


class Unit[M: Quantity]:
    def __init__(self, Quantity: type[M], symbol: str, multiplier: float):
        self.Quantity = Quantity
        self.symbol = symbol
        self.multiplier = multiplier

    @overload
    def __mul__[*Muls, *Divs, Mul](
        self: Unit[Quantity[tuple[*Muls], tuple[*Divs]]],
        other_unit: Unit[Quantity[tuple[Mul], tuple[()]]],
    ) -> Unit[Quantity[tuple[*Muls, Mul], tuple[*Divs]]]: ...

    @overload
    def __mul__[*Muls, *Divs, Div](
        self: Unit[Quantity[tuple[*Muls], tuple[*Divs]]],
        other_unit: Unit[Quantity[tuple[()], tuple[Div]]],
    ) -> Unit[Quantity[tuple[*Muls], tuple[*Divs, Div]]]: ...

    @overload
    def __mul__[*Muls, *Divs, Mul, Div](
        self: Unit[Quantity[tuple[*Muls], tuple[*Divs]]],
        other_unit: Unit[Quantity[tuple[Mul], tuple[Div]]],
    ) -> Unit[Quantity[tuple[*Muls, Mul], tuple[*Divs, Div]]]: ...

    def __mul__(self, other_unit): ...  # type: ignore

    def __truediv__(self, other_unit) -> Unit: ...

    def __call__(self, value: float) -> M:
        return self.Quantity(value)


class DURATION:
    pass


Duration = Quantity[tuple[DURATION], tuple[()]]

seconds = Unit(Duration, "s", 1)


class DISTANCE:
    pass


Distance = Quantity[tuple[DISTANCE], tuple[()]]

meters = Unit(Distance, "m", 1)


m: Distance = meters(1)


Area = Distance * Distance
meters_squared = meters * meters
a: Area = meters_squared(4)
