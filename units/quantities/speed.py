from ..quantity_and_unit import Div
from .duration import Duration, seconds, hours
from .distance import Distance, meters, kilometers


__all__ = ["Speed", "meters_per_second", "mps", "kilometers_per_hour", "kph"]


Speed = Div[Distance, Duration]

meters_per_second = mps = meters / seconds
kilometers_per_hour = kph = kilometers / hours
