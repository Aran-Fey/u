from ..quantity import Quantity
from ..quantity_caps import QUANTITY
from ..unit import Unit

__all__ = ["TEMPERATURE", "Temperature", "kelvins", "kelvin", "K"]


class TEMPERATURE(QUANTITY):
    pass


Temperature = Quantity[TEMPERATURE]


# FIXME: What happens if you add two temperatures?
kelvins = kelvin = K = Unit(Temperature, "K", 1)
# celsius = C = Unit(Temperature, "°C", offset=273.15)
# fahrenheit = F = Unit(Temperature, "°F", formula=((BASE_UNIT - 273.15) * 1.8) + 32)
