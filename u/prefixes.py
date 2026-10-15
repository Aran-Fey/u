from __future__ import annotations

import decimal
import typing as t

import u

from .maths import multiply
from ._utils import SYMBOL_REGEX, cached, parse_exponent

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
    def __init__(
        self,
        symbol: str,
        multiplier: decimal.Decimal | int,
        aliases: t.Iterable[str] = (),
    ):
        """
        `aliases` are alternative spellings of the `symbol` that are accepted when parsing, but
        never used for output.
        """
        self.symbol = symbol
        self.multiplier = decimal.Decimal(multiplier)

        global max_prefix_length

        for sym in (symbol, *aliases):
            prefix_by_symbol[sym] = self
            max_prefix_length = max(max_prefix_length, len(sym))

    @classmethod
    def from_symbol(cls, symbol: str) -> Prefix:
        try:
            return prefix_by_symbol[symbol]
        except KeyError:
            raise ValueError(f"The symbol {symbol!r} doesn't correspond to any Prefix")

    @staticmethod
    def can_attach_to(unit: u.Unit) -> bool:
        """
        Returns whether prefixes can be attached to one of the unit's factors, like "km/s". If not,
        prefixing the unit wraps its symbol in parentheses instead, like "k(m²)".
        """
        return _find_attachment_point(unit.symbol) is not None

    @cached
    def __call__(self, unit: u.Unit[Q]) -> u.Unit[Q]:
        return u.unit.lookup_unit(
            unit.quantity,
            _prefixed_symbol(self.symbol, unit.symbol),
            multiply(self.multiplier, unit.multiplier, decimal.Decimal),
            unit.systems,
        )

    def __repr__(self) -> str:
        return f"<Prefix {self.symbol}>"


def _prefixed_symbol(prefix_symbol: str, unit_symbol: str) -> str:
    """
    Applies a prefix to a unit symbol, like "k" + "m/s" -> "km/s". If the prefix can't be attached to
    any factor of the symbol, the symbol is wrapped in parentheses: "k" + "m²" -> "k(m²)".
    """
    index = _find_attachment_point(unit_symbol)
    if index is None:
        return f"{prefix_symbol}({unit_symbol})"

    return unit_symbol[:index] + prefix_symbol + unit_symbol[index:]


def _find_attachment_point(symbol: str) -> int | None:
    """
    Returns the index in the `symbol` where a prefix can be inserted, or `None` if there is no such
    place.

    Since a prefix only scales the factor it's attached to, a factor is only eligible if its
    exponent is 1 ("km²" is 10⁶ m², not 10³ m²) and it doesn't already have a prefix. (Only units
    without a prefix are registered by their symbol.) Only the numerator is considered, and nothing
    inside parentheses. The first eligible factor is used, so "m/s" becomes "km/s" and "m²*s"
    becomes "m²*ks".
    """
    # Find the end of the numerator, i.e. the first "/" that isn't inside parentheses
    depth = 0
    numerator_end = len(symbol)
    for index, char in enumerate(symbol):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "/" and depth == 0:
            numerator_end = index
            break

    for match in SYMBOL_REGEX.finditer(symbol[:numerator_end]):
        operator, factor, exponent = match.groups()
        start = match.start(2)

        if (
            operator != "/"
            and parse_exponent(exponent) == 1
            and factor != "1"
            and factor in u.unit.units_by_symbol
            and symbol.count("(", 0, start) == symbol.count(")", 0, start)
        ):
            return start

    return None


DUMMY_PREFIX = Prefix("", 1)


quecto = Prefix("q", decimal.Decimal("1e-30"))
ronto = Prefix("r", decimal.Decimal("1e-27"))
yocto = Prefix("y", decimal.Decimal("1e-24"))
zepto = Prefix("z", decimal.Decimal("1e-21"))
atto = Prefix("a", decimal.Decimal("1e-18"))
femto = Prefix("f", decimal.Decimal("1e-15"))
pico = Prefix("p", decimal.Decimal("1e-12"))
nano = Prefix("n", decimal.Decimal("1e-9"))
# The official symbol is MICRO SIGN, but GREEK SMALL LETTER MU looks identical and "u" is a
# common ASCII replacement
micro = Prefix("\N{MICRO SIGN}", decimal.Decimal("1e-6"), aliases=["\N{GREEK SMALL LETTER MU}", "u"])
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
