from __future__ import annotations

from typing import Never


class QuantityMeta(type):
    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...] = (),
        attrs: dict | None = None,
    ):
        if attrs is None:
            attrs = {}

        super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs) -> Never:
        raise TypeError(f"{cls.__name__} cannot be instantiated")

    def __mul__(cls, other_cls) -> QuantityMeta: ...

    def __truediv__(cls, other_cls) -> QuantityMeta: ...


class Quantity(metaclass=QuantityMeta):
    def __init__(self, value: float):
        self.value = value


class Unit[M: Quantity]:
    def __init__(self, Quantity: type[M], symbol: str, multiplier: float):
        self.Quantity = Quantity
        self.symbol = symbol
        self.multiplier = multiplier

    def __truediv__[M1: Quantity, M2: Quantity](
        self: Unit[M1], other_unit: Unit[M2]
    ) -> Unit[M1 | M2]: ...

    def __call__(self, value: float) -> M:
        return self.Quantity(value * self.multiplier)


class Duration(Quantity):
    pass


seconds = Unit(Duration, "s", 1)
minutes = Unit(Duration, "min", 60)
hours = Unit(Duration, "h", 3600)


class Distance(Quantity):
    pass


meters = Unit(Distance, "m", 1)


Velocity = Combine[Distance / Duration]


m: Distance = meters(1)
v: Velocity = (meters / seconds)(3)
