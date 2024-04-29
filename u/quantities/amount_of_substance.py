from ..quantity_and_unit import Quantity, Unit


# fmt: off
__all__ = [
    "AmountOfSubstance",
    "moles", "mole", "mol",
]
# fmt: on


class AmountOfSubstance(Quantity):
    pass


moles = mole = mol = Unit[AmountOfSubstance]("mol", 1)
