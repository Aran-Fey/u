from ..quantity_and_unit import Quantity, Unit


__all__ = [
    "FileSize",
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


class FileSize(Quantity):
    pass


nanograms = ng = Unit[FileSize]("ng", 1e-9)
micrograms = μg = Unit[FileSize]("μg", 1e-6)
milligrams = mg = Unit[FileSize]("mg", 0.001)
centigrams = cg = Unit[FileSize]("cg", 0.01)
decigrams = dg = Unit[FileSize]("dg", 0.1)
grams = g = Unit[FileSize]("g", 1)
kilograms = kg = Unit[FileSize]("kg", 1_000)
tons = t = Unit[FileSize]("t", 1_000_000)
