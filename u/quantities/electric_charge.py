from .duration import DURATION, seconds
from .electric_current import ELECTRIC_CURRENT, amperes
from ..quantity import Quantity
from ..quantity_caps import MUL


# fmt: off
__all__ = [
    "ElectricCharge",
    "coulombs", "coulomb", "C",
]
# fmt: on


ELECTRIC_CHARGE = MUL[DURATION, ELECTRIC_CURRENT]

ElectricCharge = Quantity[ELECTRIC_CHARGE]

coulombs = coulomb = C = seconds * amperes
coulombs.symbol = "C"
