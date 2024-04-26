from ..quantity_and_unit import Quantity, Unit


__all__ = ["LuminousIntensity", "candela", "cd"]


class LuminousIntensity(Quantity):
    pass


candela = cd = Unit[LuminousIntensity]("cd", 1)
