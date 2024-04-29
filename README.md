# u

Statically typed units.

## Quickstart

```python
# Type safe assignments
duration: u.Duration = u.seconds(5)  # Ok
distance: u.Distance = u.amperes(5)  # Type checking error

# Type safe math
print(u.seconds(120) + u.minutes(3))  # Ok
print(u.seconds(120) + u.amperes(3))  # Type checking error

# Type safe compound units (with some caveats)
speed: u.Div[u.Distance, u.Duration] = u.km(5) / u.hours(1)  # Ok

# Reusable prefixes
print(u.bytes(1000) == u.mega(u.bytes)(1))  # True

# Define your own Quantities and Units
class Tastiness(u.Quantity):
    pass

mmm = u.Unit[Tastiness](symbol='mmm', multiplier=1)
yum = u.Unit[Tastiness]('yum', 10)

taste: Tastiness = yum(42)
```
