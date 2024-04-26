from ..quantity_and_unit import Mul
from .distance import Distance, meters, kilometers


__all__ = ["Area", "square_meters", "m2", "square_kilometers", "km2"]


Area = Mul[Distance, Distance]

square_meters = m2 = meters * meters
square_kilometers = km2 = kilometers * kilometers
