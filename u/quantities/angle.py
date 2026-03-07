import decimal

from ..quantity import Quantity
from ..capital_quantities import QUANTITY
from ..unit import Unit


# fmt: off
__all__ = [
    "ANGLE",
    "Angle",
    "radians", "radian", "rad",
    "degrees", "degree", "deg",
    "gradians", "gradian", "gons", "gon",
    "turns", "turn", "tr",
    "arcminutes", "arcminute", "arcmin",
    "arcseconds", "arcsecond", "arcsec",
]
# fmt: on


# Standard PI with high precision for Decimal math
PI = decimal.Decimal("3.1415926535897932384626433832795028841971")


class ANGLE(QUANTITY):
    pass


Angle = Quantity[ANGLE]


radians = radian = rad = Unit(Angle, "rad", 1)
degrees = degree = deg = Unit(Angle, "°", 2 * PI / 360)
gradians = gradian = gons = gon = Unit(Angle, "ᵍ", 2 * PI / 400)
turns = turn = tr = Unit(Angle, "tr", 2 * PI)
arcminutes = arcminute = arcmin = Unit(Angle, "′", PI / 10800)
arcseconds = arcsecond = arcsec = Unit(Angle, "″", PI / 648000)
