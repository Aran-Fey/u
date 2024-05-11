from .duration import DURATION, seconds
from .one import ONE, one
from ..prefixes import kilo, mega, giga
from ..quantity import Quantity
from ..quantity_caps import DIV


# fmt: off
__all__ = [
    "FREQUENCY",
    "Frequency",
    "hertzes", "hertz", "Hz",
    "kilohertzes", "kilohertz", "KHz",
    "megahertzes", "megahertz", "MHz",
    "gigahertzes", "gigahertz", "GHz",
]
# fmt: on


FREQUENCY = DIV[ONE, DURATION]


Frequency = Quantity[FREQUENCY]


hertzes = hertz = Hz = one / seconds
hertz.symbol = "Hz"

kilohertzes = kilohertz = KHz = kilo(hertz)
megahertzes = megahertz = MHz = mega(hertz)
gigahertzes = gigahertz = GHz = giga(hertz)
