from __future__ import annotations

import math
from typing import Generic, TypeVar, cast, overload
from typing_extensions import Self

import sympy


__all__ = ["Quantity", "Mul", "Div", "Unit"]


class Quantity:
    """
    Represents a measurable quantity, like mass or acceleration.

    FIXME: Correct docstring

    In order to be able to represent compound quantities (like speed, which is distance divided by
    time), this is a generic class that accepts an arbitrary number of type arguments. Each type
    argument represents either a multiplication or, through the use of `Inv`, a division.

    Examples:

    ```
    Distance = Quantity[DISTANCE]  # just distance
    Area = Quantity[DISTANCE, DISTANCE]  # distance squared
    Speed = Quantity[DISTANCE, Inv[DURATION]]  # distance divided by time
    ```

    Unfortunately this isn't ideal: Because type checkers care about the order of the arguments,
    they treat `Quantity[A, B]` as different from `Quantity[B, A]`.
    """

    def __init__(self, value: float, unit: Unit[Self]):
        self._value = value
        self._unit = unit

    def to_number(self, unit: Unit[Self]) -> float:
        # We can convert between "singular" units (for example minutes to seconds) by using their
        # `_to_base_unit` and `_from_base_unit` formulas.
        formula = unit._from_base_unit.subs(BASE_UNIT, self._unit._to_base_unit)

        result = formula.subs(SELF_UNIT, self._value)
        return float(result.evalf())  # type: ignore

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, __class__):
            return NotImplemented

        num = self.to_number(value._unit)  # type: ignore
        return math.isclose(num, self._value)

    def __repr__(self) -> str:
        return f"{self._value}{self._unit.symbol}"


Q = TypeVar("Q", bound=Quantity)
Q2 = TypeVar("Q2", bound=Quantity)


class Mul(Generic[Q, Q2], Quantity): ...


class Div(Generic[Q, Q2], Quantity): ...


BASE_UNIT = sympy.symbols("BASE_UNIT")
SELF_UNIT = sympy.symbols("SELF_UNIT")


class Unit(Generic[Q]):
    """
    Represents a unit of measurement for a certain `Quantity`.

    To create your own unit, simply create an instance of this class. Make sure to pass the
    corresponding `Quantity` as a type argument as seen here:

    ```
    seconds = Unit[Duration]("s", 1)
    minutes = Unit[Duration]("min", 60)
    ```
    """

    @overload
    def __init__(self, symbol: str, multiplier: float): ...

    @overload
    def __init__(self, symbol: str, *, offset: float): ...

    @overload
    def __init__(self, symbol: str, *, formula: sympy.Expr): ...

    @overload
    def __init__(self, symbol: str, *, from_base_unit: sympy.Expr, to_base_unit: sympy.Expr): ...

    def __init__(
        self,
        symbol: str,
        multiplier: float | None = None,
        offset: float | None = None,
        formula: sympy.Expr | None = None,
        from_base_unit: sympy.Expr | None = None,
        to_base_unit: sympy.Expr | None = None,
    ):
        self.symbol = symbol

        # normalize: Callable[[float], float]
        # if multiplier is not None:
        #     normalize = functools.partial(operator.mul, multiplier)
        # else:
        #     normalize = functools.partial(operator.add, offset)

        # self._normalize = normalize

        if multiplier is not None:
            to_base_unit = SELF_UNIT * multiplier
            from_base_unit = BASE_UNIT / multiplier
        elif offset is not None:
            to_base_unit = SELF_UNIT + offset
            from_base_unit = BASE_UNIT - offset
        elif formula is not None:
            from_base_unit = formula
            to_base_unit = sympy.solve(sympy.Eq(SELF_UNIT, formula), BASE_UNIT)[0]

        self._to_base_unit = cast(sympy.Expr, to_base_unit)
        self._from_base_unit = cast(sympy.Expr, from_base_unit)

    def __mul__(self, other: Unit[Q2]) -> Unit[Mul[Q, Q2]]:
        return Unit(
            f"{self.symbol}*{other.symbol}",
            from_base_unit=self._from_base_unit * other._from_base_unit,  # type: ignore
            to_base_unit=self._to_base_unit / other._to_base_unit,  # type: ignore
        )

    def __truediv__(self, other: Unit[Q2]) -> Unit[Div[Q, Q2]]:
        return Unit(
            f"{self.symbol}/{other.symbol}",
            from_base_unit=self._from_base_unit * other._from_base_unit,  # type: ignore
            to_base_unit=self._to_base_unit / other._to_base_unit,  # type: ignore
        )

    def __call__(self, value: float) -> Q:
        return Quantity(value, self)  # type: ignore
