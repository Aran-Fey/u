from ..quantity_and_unit import Mul
from .duration import Duration, seconds
from .electric_current import ElectricCurrent, amperes


# fmt: off
__all__ = [
    "ElectricCharge",
    "coulombs", "coulomb", "C",
]
# fmt: on


ElectricCharge = Mul[Duration, ElectricCurrent]

coulombs = coulomb = C = seconds * amperes
coulombs.symbol = "C"
