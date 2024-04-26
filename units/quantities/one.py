from ..quantity_and_unit import Quantity, Unit


__all__ = ["One", "one"]


class One(Quantity):
    """
    Represents the absence of a quantity. Used to create "inverted" quantities like `Frequency =
    Div[One, Duration]`.
    """


one = Unit[One]("1", 1)
