import typing as t

from .prefixes import SI_PREFIXES


__all__ = ["QUANTITY", "MUL", "DIV", "SQUARE"]


class QUANTITY:
    PREFIXES = SI_PREFIXES


Q = t.TypeVar("Q", bound=QUANTITY)
Q1 = t.TypeVar("Q1", bound=QUANTITY)
Q2 = t.TypeVar("Q2", bound=QUANTITY)


class _MUL(t.Generic[Q1, Q2], QUANTITY): ...


class DIV(t.Generic[Q1, Q2], QUANTITY): ...


MUL = t.Union[_MUL[Q1, Q2], _MUL[Q2, Q1]]
SQUARE = _MUL[Q, Q]
