# 3.0

- Add support for `decimal.Decimal`. Unlike floats and Decimals, which throw a TypeError when used
  together, `Quantity`s remain interoperable regardless of whether they were created with a float or
  a Decimal.
- `Unit.multiplier` is now a Decimal.

# 2.1

- `Quantity.to_number` now raises `ValueError` if an incompatible unit is passed

# 2.0

- Removed `.unit` attribute of `Quantity` objects
- Renamed `ton` to `tonne`
