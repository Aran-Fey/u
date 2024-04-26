from ..quantity_and_unit import Quantity, Unit


__all__ = [
    "Distance",
    "nanometers",
    "nm",
    "micrometers",
    "μm",
    "millimeters",
    "mm",
    "centimeters",
    "cm",
    "decimeters",
    "dm",
    "meters",
    "m",
    "kilometers",
    "km",
]


class Distance(Quantity):
    pass


nanometers = nm = Unit[Distance]("nm", 1e-9)
micrometers = μm = Unit[Distance]("μm", 1e-6)
millimeters = mm = Unit[Distance]("mm", 0.001)
centimeters = cm = Unit[Distance]("cm", 0.01)
decimeters = dm = Unit[Distance]("dm", 0.1)
meters = m = Unit[Distance]("m", 1)
kilometers = km = Unit[Distance]("km", 1_000)
