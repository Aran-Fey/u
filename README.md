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
SPEED = u.DIV[u.DISTANCE, u.DURATION]
Speed = u.Quantity[SPEED]

speed: Speed = u.km(5) / u.hours(1)  # Ok
speed: Speed = (u.km / u.hours)(5)  # Also ok

ELECTRIC_CHARGE = u.MUL[u.DURATION, u.ELECTRIC_CURRENT]
ElectricCharge = u.Quantity[ELECTRIC_CHARGE]

charge: ElectricCharge = u.sec(3) * u.amperes(2)  # Ok
charge: ElectricCharge = u.amperes(2) * u.sec(3)  # Also ok
```

Reusable prefixes:

```python
print(u.megabytes(5) == u.mega(u.bytes)(5))  # True
```

Define your own quantities and units:

```python
class TASTINESS(u.QUANTITY):
    pass

Tastiness = u.Quantity[TASTINESS]

mmm = u.Unit(Tastiness, symbol='mmm', multiplier=1)
yum = u.Unit(Tastiness, 'yum', 10)

taste: Tastiness = yum(42)
```

## Caveats

Since type checkers don't understand math, calculations involving different types of quantities are
only type safe as long as they follow a pre-defined order. For example:

```python
ACCELERATION = typing.Union[
    u.DIV[u.SPEED, u.DURATION],
    u.DIV[u.DISTANCE, u.SQUARE[u.DURATION]],
]
Acceleration = u.Quantity[ACCELERATION]

accel: Acceleration = (u.meters_per_second / u.second)(1)  # Ok
accel = (u.meter / u.second**2)(1)  # Also ok
accel = (u.meters_per_second_squared * u.kelvins / u.kelvins)(1)  # Type checking error
```
