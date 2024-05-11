from ..quantity import Quantity
from ..quantity_caps import QUANTITY
from ..unit import Unit


__all__ = ["LUMINOUS_INTENSITY", "LuminousIntensity", "candelas", "candela", "cd"]


class LUMINOUS_INTENSITY(QUANTITY):
    pass


LuminousIntensity = Quantity[LUMINOUS_INTENSITY]


candelas = candela = cd = Unit(LuminousIntensity, "cd", 1)
