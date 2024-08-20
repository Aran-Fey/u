from __future__ import annotations

import collections
import math
import re
import types
import typing as t

import u

from ._utils import UNION_TYPES, ExponentDict, str_exponent
from .quantity_caps import QUANTITY, DIV, MUL, _MUL


__all__ = ["Quantity", "NullableQuantity"]


FrozenExponents = frozenset[tuple[type[QUANTITY], int]]

Q_co = t.TypeVar("Q_co", bound=QUANTITY, covariant=True)
Q2 = t.TypeVar("Q2", bound=QUANTITY)


NUMBER_WITH_UNIT_REGEX = re.compile(r"([+-]?[0-9._]+)(.*)")


QUANTITY_ALIASES_BY_EXPONENTS = dict[FrozenExponents, "QuantityAlias"]()


class QuantityAlias(types.GenericAlias):
    exponents: ExponentDict
    units: t.Sequence[u.Unit]

    def __new__(cls, typ, subtype, exponents: ExponentDict):
        self = super().__new__(cls, typ, subtype)

        self.exponents = exponents
        self.units = []

        return self

    # GenericAlias is stupid and redirects all attribute access to the __origin__ class. Since we
    # want to implement an `exponents` property, we have to fix that idiotic behavior.
    def __getattribute__(self, name: str):
        if name in __class__.__annotations__:
            return vars(self)[name]

        if name in vars(__class__):
            return vars(__class__)[name].__get__(self)

        return super().__getattribute__(name)

    @property
    def base_unit(self) -> u.Unit:
        if self.units:
            return next(unit for unit in self.units if unit.multiplier == 1)

        unit = u.one
        for quantity, exponent in self.exponents.items():
            unit *= Quantity[quantity].base_unit ** exponent

        return unit

    def parse(self, *args, **kwargs):
        return Quantity.parse.__func__(self, *args, **kwargs)  # type: ignore

    def __call__(self, value: float, unit: u.Unit[Q_co] | None = None):
        if unit is None:
            assert value == 0
            unit = self.base_unit

        return super().__call__(value, unit)  # type: ignore (wtf?)

    def __hash__(self) -> int:
        return hash(self.exponents)

    def __eq__(self, other: object):
        if not isinstance(other, __class__):
            return NotImplemented

        return self.exponents == other.exponents

    def __repr__(self) -> str:
        exponents = self.exponents

        if not exponents:
            return "Quantity[ONE]"

        exponents = " ".join(
            f"{quantity.__name__}{str_exponent(exponents[quantity])}"
            for quantity in sorted(exponents, key=lambda q: q.__name__)
        )

        return f"Quantity[{exponents}]"


def get_exponents(quantity_caps: type[QUANTITY]) -> ExponentDict:
    exponents = collections.defaultdict(int)

    _add_exponents(quantity_caps, exponents)

    return ExponentDict(exponents)


def _add_exponents(quantity, exponents: collections.defaultdict[t.Type[QUANTITY], int]) -> None:
    # `quantity` can be:
    #
    # 1. A parameterized MUL or DIV
    # 2. A subclass of `QUANTITY`
    # 3. A Union
    if isinstance(quantity, type):
        if quantity.__name__ != "ONE":
            exponents[quantity] += 1

        return

    origin = t.get_origin(quantity)
    args = t.get_args(quantity)

    if any(isinstance(arg, t.TypeVar) for arg in args):
        raise NotFullyParameterized

    if origin in UNION_TYPES:
        # If it's a Union, then the subtypes must all be equivalent. So we simply pick one and
        # recurse.
        quantity = args[0]
        _add_exponents(quantity, exponents)
    elif origin is _MUL:
        _add_exponents(args[0], exponents)
        _add_exponents(args[1], exponents)
    else:
        _add_exponents(args[0], exponents)

        exps = collections.defaultdict(int)
        _add_exponents(args[1], exps)

        for quant, exp in exps.items():
            exponents[quant] -= exp


class NotFullyParameterized(Exception):
    pass


class QuantityMeta(type(t.Generic)):
    @property
    def exponents(cls) -> ExponentDict:
        raise TypeError(f"Unparameterized {cls} has no exponents")

    @property
    def units(cls) -> t.Sequence[u.Unit]:
        raise TypeError(f"Unparameterized {cls} has no units")

    @property
    def base_unit(cls) -> u.Unit:
        raise TypeError(f"Unparameterized {cls} has no units")


class Quantity(t.Generic[Q_co], metaclass=QuantityMeta):
    @classmethod  # This is only here to shut up the type checker
    def __class_getitem(cls, quantity_caps) -> QuantityAlias:
        # Make sure that all equivalent quantities return the same QuantityAlias
        try:
            if isinstance(quantity_caps, t.TypeVar):
                raise NotFullyParameterized

            exponents = get_exponents(quantity_caps)
        except NotFullyParameterized:
            return super().__class_getitem__(quantity_caps)  # type: ignore (wtf?)

        frozen_exponents = frozenset(exponents.items())

        try:
            return QUANTITY_ALIASES_BY_EXPONENTS[frozen_exponents]
        except KeyError:
            pass

        alias = QuantityAlias(cls, quantity_caps, exponents)

        QUANTITY_ALIASES_BY_EXPONENTS[frozen_exponents] = alias
        return alias

    if not t.TYPE_CHECKING:
        __class_getitem__ = __class_getitem

    @t.overload
    def __init__(self, value: t.Literal[0]): ...

    @t.overload
    def __init__(self, value: float, unit: u.Unit[Q_co]): ...

    def __init__(self, value: float, unit: u.Unit[Q_co] | None = None):
        # We actually can't implement the case with the optional unit here because `self` is a
        # `Quantity` instance and not a `QuantityAlias`. So `QuantityAlias.__call__` is responsible
        # for giving us a unit.
        if unit is None:
            raise TypeError("Creating an unparameterized `Quantity` requires a `unit`.")

        self._value = value
        self.unit = unit

    @property
    def quantity(self) -> type[Quantity[Q_co]]:
        return self.unit.quantity

    def to_number(self, unit: u.Unit[Q_co]) -> float:
        return self._value * (self.unit.multiplier / unit.multiplier)

    @classmethod
    def parse(cls, text: str, /) -> Quantity[Q_co]:
        match = NUMBER_WITH_UNIT_REGEX.match(text)
        if not match:
            raise ValueError(f"Cannot parse {text!r} as a Quantity")

        number_str, unit_str = match.groups()
        number = float(number_str)

        try:
            unit = u.Unit.parse(unit_str, cls)
        except ValueError:
            raise ValueError(f"Cannot parse {text!r} as a {cls!r}")

        return cls(number, unit)

    @classmethod
    def typecheck(cls, other: Quantity, /) -> t.TypeGuard[Quantity[Q_co]]:
        return cls.exponents == type(other).exponents

    def is_compatible_with(self, other: Quantity) -> t.TypeGuard[Quantity[Q_co]]:
        return self.unit.quantity.exponents == other.unit.quantity.exponents

    def __bool__(self) -> bool:
        return bool(self._value)

    def __float__(self) -> float:
        return float(self._value * self.unit.multiplier)

    def __neg__(self) -> Quantity[Q_co]:
        return Quantity(-self._value, self.unit)

    def __eq__(self, quantity: object, /) -> bool:
        if quantity == 0:
            num = self._value * self.unit.multiplier
            expected = 0
        elif not isinstance(quantity, __class__):
            return NotImplemented
        elif not self.is_compatible_with(quantity):
            return False
        else:
            num = self.to_number(quantity.unit)
            expected = quantity._value

        return math.isclose(num, expected)

    def __lt__(self, quantity: NullableQuantity[Q_co], /) -> bool:
        if quantity == 0:
            num = self._value * self.unit.multiplier
            expected = 0
        elif not isinstance(quantity, __class__):
            return NotImplemented
        elif not self.is_compatible_with(quantity):
            return False
        else:
            num = self.to_number(quantity.unit)
            expected = quantity._value

        return num < expected and not math.isclose(num, expected)

    def __le__(self, quantity: object, /) -> bool:
        if quantity == 0:
            num = self._value * self.unit.multiplier
            expected = 0
        elif not isinstance(quantity, __class__):
            return NotImplemented
        elif not self.is_compatible_with(quantity):
            return False
        else:
            num = self.to_number(quantity.unit)
            expected = quantity._value

        return num < expected or math.isclose(num, expected)

    def __gt__(self, quantity: object, /) -> bool:
        if quantity == 0:
            num = self._value * self.unit.multiplier
            expected = 0
        elif not isinstance(quantity, __class__):
            return NotImplemented
        elif not self.is_compatible_with(quantity):
            return False
        else:
            num = self.to_number(quantity.unit)
            expected = quantity._value

        return num > expected and not math.isclose(num, expected)

    def __ge__(self, quantity: object, /) -> bool:
        if quantity == 0:
            num = self._value * self.unit.multiplier
            expected = 0
        elif not isinstance(quantity, __class__):
            return NotImplemented
        elif not self.is_compatible_with(quantity):
            return False
        else:
            num = self.to_number(quantity.unit)
            expected = quantity._value

        return num > expected or math.isclose(num, expected)

    def __add__(self, quantity: NullableQuantity[Q_co], /) -> Quantity[Q_co]:
        if quantity == 0:
            return self

        return Quantity(
            self._value + quantity.to_number(self.unit),
            self.unit,
        )

    __radd__ = __add__

    def __sub__(self, quantity: NullableQuantity[Q_co], /) -> Quantity[Q_co]:
        if quantity == 0:
            return self

        return Quantity(
            self._value - quantity.to_number(self.unit),
            self.unit,
        )

    def __rsub__(self, zero: t.Literal[0], /) -> Quantity[Q_co]:
        assert zero == 0
        return Quantity(-self._value, self.unit)

    @t.overload
    def __mul__(self, number: float, /) -> Quantity[Q_co]: ...

    @t.overload
    def __mul__(self, quantity: Quantity[Q2], /) -> Quantity[MUL[Q_co, Q2]]: ...

    def __mul__(self, other: float | Quantity[Q2]) -> Quantity:
        if isinstance(other, Quantity):
            return Quantity(
                self._value * other._value,
                self.unit * other.unit,
            )
        else:
            return Quantity(self._value * other, self.unit)

    @t.overload
    def __truediv__(self, number: float, /) -> Quantity[Q_co]: ...

    @t.overload
    def __truediv__(self, quantity: Quantity[Q2], /) -> Quantity[DIV[Q_co, Q2]]: ...

    def __truediv__(self, other: float | Quantity[Q2]) -> Quantity:
        if isinstance(other, Quantity):
            return Quantity(
                self._value / other._value,
                self.unit / other.unit,
            )
        else:
            return Quantity(self._value / other, self.unit)

    @t.overload
    def __rtruediv__(self, number: float, /) -> Quantity[DIV[u.ONE, Q_co]]: ...

    @t.overload
    def __rtruediv__(self, quantity: Quantity[Q2], /) -> Quantity[DIV[Q2, Q_co]]: ...

    def __rtruediv__(self, other: t.Union[float, Quantity[Q2]]) -> Quantity[DIV]:
        if isinstance(other, Quantity):
            return Quantity(
                other._value / self._value,
                other.unit / self.unit,
            )
        else:
            return Quantity(
                other / self._value,
                u.one / self.unit,
            )

    def __repr__(self) -> str:
        return f"{self._value}{self.unit.symbol}"

    def __str__(self) -> str:
        value = self._value * self.unit.multiplier

        # Special case: If the value is 0, use the base unit
        if math.isclose(value, 0):
            base_unit = self.unit.quantity.base_unit
            return f"0 {base_unit.symbol}"

        exponents = self.unit.quantity.exponents

        # If this isn't a compound unit, keep it simple
        if len(exponents) == 1:
            exponent = next(iter(exponents.values()))

            unit = find_most_suitable_unit(value, self.quantity.units, exponent)
            value /= unit.multiplier

            quantity_caps: type[QUANTITY] = t.get_args(unit.quantity)[0]
            prefixes = quantity_caps.PREFIXES
        else:
            unit = self.quantity.base_unit
            exponent = 1

            prefixes = u.SI_PREFIXES

        prefix = find_most_suitable_prefix(value, prefixes, exponent)
        value /= prefix.multiplier

        if value.is_integer():
            value_str = str(int(value))
        else:
            value_str = format(value, ".1f")

        return f"{value_str} {prefix.symbol}{unit.symbol}"


NullableQuantity = t.Union[Quantity[Q2], t.Literal[0]]


def find_most_suitable_unit(value: float, units: t.Iterable[u.Unit], exponent: int) -> u.Unit:
    return _find_most_suitable_multiplier(value, units, exponent)


def find_most_suitable_prefix(
    value: float, prefixes: t.Iterable[u.Prefix], exponent: int
) -> u.Prefix:
    prefixes = list(prefixes)
    prefixes.append(u.prefixes.DUMMY_PREFIX)

    return _find_most_suitable_multiplier(value, prefixes, exponent)


def _find_most_suitable_multiplier(
    value: float, things: t.Iterable[u.Unit | u.Prefix], exponent: int
) -> t.Any:
    candidates = [thing for thing in things if thing.multiplier**exponent <= value]

    if candidates:
        return max(candidates, key=lambda thing: thing.multiplier)
    else:
        return min(things, key=lambda thing: thing.multiplier)
