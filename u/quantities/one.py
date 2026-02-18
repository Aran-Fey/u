from ..quantity import Quantity
from ..capital_quantities import QUANTITY
from ..unit import Unit

__all__ = ["ONE", "One", "ones", "one"]


class ONE(QUANTITY):
    """
    Represents the absence of a quantity. Its primary use is the creation of "inverted" quantities
    like `FREQUENCY = DIV[ONE, DURATION]`, but it can also be used like any other quantity.
    """


One = Quantity[ONE]


ones = one = Unit(One, "1", 1)
# dozens = dozen = Unit(One, "12", 12)
