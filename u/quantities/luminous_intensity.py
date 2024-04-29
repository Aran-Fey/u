from ..quantity_and_unit import Quantity, Unit


__all__ = ["LuminousIntensity", "candelas", "candela", "cd"]


class LuminousIntensity(Quantity):
    pass


candelas = candela = cd = Unit[LuminousIntensity]("cd", 1)
