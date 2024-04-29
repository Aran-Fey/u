from ..quantity_and_unit import Quantity, Unit


__all__ = ["Pixels", "pixels", "pixel", "px"]


class Pixels(Quantity):
    pass


pixels = pixel = px = Unit[Pixels]("px", 1)
