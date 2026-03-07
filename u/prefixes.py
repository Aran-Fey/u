from __future__ import annotations

import decimal
import typing as t

import u

from .maths import multiply
from ._utils import cached

__all__ = [
    "Prefix",
    "STANDARD_SI_PREFIXES",
    "SI_PREFIXES",
    "BINARY_PREFIXES",
    "atto",
    "femto",
    "pico",
    "nano",
    "micro",
    "milli",
    "centi",
    "deci",
    "deka",
    "hecto",
    "kilo",
    "mega",
    "giga",
    "tera",
    "peta",
    "exa",
    "zetta",
    "yotta",
    "kibi",
    "mebi",
    "gibi",
    "tebi",
    "pebi",
    "exbi",
    "zebi",
    "yobi",
]


Q = t.TypeVar("Q", bound="u.QUANTITY")


prefix_by_symbol = dict[str, "Prefix"]()
max_prefix_length = 0


class Prefix:
    def __init__(self, symbol: str, multiplier: decimal.Decimal | int):
        self.symbol = symbol
        self.multiplier = decimal.Decimal(multiplier)

        prefix_by_symbol[symbol] = self

        global max_prefix_length
        max_prefix_length = max(max_prefix_length, len(symbol))

    @classmethod
    def from_symbol(cls, symbol: str) -> Prefix:
        try:
            return prefix_by_symbol[symbol]
        except KeyError:
            raise ValueError(f"The symbol {symbol!r} doesn't correspond to any Prefix")

    @cached
    def __call__(self, unit: u.Unit[Q]) -> u.Unit[Q]:
        if isinstance(unit, u.unit.UnregisteredUnit):
            raise ValueError("Prefixes cannot be applied to compound units") from None

        return u.unit.lookup_unit(
            unit.quantity,
            self.symbol + unit.symbol,
            multiply(self.multiplier, unit.multiplier, decimal.Decimal),
            unit.systems,
        )

    def __repr__(self) -> str:
        return f"<Prefix {self.symbol}>"


DUMMY_PREFIX = Prefix("", 1)


quecto = Prefix("q", decimal.Decimal("1e-30"))
ronto = Prefix("r", decimal.Decimal("1e-27"))
yocto = Prefix("y", decimal.Decimal("1e-24"))
zepto = Prefix("z", decimal.Decimal("1e-21"))
atto = Prefix("a", decimal.Decimal("1e-18"))
femto = Prefix("f", decimal.Decimal("1e-15"))
pico = Prefix("p", decimal.Decimal("1e-12"))
nano = Prefix("n", decimal.Decimal("1e-9"))
micro = Prefix("µ", decimal.Decimal("1e-6"))
milli = Prefix("m", decimal.Decimal("1e-3"))
centi = Prefix("c", decimal.Decimal("1e-2"))
deci = Prefix("d", decimal.Decimal("1e-1"))
deka = Prefix("da", 10**1)
hecto = Prefix("h", 10**2)
kilo = Prefix("k", 10**3)
mega = Prefix("M", 10**6)
giga = Prefix("G", 10**9)
tera = Prefix("T", 10**12)
peta = Prefix("P", 10**15)
exa = Prefix("E", 10**18)
zetta = Prefix("Z", 10**21)
yotta = Prefix("Y", 10**24)
ronna = Prefix("R", 10**27)
quetta = Prefix("Q", 10**30)


STANDARD_SI_PREFIXES = (
    quecto,
    ronto,
    yocto,
    zepto,
    atto,
    femto,
    pico,
    nano,
    micro,
    milli,
    kilo,
    mega,
    giga,
    tera,
    peta,
    exa,
    zetta,
    yotta,
    ronna,
    quetta,
)

SI_PREFIXES = (
    quecto,
    ronto,
    yocto,
    zepto,
    atto,
    femto,
    pico,
    nano,
    micro,
    milli,
    centi,
    deci,
    deka,
    hecto,
    kilo,
    mega,
    giga,
    tera,
    peta,
    exa,
    zetta,
    yotta,
    ronna,
    quetta,
)

kibi = Prefix("ki", 2**10)
mebi = Prefix("Mi", 2**20)
gibi = Prefix("Gi", 2**30)
tebi = Prefix("Ti", 2**40)
pebi = Prefix("Pi", 2**50)
exbi = Prefix("Ei", 2**60)
zebi = Prefix("Zi", 2**70)
yobi = Prefix("Yi", 2**80)

BINARY_PREFIXES = (kibi, mebi, gibi, tebi, pebi, exbi, zebi, yobi)
