import decimal

from .distance import DISTANCE, meter, kilometer
from ..quantity import Quantity
from ..capital_quantities import MUL
from ..unit import Unit


# fmt: off
__all__ = [
    "AREA",
    "Area",
    "square_meters", "square_meter", "m2",
    "square_kilometers", "square_kilometer", "km2",
    "hectares", "hectare", "ha",
    "acres", "acre",
]
# fmt: on


AREA = MUL[DISTANCE, DISTANCE]

Area = Quantity[AREA]


square_meters = square_meter = m2 = Unit(meter**2, "m²", systems={"metric"})
square_kilometers = square_kilometer = km2 = Unit(kilometer**2, "km²", systems={"metric"})
hectares = hectare = ha = Unit(Area, "ha", 10_000, systems={"metric"})
acres = acre = Unit(Area, "acre", decimal.Decimal("4046.8564224"), systems={"imperial"})
