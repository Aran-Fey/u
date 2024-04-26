from typing import *


class U[P: tuple, N: tuple]: ...


def mul[*P1, *N1, *P2, *N2](
    u1: U[tuple[*P1], tuple[*N1]],
    u2: U[tuple[*P2], tuple[*N2]],
) -> U[tuple[*P1, *P2], tuple[*N1, *N2]]: ...


def div[*M1, *M2](u1: U[*M1], u2: U[*M2]) -> U[*M1, *M2]: ...


i = U[int]()
s = U[str]()

reveal_type(mul(i, i))


t: tuple[str, int, float, int] = ...


@overload
def remove[*Is, R](tup: tuple[R, *Is], typ: type[R]) -> tuple[*Is]: ...


@overload
def remove[I, *Is, R, *Os](
    tup: tuple[I, *Is],
    typ: type[R],
    _r: Callable[[tuple[*Is], type[R]], tuple[*Os]] = remove,
) -> tuple[I, *Os]: ...


def remove(tup: tuple, typ: type) -> tuple: ...  # type: ignore


reveal_type(remove(t, str))  # tuple[int, float, int]
reveal_type(remove(t, float))  # tuple[str, int, int]
