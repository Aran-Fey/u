import decimal

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


cubic_meters = cubic_meter = m3 = meter**2 * meter
liters = liter = l = L = Unit(Volume, "L", decimal.Decimal("0.001"), systems={"metric"})
milliliters = milliliter = ml = mL = Unit(Volume, "mL", decimal.Decimal("1e-6"), systems={"metric"})

# US Gallon
gallons = gallon = gal = Unit(Volume, "gal", decimal.Decimal("0.003785411784"), systems={"imperial"})
quarts = quart = qt = Unit(Volume, "qt", decimal.Decimal("0.000946352946"), systems={"imperial"})
pints = pint = pt = Unit(Volume, "pt", decimal.Decimal("0.000473176473"), systems={"imperial"})
cups = cup = Unit(Volume, "cup", decimal.Decimal("0.0002365882365"), systems={"imperial"})
fluid_ounces = fluid_ounce = floz = Unit(Volume, "fl oz", decimal.Decimal("2.95735295625e-5"), systems={"imperial"})
tablespoons = tablespoon = tbsp = Unit(Volume, "tbsp", decimal.Decimal("1.478676478125e-5"), systems={"imperial"})
teaspoons = teaspoon = tsp = Unit(Volume, "tsp", decimal.Decimal("4.92892159375e-6"), systems={"imperial"})
