"""
Floats and Decimals refuse to cooperate, so any math involving mixed types will throw an error. This
module can be used to safely perform math without worrying about the types of the operands.
"""

import decimal
import operator
import typing as t


FloatOrDecimal = float | decimal.Decimal
TypePreference = type[float] | type[decimal.Decimal] | None


def add(
    lhs: FloatOrDecimal, rhs: FloatOrDecimal, type_preference: TypePreference = None
) -> FloatOrDecimal:
    return apply_operator(operator.add, lhs, rhs, type_preference)


def subtract(
    lhs: FloatOrDecimal, rhs: FloatOrDecimal, type_preference: TypePreference = None
) -> FloatOrDecimal:
    return apply_operator(operator.sub, lhs, rhs, type_preference)


def multiply(
    lhs: FloatOrDecimal, rhs: FloatOrDecimal, type_preference: TypePreference = None
) -> FloatOrDecimal:
    return apply_operator(operator.mul, lhs, rhs, type_preference)


def divide(
    lhs: FloatOrDecimal, rhs: FloatOrDecimal, type_preference: TypePreference = None
) -> FloatOrDecimal:
    return apply_operator(operator.truediv, lhs, rhs, type_preference)


def apply_operator(
    operator: t.Callable[[float, float], float],
    lhs: FloatOrDecimal,
    rhs: FloatOrDecimal,
    type_preference: TypePreference = None,
) -> FloatOrDecimal:
    try:
        return operator(lhs, rhs)  # type: ignore
    except TypeError:
        pass

    if type_preference is None:
        type_preference = type(lhs)

    lhs = type_preference(lhs)
    rhs = type_preference(rhs)

    return operator(lhs, rhs)  # type: ignore
