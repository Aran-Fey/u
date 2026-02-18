from ..prefixes import nano, micro, milli, centi, deci, kilo, mega
from ..quantity import Quantity
from ..capital_quantities import QUANTITY
from ..unit import Unit


# fmt: off
__all__ = [
    "MASS",
    "Mass",
    "nanograms", "nanogram", "ng",
    "micrograms", "microgram", "μg",
    "milligrams", "milligram", "mg",
    "centigrams", "centigram", "cg",
    "decigrams", "decigram", "dg",
    "grams", "gram", "g",
    "kilograms", "kilogram", "kg",
    "metric_tons", "metric_ton", "tonnes", "tonne", "t", "tons", "ton",
    "kilotons", "kiloton", "kt",
    "megatons", "megaton", "Mt",
]
# fmt: on


class MASS(QUANTITY):
    pass


Mass = Quantity[MASS]


grams = gram = g = Unit(Mass, "g", 1)

# Careful: "ton" is not the same thing as "tonne".
metric_tons = metric_ton = tonnes = tonne = t = Unit(Mass, "t", 1_000_000)
tons = ton = t  # For backwards compat. Delete eventually.

nanograms = nanogram = ng = nano(grams)
micrograms = microgram = μg = micro(grams)
milligrams = milligram = mg = milli(grams)
centigrams = centigram = cg = centi(grams)
decigrams = decigram = dg = deci(grams)
kilograms = kilogram = kg = kilo(grams)

kilotons = kiloton = kt = kilo(tons)
megatons = megaton = Mt = mega(tons)
