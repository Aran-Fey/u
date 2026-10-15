from __future__ import annotations

import collections.abc
import decimal
import functools
from operator import is_
import re
import sys
import types
import typing as t

import u
from .maths import FloatOrDecimal


C = t.TypeVar("C", bound=t.Callable)


if sys.version_info >= (3, 10):
    UNION_TYPES = (t.Union, types.UnionType)
else:
    UNION_TYPES = (t.Union,)


def is_union(obj: object) -> bool:
    return t.get_origin(obj) in UNION_TYPES


def cached(func: C) -> C:
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        try:
            return cache[args]
        except KeyError:
            pass

        result = cache[args] = func(*args)
        return result

    return wrapper  # type: ignore


LEADING_DURATION_FIELD_REGEX = re.compile(r"[0-9]+")
DURATION_FIELD_REGEX = re.compile(r"[0-5][0-9]")
FRACTION_REGEX = re.compile(r"(?:\.[0-9]+)?")


def parse_duration(text: str) -> u.Duration:
    """
    Parses a duration in the form "HH:MM:SS", "MM:SS" or "SS". The seconds can have a fractional
    part, like "1:30.5".

    The leading number can be arbitrarily large (like "90:00" for 90 minutes), but all following
    numbers must have exactly 2 digits and be at most 59.
    """
    fields = text.split(":")
    if len(fields) > 3:
        raise ValueError(f"Cannot parse {text!r} as a duration")

    # Only the seconds can have a fractional part
    fields[-1], dot, fraction = fields[-1].partition(".")
    fraction = dot + fraction

    leading_field, *other_fields = fields
    if (
        not LEADING_DURATION_FIELD_REGEX.fullmatch(leading_field)
        or not all(DURATION_FIELD_REGEX.fullmatch(field) for field in other_fields)
        or not FRACTION_REGEX.fullmatch(fraction)
    ):
        raise ValueError(f"Cannot parse {text!r} as a duration")

    # Decimal avoids rounding errors, e.g. 60 + 30.12345 isn't 90.12345 in floating point
    total = decimal.Decimal(0)
    for field in fields:
        total = total * 60 + int(field)

    total += decimal.Decimal("0" + fraction)

    if total == total.to_integral_value():
        return u.seconds(int(total))

    return u.seconds(float(total))


def format_duration(seconds: FloatOrDecimal, format_: str, number_format: str | None) -> str:
    """
    Formats a duration in the form "HH:MM:SS".
    """
    *_, hour_format, minute_format, second_format = ["", "", ""] + format_.split(":")

    # Splitting a float into minutes and seconds exposes its representation error: 90.12345 is
    # printed as "90.12345", but 90.12345 - 60 is printed as "30.123450000000005". Decimals don't
    # have that problem, and going through `repr` gives us the value the float is displayed as.
    if not isinstance(seconds, decimal.Decimal):
        seconds = decimal.Decimal(repr(seconds))

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(int(minutes), 60)

    # Get rid of trailing zeros, like in `1.500` or `30.0`
    if seconds == seconds.to_integral_value():
        seconds = int(seconds)
    else:
        seconds = seconds.normalize()

    show_hours = bool(hours or hour_format)
    show_minutes = bool(minutes or minute_format or show_hours)

    # Once a larger unit is displayed, smaller ones need 2 digits, regardless of the format. ("1:2:5"
    # would be unreadable.)
    seconds_str = format(seconds, number_format or "")
    integer_part, dot, fraction = seconds_str.partition(".")
    seconds_digits = 2 if show_minutes else len(second_format)
    parts = [integer_part.zfill(seconds_digits) + dot + fraction]

    if show_minutes:
        minutes_digits = 2 if show_hours else len(minute_format)
        parts.append(str(minutes).zfill(minutes_digits))

    if show_hours:
        parts.append(str(hours).zfill(len(hour_format)))

    return ":".join(reversed(parts))


SYMBOL_REGEX = re.compile(r"(^|[*/])([^*/]+?)([⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹]*)\s*(?=[*/]|$)")


EXPONENT_CHARS = "⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹"


def parse_symbol(symbol: str) -> t.Counter[str]:
    """
    Parses a symbol into a Counter of the symbols it consists of and their exponents.

    ```
    >>> parse_symbol('1/s²')
    Counter({'1': 1, 's': -2})
    >>> parse_symbol('kg*m/(s²*A)')
    Counter({'kg': 1, 'm': 1, 's': -2, 'A': -1})
    ```

    Parenthesized groups are expanded, unless they have a prefix: The prefix applies to the group as
    a whole, so something like "k(m²)" is treated as a single symbol.
    """
    if not symbol.strip():
        return collections.Counter()

    parser = _SymbolParser(symbol)
    result = parser.parse_product()

    if parser.pos != len(symbol):
        raise parser.error()

    return result


class _SymbolParser:
    """
    A recursive descent parser for unit symbols. The grammar is:

        product := factor (("*" | "/") factor)*
        factor  := (name | name? "(" product ")") exponent?

    A "/" only applies to the factor directly after it, so "m/s*A" is "m*A/s".
    """

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def error(self) -> ValueError:
        return ValueError(f"Invalid unit symbol: {self.text!r}")

    def _skip_whitespace(self) -> None:
        while self.text[self.pos : self.pos + 1].isspace():
            self.pos += 1

    def _next_char(self) -> str:
        return self.text[self.pos : self.pos + 1]

    def parse_product(self) -> t.Counter[str]:
        result = collections.Counter[str]()
        sign = 1

        while True:
            for symbol, exponent in self.parse_factor().items():
                result[symbol] += sign * exponent

            self._skip_whitespace()

            char = self._next_char()
            if char == "*":
                sign = 1
            elif char == "/":
                sign = -1
            else:
                return result

            self.pos += 1

    def parse_factor(self) -> t.Counter[str]:
        self._skip_whitespace()

        start = self.pos
        while self._next_char() and self._next_char() not in "*/()" + EXPONENT_CHARS:
            self.pos += 1
        name = self.text[start : self.pos].strip()

        if self._next_char() == "(":
            self.pos += 1
            group_start = self.pos
            group = self.parse_product()

            if self._next_char() != ")":
                raise self.error()

            group_text = self.text[group_start : self.pos].strip()
            self.pos += 1

            if name:
                factors = collections.Counter({f"{name}({group_text})": 1})
            else:
                factors = group
        elif name:
            factors = collections.Counter({name: 1})
        else:
            raise self.error()

        exponent_start = self.pos
        while self._next_char() and self._next_char() in EXPONENT_CHARS:
            self.pos += 1

        try:
            exponent = parse_exponent(self.text[exponent_start : self.pos])
        except ValueError:
            raise self.error() from None

        return collections.Counter(
            {symbol: power * exponent for symbol, power in factors.items()}
        )


POW_TO_NUM = str.maketrans("⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹", "-+0123456789")
NUM_TO_POW = {value: key for key, value in POW_TO_NUM.items()}


def parse_exponent(exp: str) -> int:
    if not exp:
        return 1

    return int(exp.translate(POW_TO_NUM))


def str_exponent(exp: int) -> str:
    if exp == 1:
        return ""

    return str(exp).translate(NUM_TO_POW)


def join_symbols(symbol1: str, symbol2: str, operator: t.Literal["*", "/"]) -> str:
    powers = parse_symbol(symbol1)
    sign = -1 if operator == "/" else 1

    for symbol, exponent in parse_symbol(symbol2).items():
        powers[symbol] += sign * exponent

    return format_symbol(powers)


def format_symbol(powers: t.Mapping[str, int]) -> str:
    """
    Creates a symbol like "kg*m/(A*s²)" from a mapping of symbols to exponents.

    The factors are sorted by their symbols (numerator first), so the result doesn't depend on the
    order in which the units were multiplied. (Units with conventional symbols that don't follow
    this order, like "N*m", can be registered explicitly.)
    """
    powers = {
        symbol: powers[symbol]
        for symbol in sorted(powers)
        if powers[symbol] != 0 and symbol != "1"
    }

    numerator = [symbol + str_exponent(exp) for symbol, exp in powers.items() if exp > 0]
    denominator = [symbol + str_exponent(-exp) for symbol, exp in powers.items() if exp < 0]

    # "s⁻¹" reads better than "1/s"
    if not numerator:
        return "*".join(symbol + str_exponent(exp) for symbol, exp in powers.items()) or "1"

    result = "*".join(numerator)

    if len(denominator) == 1:
        result += "/" + denominator[0]
    elif denominator:
        result += "/(" + "*".join(denominator) + ")"

    return result


class ExponentDict(collections.abc.Mapping[type["u.QUANTITY"], int]):
    def __init__(self, exponents: t.Mapping[type[u.QUANTITY], int]):
        # We're converting to a dict for 2 reasons:
        # 1. Makes implementing `__repr__` trivial
        # 2. If it's a defaultdict, we don't have to worry about accidentally mutating it
        self._exponents = dict(exponents)

    def __getitem__(self, quantity: type[u.QUANTITY]) -> int:
        return self._exponents.get(quantity, 0)

    def __iter__(self) -> t.Iterator[type[u.QUANTITY]]:
        return iter(self._exponents)

    def __len__(self) -> int:
        return len(self._exponents)

    def __hash__(self) -> int:
        return hash(tuple(self.items()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, __class__):
            return NotImplemented

        return self._exponents == other._exponents

    def __repr__(self) -> str:
        return repr(self._exponents)
