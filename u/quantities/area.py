from ..quantity_and_unit import Mul
from .distance import Distance, meter, kilometer


# fmt: off
__all__ = [
    "Area",
    "square_meters", "square_meter", "m2",
    "square_kilometers", "square_kilometer", "km2",
]
# fmt: on


Area = Mul[Distance, Distance]

square_meters = square_meter = m2 = meter * meter
square_kilometers = square_kilometer = km2 = kilometer * kilometer
