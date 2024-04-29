from ..quantity_and_unit import Quantity, Unit


__all__ = ["One", "ones", "one"]


class One(Quantity):
    """
    Represents the absence of a quantity. Used to create "inverted" quantities like `Frequency =
    Div[One, Duration]`.
    """


ones = one = Unit[One]("1", 1)
