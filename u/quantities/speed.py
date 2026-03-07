from .distance import DISTANCE, meters, kilometers, miles, nautical_miles
from .duration import DURATION, seconds, hours
from ..quantity import Quantity
from ..capital_quantities import DIV
from ..unit import Unit


__all__ = [
    "SPEED",
    "Speed",
    "meters_per_second", "mps",
    "kilometers_per_hour", "kph",
    "miles_per_hour", "mph",
    "knots", "knot", "kn",
    "mach", "Ma",
]


SPEED = DIV[DISTANCE, DURATION]

Speed = Quantity[SPEED]

meters_per_second = mps = meters / seconds
kilometers_per_hour = kph = kilometers / hours
miles_per_hour = mph = miles / hours
knots = knot = kn = nautical_miles / hours
mach = Ma = Unit(Speed, "Ma", 343, systems={"technical"})
