import decimal

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


grams = gram = g = Unit(Mass, "g", 1, systems={"metric"})

# Careful: "ton" is not the same thing as "tonne".
metric_tons = metric_ton = tonnes = tonne = t = Unit(Mass, "t", 1000000, systems={"metric"})

pounds = pound = lb = Unit(Mass, "lb", decimal.Decimal("453.59237"), systems={"imperial"})
ounces = ounce = oz = Unit(Mass, "oz", decimal.Decimal("28.349523125"), systems={"imperial"})
stones = stone = st = Unit(Mass, "st", decimal.Decimal("6350.29318"), systems={"imperial"})
slugs = slug = Unit(Mass, "slug", decimal.Decimal("14593.9029"), systems={"imperial"})
daltons = dalton = Da = Unit(Mass, "Da", decimal.Decimal("1.66053906660e-24"))

nanograms = nanogram = ng = nano(grams)
micrograms = microgram = μg = micro(grams)
milligrams = milligram = mg = milli(grams)
centigrams = centigram = cg = centi(grams)
decigrams = decigram = dg = deci(grams)
kilograms = kilogram = kg = kilo(grams)

kilotonnes = kilotonne = kt = kilo(tonnes)
megatonnes = megatonne = Mt = mega(tonnes)
