from ..quantity_and_unit import Quantity, Unit


__all__ = [
    "Duration",
    "seconds",
    "sec",
    "s",
    "minutes",
    "min",
    "hours",
    "h",
    "days",
    "d",
    "weeks",
    "wk",
    "w",
    "years",
    "yr",
    "y",
    "decades",
    "dec",
    "centuries",
    "cent",
    "c",
    "millenia",
    "mil",
    "ka",
    "ky",
]


class Duration(Quantity):
    pass


seconds = sec = s = Unit[Duration]("s", 1)
minutes = min = Unit[Duration]("min", 60)
hours = h = Unit[Duration]("h", 3_600)
days = d = Unit[Duration]("d", 86_400)
weeks = wk = w = Unit[Duration]("wk", 86_400)
years = yr = y = Unit[Duration]("yr", 31_557_600)
decades = dec = Unit[Duration]("dec", 315_576_000)
centuries = cent = c = Unit[Duration]("cent", 3_155_760_000)
millenia = mil = ka = ky = Unit[Duration]("mil", 31_557_600_000)
