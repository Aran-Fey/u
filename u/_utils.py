import functools
from typing import Callable, TypeVar


C = TypeVar("C", bound=Callable)


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
