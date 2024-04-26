from ..quantity_and_unit import Quantity, Unit


__all__ = [
    "Mass",
    "nanograms",
    "ng",
    "micrograms",
    "μg",
    "milligrams",
    "mg",
    "centigrams",
    "cg",
    "decigrams",
    "dg",
    "grams",
    "g",
    "kilograms",
    "kg",
    "tons",
    "t",
]


class Mass(Quantity):
    pass


nanograms = ng = Unit[Mass]("ng", 1e-9)
micrograms = μg = Unit[Mass]("μg", 1e-6)
milligrams = mg = Unit[Mass]("mg", 0.001)
centigrams = cg = Unit[Mass]("cg", 0.01)
decigrams = dg = Unit[Mass]("dg", 0.1)
grams = g = Unit[Mass]("g", 1)
kilograms = kg = Unit[Mass]("kg", 1_000)
tons = t = Unit[Mass]("t", 1_000_000)
