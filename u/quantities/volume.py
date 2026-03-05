from .distance import DISTANCE, meter
from ..quantity import Quantity
from ..capital_quantities import CUBE
from ..unit import Unit


# fmt: off
__all__ = [
    "VOLUME",
    "Volume",
    "cubic_meters", "cubic_meter", "m3",
    "liters", "liter", "l", "L",
    "milliliters", "milliliter", "ml", "mL",
    "gallons", "gallon", "gal",
    "quarts", "quart", "qt",
    "pints", "pint", "pt",
    "cups", "cup",
    "fluid_ounces", "fluid_ounce", "floz",
    "tablespoons", "tablespoon", "tbsp",
    "teaspoons", "teaspoon", "tsp",
]
# fmt: on


VOLUME = CUBE[DISTANCE]

Volume = Quantity[VOLUME]


cubic_meters = cubic_meter = m3 = meter**3
liters = liter = l = L = Unit(Volume, "L", 0.001)
milliliters = milliliter = ml = mL = Unit(Volume, "mL", 1e-6)

# US Gallon
gallons = gallon = gal = Unit(Volume, "gal", 0.003785411784)
quarts = quart = qt = Unit(Volume, "qt", 0.000946352946)
pints = pint = pt = Unit(Volume, "pt", 0.000473176473)
cups = cup = Unit(Volume, "cup", 0.0002365882365)
fluid_ounces = fluid_ounce = floz = Unit(Volume, "fl oz", 2.95735295625e-5)
tablespoons = tablespoon = tbsp = Unit(Volume, "tbsp", 1.478676478125e-5)
teaspoons = teaspoon = tsp = Unit(Volume, "tsp", 4.92892159375e-6)
