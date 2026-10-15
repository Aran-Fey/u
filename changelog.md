# Unreleased

- `Quantity` now supports `abs()`
- Add `u.Point`
- Add `u.Angle` and its units (`radians`, `degrees`, `gradians`, `turns`, `arcminutes`,
  `arcseconds`)
- Add `u.milliseconds` (`u.ms`), `u.microseconds` (`u.μs`, `u.us`) and `u.nanoseconds` (`u.ns`)
- Add ASCII aliases for the other micro units: `u.um` (micrometers) and `u.ug` (micrograms)
- Parsing now accepts "μ" (GREEK SMALL LETTER MU) and "u" as alternative spellings of the micro
  prefix "µ" (MICRO SIGN), e.g. `u.Duration.parse("5us")`. Output still uses "µ".
- Export `u.kilobytes` (`u.kB`), which existed but was missing from `__all__`
- `Duration.parse` now also accepts the formats "HH:MM:SS", "MM:SS" and "SS", optionally with
  fractional seconds like "1:30.5". The leading number is unlimited (e.g. "90:00" is 90 minutes),
  but the following numbers must have 2 digits and be between 00 and 59.
- Durations can now be formatted as `H:MM:SS`, `HH:MM:SS`, `M:SS`, `MM:SS` or `SS`, e.g.
  `f"{duration:MM:SS}"`. `f"{duration::}"` uses the shortest of these, and a number format can be
  prepended: `f"{duration:.2f :}"`.
- Ordering (`<`, `<=`, `>`, `>=`) quantities of different kinds, like a duration and a distance, now
  raises a `TypeError` instead of returning `False`, and is also a type checking error now.
  Equality comparisons still return `False`, just like `1 == "1"`.
- Adding or subtracting a number other than 0 now raises a `TypeError` instead of an
  `AttributeError` or `AssertionError`
- Adding or subtracting quantities of different kinds now raises a `TypeError` instead of a
  `ValueError`, consistent with ordering and with what type checkers report. (`to_number` with an
  incompatible unit still raises a `ValueError`.)
- Comparisons and hashing now use the quantities' values in the base unit, computed with Decimal
  precision. This makes equality symmetric and fixes cases like `u.inches(1) == u.centimeters(2.54)`.
  `float(quantity)` uses the same Decimal precision.
- Fix equal quantities having different hashes (e.g. `u.minutes(1)` and `u.seconds(60)`), which
  broke sets and dict keys
- Fix quantities that cancel out not being removed, e.g. `u.minutes(1) / u.seconds(1)` was not a
  `u.One`, and `u.m * u.s / u.s` was not compatible with `u.Distance`
- Fix `typing.get_type_hints` crashing on Python 3.14 for functions annotated with quantities.
  (`Quantity[(X,)]` is now equivalent to `Quantity[X]`.)
- Fix `typing.Annotated[u.Duration, ...]` crashing on Python 3.10
- Fix `str()` of short durations, e.g. `u.seconds(0.0015)` was printed as "0.0 s" instead of
  "1.5 ms"
- Prefixes can now be applied to any unit. The prefix is attached to the first factor of the
  symbol that has an exponent of 1 and no prefix yet (`u.kilo(u.mps)` is "km/s"). If there is no
  such factor, the symbol is wrapped in parentheses: `u.kilo(u.m2)` is "k(m²)", i.e. 1000 m².
  Previously, prefixing unregistered compound units raised a `ValueError`, and prefixing registered
  ones like `u.m2` produced misleading symbols like "km²" (which means 10⁶ m²).
- Fix `str()` printing nonsensical symbols like "3 kkm²" for `u.km2(3000)`

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
