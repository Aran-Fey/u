from ..quantity_and_unit import Div
from .duration import Duration, second, hour
from .speed import Speed, meters_per_second, kilometers_per_hour


# fmt: off
__all__ = [
    "Acceleration",
    "meters_per_second_squared", "mps2",
    "kilometers_per_hour_squared", "kph2",
]
# fmt: on


Acceleration = Div[Speed, Duration]

meters_per_second_squared = mps2 = meters_per_second / second
kilometers_per_hour_squared = kph2 = kilometers_per_hour / hour
