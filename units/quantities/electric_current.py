from ..quantity_and_unit import Quantity, Unit


__all__ = ["ElectricCurrent", "ampere", "A"]


class ElectricCurrent(Quantity):
    pass


ampere = A = Unit[ElectricCurrent]("A", 1)
