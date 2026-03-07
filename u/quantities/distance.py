import decimal

from ..prefixes import nano, micro, milli, centi, deci, kilo
from ..quantity import Quantity
from ..capital_quantities import QUANTITY
from ..unit import Unit


# fmt: off
__all__ = [
    "DISTANCE",
    "Distance",
    "nanometers", "nanometer", "nm",
    "micrometers", "micrometer", "μm",
    "millimeters", "millimeter", "mm",
    "centimeters", "centimeter", "cm",
    "decimeters", "decimeter", "dm",
    "meters", "meter", "m",
    "kilometers", "kilometer", "km",
    "light_seconds", "light_second", "ls",
    "light_years", "light_year", "ly",
    "astronomical_units", "astronomical_unit", "au",
    "parsecs", "parsec", "pc",
    "inches", "inch", "in_",
    "feet", "foot", "ft",
    "yards", "yard", "yd",
    "miles", "mile", "mi",
    "nautical_miles", "nautical_mile", "nmi",
    "fathoms", "fathom",
    "mils", "mil",
]
# fmt: on


class DISTANCE(QUANTITY):
    pass


Distance = Quantity[DISTANCE]


meters = meter = m = Unit(Distance, "m", 1, systems={"metric"})
light_seconds = light_second = ls = Unit(Distance, "ls", 299792458)
light_years = light_year = ly = Unit(Distance, "ly", 9460730472580800)
astronomical_units = astronomical_unit = au = Unit(Distance, "au", 149597870700)
parsecs = parsec = pc = Unit(Distance, "pc", decimal.Decimal("3.0856775814913673e16"))

inches = inch = in_ = Unit(Distance, "in", decimal.Decimal("0.0254"), systems={"imperial"})
feet = foot = ft = Unit(Distance, "ft", decimal.Decimal("0.3048"), systems={"imperial"})
yards = yard = yd = Unit(Distance, "yd", decimal.Decimal("0.9144"), systems={"imperial"})
miles = mile = mi = Unit(Distance, "mi", decimal.Decimal("1609.344"), systems={"imperial"})
nautical_miles = nautical_mile = nmi = Unit(Distance, "nmi", 1852, systems={"nautical"})
fathoms = fathom = Unit(Distance, "fathom", decimal.Decimal("1.8288"), systems={"nautical"})
mils = mil = Unit(Distance, "mil", decimal.Decimal("0.0000254"), systems={"imperial"})

nanometers = nanometer = nm = nano(meter)
micrometers = micrometer = μm = micro(meter)
millimeters = millimeter = mm = milli(meter)
centimeters = centimeter = cm = centi(meter)
decimeters = decimeter = dm = deci(meter)
kilometers = kilometer = km = kilo(meter)
