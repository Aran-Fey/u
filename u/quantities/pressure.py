from .force import FORCE, newtons
from .area import AREA, square_meters
from ..quantity import Quantity
from ..capital_quantities import DIV
from ..unit import Unit
from ..prefixes import kilo


# fmt: off
__all__ = [
    "PRESSURE",
    "Pressure",
    "pascals", "pascal", "Pa",
    "kilopascals", "kilopascal", "kPa",
    "bars", "bar",
    "atmospheres", "atmosphere", "atm",
    "torrs", "torr", "mmHg",
    "psi",
]
# fmt: on


PRESSURE = DIV[FORCE, AREA]

Pressure = Quantity[PRESSURE]


pascals = pascal = Pa = Unit(newtons / square_meters, "Pa")
kilopascals = kilopascal = kPa = kilo(pascal)
bars = bar = Unit(Pressure, "bar", 100_000 * pascal.multiplier)
atmospheres = atmosphere = atm = Unit(Pressure, "atm", 101_325 * pascal.multiplier)
torrs = torr = mmHg = Unit(Pressure, "torr", (101_325 / 760) * pascal.multiplier)
psi = Unit(Pressure, "psi", 6894.757293168 * pascal.multiplier)
