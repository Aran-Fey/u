from __future__ import annotations

import typing as t
import weakref

import u

from ._utils import cached, join_symbols, parse_symbol
from .quantity import Quantity
from .quantity_caps import QUANTITY, DIV, MUL, Q2


__all__ = ["Unit"]


Q_co = t.TypeVar("Q_co", bound=QUANTITY, covariant=True)


units_by_symbol: t.MutableMapping[str, Unit] = weakref.WeakValueDictionary()


class Unit(t.Generic[Q_co]):
    """
    Represents a unit of measurement for a certain `Quantity`.

    To create your own unit, simply create an instance of this class:

    ```
    seconds = Unit(Duration, "s", 1)
    minutes = Unit(Duration, "min", 60)
    coulombs = Unit(ElectricCharge, "C", seconds.multiplier * amperes.multiplier)
    ```
    """

    def __init__(self, quantity: t.Type[Quantity[Q_co]], symbol: str, multiplier: float):
        self.quantity = quantity
        self._symbol = symbol
        self.multiplier = multiplier

        units_by_symbol[symbol] = self

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        del units_by_symbol[self._symbol]

        self._symbol = symbol
        units_by_symbol[symbol] = self

    @staticmethod
    def _from_symbol(symbol: str) -> Unit:
        try:
            return units_by_symbol[symbol]
        except KeyError:
            raise ValueError(f"The symbol {symbol!r} does not correspond to a known Unit")

    @classmethod
    def parse(cls, symbol: str, /, quantity: t.Type[Quantity[Q2]] = Quantity) -> Unit[Q2]:
        exponents = parse_symbol(symbol)

        unit: Unit

        # Try to start with a positive exponent
        try:
            sym = next(sym for sym, exponent in exponents.items() if exponent > 0)
        except StopIteration:
            unit = u.one
        else:
            unit = Unit._from_symbol(sym) ** exponents.pop(sym)

        for sym, exponent in exponents.items():
            if exponent > 0:
                unit *= Unit._from_symbol(sym) ** exponent
            elif exponent < 0:
                unit /= Unit._from_symbol(sym) ** -exponent

        if unit.is_compatible_with(quantity):
            return unit

        raise ValueError(f"{symbol!r} is not a unit of {cls}")

    @t.overload
    def is_compatible_with(self, unit: Unit, /) -> t.TypeGuard[Unit[Q_co]]: ...

    @t.overload
    def is_compatible_with(self, quantity: t.Type[Quantity[Q2]], /) -> t.TypeGuard[Unit[Q2]]: ...

    def is_compatible_with(
        self,
        other: t.Union[Unit[Q2], t.Type[Quantity[Q2]]],
        /,
    ) -> t.TypeGuard[Unit[Q2]]:
        if isinstance(other, Unit):
            return self.quantity.exponents == other.quantity.exponents
        else:
            return self.quantity.exponents == other.exponents

    @t.overload
    def __pow__(self, exponent: t.Literal[1]) -> t.Self: ...

    @t.overload
    def __pow__(self, exponent: t.Literal[2]) -> Unit[MUL[Q_co, Q_co]]: ...

    @t.overload
    def __pow__(self, exponent: t.Literal[3]) -> Unit[MUL[MUL[Q_co, Q_co], Q_co]]: ...

    @t.overload
    def __pow__(self, exponent: int) -> Unit: ...

    def __pow__(self, exponent: int) -> Unit:
        result = self

        for _ in range(exponent - 1):
            result *= self

        return result

    @cached
    def __mul__(self, other: Unit[Q2]) -> Unit[MUL[Q_co, Q2]]:
        return Unit(
            join_quantities(self.quantity, other.quantity, MUL),
            join_symbols(self.symbol, other.symbol, "*"),
            self.multiplier * other.multiplier,
        )

    @cached
    def __truediv__(self, other: Unit[Q2]) -> Unit[DIV[Q_co, Q2]]:
        return Unit(
            join_quantities(self.quantity, other.quantity, DIV),
            join_symbols(self.symbol, other.symbol, "/"),
            self.multiplier / other.multiplier,
        )

    def __rmul__(self, value: float) -> Quantity[Q_co]:
        return Quantity(value, self)

    def __call__(self, value: float) -> Quantity[Q_co]:
        return Quantity(value, self)

    def __repr__(self) -> str:
        return f"Unit({self.quantity!r}, {self.symbol!r}, {self.multiplier!r})"

    def __str__(self) -> str:
        return self.symbol


def join_quantities(q1, q2, joiner) -> t.Type[Quantity]:
    [a] = t.get_args(q1)
    [b] = t.get_args(q2)

    return Quantity[joiner[a, b]]
