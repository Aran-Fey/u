# u

Statically typed units.

## Quickstart

Type safe assignments:

```python
duration: u.Duration = u.seconds(5)  # Ok
distance: u.Distance = u.amperes(5)  # Type checking error
```

Type safe math:

```python
print(u.seconds(120) + u.minutes(3))  # Ok
print(u.seconds(120) + u.amperes(3))  # Type checking error
```

Type safe derived units:

```python
Speed = u.Div[u.Distance, u.Duration]
speed: Speed = u.km(5) / u.hours(1)  # Ok
speed: Speed = (u.km / u.hours)(5)  # Also ok

ElectricCharge = u.Mul[u.Duration, u.ElectricCurrent]
charge: ElectricCharge = u.sec(3) * u.amperes(2)  # Ok
charge: ElectricCharge = u.amperes(2) * u.sec(3)  # Also ok
```

Reusable prefixes:

```python
print(u.megabytes(5) == u.mega(u.bytes)(5))  # True
```

Define your own quantities and units:

```python
class Tastiness(u.Quantity):
    pass

mmm = u.Unit(Tastiness, symbol='mmm', multiplier=1)
yum = u.Unit(Tastiness, 'yum', 10)

taste: Tastiness = yum(42)
```
