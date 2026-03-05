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


meters = meter = m = Unit(Distance, "m", 1)
light_seconds = light_second = ls = Unit(Distance, "ls", 299_792_458)
light_years = light_year = ly = Unit(Distance, "ly", 9_460_730_472_580_800)
astronomical_units = astronomical_unit = au = Unit(Distance, "au", 149_597_870_700)
parsecs = parsec = pc = Unit(Distance, "pc", 3.085_677_581_491_367_3e16)

inches = inch = in_ = Unit(Distance, "in", 0.0254)
feet = foot = ft = Unit(Distance, "ft", 0.3048)
yards = yard = yd = Unit(Distance, "yd", 0.9144)
miles = mile = mi = Unit(Distance, "mi", 1609.344)
nautical_miles = nautical_mile = nmi = Unit(Distance, "nmi", 1852)
fathoms = fathom = Unit(Distance, "fathom", 1.8288)
mils = mil = Unit(Distance, "mil", 0.0000254)

nanometers = nanometer = nm = nano(meter)
micrometers = micrometer = μm = micro(meter)
millimeters = millimeter = mm = milli(meter)
centimeters = centimeter = cm = centi(meter)
decimeters = decimeter = dm = deci(meter)
kilometers = kilometer = km = kilo(meter)
