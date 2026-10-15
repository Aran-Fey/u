import decimal

from .energy import ENERGY, joules
from .duration import DURATION, seconds
from ..prefixes import kilo, mega
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


watts = watt = W = Unit(joules / seconds, "W", systems={"metric"})
kilowatts = kilowatt = kW = kilo(watts)
megawatts = megawatt = MW = mega(watts)
horsepower = hp = Unit(
    Power, "hp", decimal.Decimal("745.69987158227") * watt.multiplier, systems={"imperial"}
)
