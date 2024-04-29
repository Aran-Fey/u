from ..quantity_and_unit import Div
from .duration import Duration, seconds
from .one import One, one


__all__ = ["Frequency", "hertz", "hertzes", "Hz"]


Frequency = Div[One, Duration]

hertz = hertzes = Hz = one / seconds
hertz.symbol = "Hz"
