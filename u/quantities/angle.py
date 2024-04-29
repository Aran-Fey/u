from math import pi

from ..quantity_and_unit import Quantity, Unit


# fmt: off
__all__ = [
    "Angle",
    "radians", "radian", "rad",
    "degrees", "degree", "deg",
    "gradians", "gradian", "gons", "gon",
    "turns", "turn", "tr",
]
# fmt: on


class Angle(Quantity):
    pass


radians = radian = rad = Unit[Angle]("rad", 1)
degrees = degree = deg = Unit[Angle]("°", 2 * pi / 360)
gradians = gradian = gons = gon = Unit[Angle]("ᵍ", 2 * pi / 400)
turns = turn = tr = Unit[Angle]("tr", 2 * pi)
