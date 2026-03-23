# 4.0

- Comparison operators in `Quantity` no longer use `math.isclose`, and hashing no longer rounds.
  Basically, comparing `Quantity` objects is now just as unpredictable as comparing floats. The
  upside is that equality is now transitive. (i.e. if `a == b` and `b == c`, then `a == c`.)

# 3.1

- Add `__hash__` method

# 3.0

- Add support for `decimal.Decimal`. Unlike floats and Decimals, which throw a TypeError when used
  together, `Quantity`s remain interoperable regardless of whether they were created with a float or
  a Decimal.
- `Unit.multiplier` is now a Decimal.
- Add `systems` parameter and attribute to `Unit`

# 2.1

- `Quantity.to_number` now raises `ValueError` if an incompatible unit is passed

# 2.0

- Removed `.unit` attribute of `Quantity` objects
- Renamed `ton` to `tonne`
