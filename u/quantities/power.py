from .energy import ENERGY, joules
from .duration import DURATION, seconds
from ..quantity import Quantity
from ..capital_quantities import DIV
from ..unit import Unit


# fmt: off
__all__ = [
    "POWER",
    "Power",
    "watts", "watt", "W",
    "kilowatts", "kilowatt", "kW",
    "megawatts", "megawatt", "MW",
    "horsepower", "hp",
]
# fmt: on


POWER = DIV[ENERGY, DURATION]

Power = Quantity[POWER]


watts = watt = W = Unit(joules / seconds, "W")
kilowatts = kilowatt = kW = Unit(Power, "kW", 1000 * watt.multiplier)
megawatts = megawatt = MW = Unit(Power, "MW", 1_000_000 * watt.multiplier)
horsepower = hp = Unit(Power, "hp", 745.69987158227 * watt.multiplier)
