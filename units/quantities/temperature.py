from ..quantity_and_unit import BASE_UNIT, Quantity, Unit


__all__ = ["Temperature", "kelvin", "K", "celsius", "C", "fahrenheit", "F"]


class Temperature(Quantity):
    pass


# FIXME: What happens if you add two temperatures?
kelvin = K = Unit[Temperature]("K", 1)
celsius = C = Unit[Temperature]("°C", offset=273.15)
fahrenheit = F = Unit[Temperature]("°F", formula=((BASE_UNIT - 273.15) * 1.8) + 32)
