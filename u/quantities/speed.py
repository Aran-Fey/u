from .distance import DISTANCE, meters, kilometers, miles, nautical_miles
from .duration import DURATION, seconds, hours
from ..quantity import Quantity
from ..capital_quantities import DIV
from ..unit import Unit


# fmt: off
__all__ = [
    "SPEED",
    "Speed",
    "meters_per_second", "mps",
    "kilometers_per_hour", "kph",
    "miles_per_hour", "mph",
    "knots", "knot", "kn",
    "mach", "Ma",
]
# fmt: on


SPEED = DIV[DISTANCE, DURATION]

Speed = Quantity[SPEED]


meters_per_second = mps = Unit(meters / seconds, "m/s", systems={"metric"})
kilometers_per_hour = kph = Unit(kilometers / hours, "km/h", systems={"metric"})
miles_per_hour = mph = Unit(miles / hours, "mph", systems={"imperial"})
knots = knot = kn = Unit(nautical_miles / hours, "kn", systems={"nautical"})
mach = Ma = Unit(Speed, "Ma", 343, systems={"technical"})
