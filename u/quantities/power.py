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
import decimal

from .energy import ENERGY, joules
...
watts = watt = W = Unit(joules / seconds, "W", systems={"metric"})
kilowatts = kilowatt = kW = Unit(Power, "kW", 1000 * watt.multiplier, systems={"metric"})
megawatts = megawatt = MW = Unit(Power, "MW", 1000000 * watt.multiplier, systems={"metric"})
horsepower = hp = Unit(Power, "hp", decimal.Decimal("745.69987158227") * watt.multiplier, systems={"imperial"})

