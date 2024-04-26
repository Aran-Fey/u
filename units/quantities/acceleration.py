from ..quantity_and_unit import Div
from .duration import Duration, seconds, hours
from .speed import Speed, meters_per_second, kilometers_per_hour


__all__ = [
    "Acceleration",
    "meters_per_second_squared",
    "mps2",
    "kilometers_per_hour",
    "kph2",
]


Acceleration = Div[Speed, Duration]

meters_per_second_squared = mps2 = meters_per_second / seconds
kilometers_per_hour_squared = kph2 = kilometers_per_hour / hours
