import typing as t


__all__ = ["QUANTITY", "MUL", "DIV", "SQUARE"]


class QUANTITY:
    pass


Q = t.TypeVar("Q", bound=QUANTITY)
Q1 = t.TypeVar("Q1", bound=QUANTITY)
Q2 = t.TypeVar("Q2", bound=QUANTITY)


class _MUL(t.Generic[Q1, Q2], QUANTITY): ...


class DIV(t.Generic[Q1, Q2], QUANTITY): ...


MUL = _MUL[Q1, Q2] | _MUL[Q2, Q1]
SQUARE = _MUL[Q, Q]
