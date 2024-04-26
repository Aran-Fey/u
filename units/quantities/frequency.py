from ..quantity_and_unit import Div
from .duration import Duration, seconds
from .one import One, one


__all__ = ["Frequency", "hertz"]


Frequency = Div[One, Duration]

hertz = one / seconds
hertz.symbol = "Hz"
