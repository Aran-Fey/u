from __future__ import annotations

import typing as t

import u

from .prefixes import SI_PREFIXES


__all__ = ["QUANTITY", "MUL", "DIV", "SQUARE"]


class QUANTITY:
    PREFIXES: t.Sequence[u.Prefix] = SI_PREFIXES


Q = t.TypeVar("Q", bound=QUANTITY)
Q1 = t.TypeVar("Q1", bound=QUANTITY, covariant=True)
Q2 = t.TypeVar("Q2", bound=QUANTITY, covariant=True)


class _MUL(t.Generic[Q1, Q2], QUANTITY): ...


class DIV(t.Generic[Q1, Q2], QUANTITY): ...


MUL = _MUL[Q1, Q2] | _MUL[Q2, Q1]
SQUARE = _MUL[Q, Q]
