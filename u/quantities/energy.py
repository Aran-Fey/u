import decimal

from .force import FORCE, newtons
from .distance import DISTANCE, meters
from ..quantity import Quantity
from ..capital_quantities import MUL
from ..unit import Unit


# fmt: off
__all__ = [
    "ENERGY",
    "Energy",
    "joules", "joule", "J",
    "calories", "calorie", "cal",
    "kilocalories", "kilocalorie", "kcal",
    "kilowatt_hours", "kilowatt_hour", "kWh",
    "electronvolts", "electronvolt", "eV",
    "ergs", "erg",
    "btus", "btu", "BTU",
]
# fmt: on


ENERGY = MUL[FORCE, DISTANCE]

Energy = Quantity[ENERGY]


joules = joule = J = Unit(newtons * meters, "J", systems={"metric"})
calories = calorie = cal = Unit(Energy, "cal", decimal.Decimal("4.184") * joule.multiplier)
kilocalories = kilocalorie = kcal = Unit(Energy, "kcal", 4184 * joule.multiplier)
kilowatt_hours = kilowatt_hour = kWh = Unit(Energy, "kWh", 3600000 * joule.multiplier)
electronvolts = electronvolt = eV = Unit(
    Energy, "eV", decimal.Decimal("1.602176634e-19") * joule.multiplier, systems={"technical"}
)
ergs = erg = Unit(Energy, "erg", decimal.Decimal("1e-7") * joule.multiplier, systems={"metric"})
btus = btu = BTU = Unit(
    Energy, "BTU", decimal.Decimal("1055.05585262") * joule.multiplier, systems={"imperial"}
)
