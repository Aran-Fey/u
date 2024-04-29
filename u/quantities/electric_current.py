from ..quantity_and_unit import Quantity, Unit


# fmt: off
__all__ = [
    "ElectricCurrent",
    "amperes", "ampere", "A",
]
# fmt: on


class ElectricCurrent(Quantity):
    pass


amperes = ampere = A = Unit[ElectricCurrent]("A", 1)
