from ..prefixes import SI_PREFIXES, milli
from ..quantity import Quantity
from ..capital_quantities import QUANTITY
from ..unit import Unit


# fmt: off
__all__ = [
    "DURATION",
    "Duration",
    "seconds", "second", "sec", "s",
    "minutes", "minute", "min",
    "hours", "hour", "h",
    "days", "day", "d",
    "weeks", "week", "wk", "w",
    "years", "year", "yr", "y",
    "decades", "decade", "dec",
    "centuries", "century", "cent", "c",
    "millenia", "millenium", "mil", "ka", "ky",
]
# fmt: on


class DURATION(QUANTITY):
    pass


Duration = Quantity[DURATION]
Duration.prefixes = SI_PREFIXES[: SI_PREFIXES.index(milli) + 1]

SYSTEMS = {"metric", "imperial", "nautical"}

seconds = second = sec = s = Unit(Duration, "s", 1, systems=SYSTEMS)
minutes = minute = min = Unit(Duration, "min", 60, systems=SYSTEMS)
hours = hour = h = Unit(Duration, "h", 3_600, systems=SYSTEMS)
days = day = d = Unit(Duration, "d", 86_400, systems=SYSTEMS)
weeks = week = wk = w = Unit(Duration, "wk", 604_800, systems=SYSTEMS)
years = year = yr = y = Unit(Duration, "yr", 31_536_000, systems=SYSTEMS)
decades = decade = dec = Unit(Duration, "dec", 315_360_000, systems=SYSTEMS)
centuries = century = cent = c = Unit(Duration, "cent", 3_153_600_000, systems=SYSTEMS)
millenia = millenium = mil = ka = ky = Unit(Duration, "mil", 31_536_000_000, systems=SYSTEMS)
