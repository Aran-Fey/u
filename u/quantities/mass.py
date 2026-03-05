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
    "metric_tons", "metric_ton", "tonnes", "tonne", "t",
    "kilotonnes", "kilotonne", "kt",
    "megatonnes", "megatonne", "Mt",
    "pounds", "pound", "lb",
    "ounces", "ounce", "oz",
    "stones", "stone", "st",
    "slugs", "slug",
    "daltons", "dalton", "Da",
]
# fmt: on


class MASS(QUANTITY):
    pass


Mass = Quantity[MASS]


grams = gram = g = Unit(Mass, "g", 1)

# Careful: "ton" is not the same thing as "tonne".
metric_tons = metric_ton = tonnes = tonne = t = Unit(Mass, "t", 1_000_000)

pounds = pound = lb = Unit(Mass, "lb", 453.59237)
ounces = ounce = oz = Unit(Mass, "oz", 28.349523125)
stones = stone = st = Unit(Mass, "st", 6350.29318)
slugs = slug = Unit(Mass, "slug", 14593.9029)
daltons = dalton = Da = Unit(Mass, "Da", 1.66053906660e-24)

nanograms = nanogram = ng = nano(grams)
micrograms = microgram = μg = micro(grams)
milligrams = milligram = mg = milli(grams)
centigrams = centigram = cg = centi(grams)
decigrams = decigram = dg = deci(grams)
kilograms = kilogram = kg = kilo(grams)

kilotonnes = kilotonne = kt = kilo(tonnes)
megatonnes = megatonne = Mt = mega(tonnes)
