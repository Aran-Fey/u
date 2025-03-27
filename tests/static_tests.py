import typing_extensions as t

import u


# Are Quantities valid type annotations?
accel: u.Acceleration = u.mps2(5)

# Do quantities have the expected attributes/methods?
t.assert_type(u.Distance.base_unit, u.Unit[u.DISTANCE])
t.assert_type(u.Area.units, t.Sequence[u.Unit[u.AREA]])

u.Speed.exponents
u.Quantity[u.SPEED].exponents

t.assert_type(u.Quantity.parse("3m"), u.Quantity)
t.assert_type(u.Distance.parse("3m"), u.Distance)
t.assert_type(u.Area.parse("3m²"), u.Area)
t.assert_type(u.ElectricCharge.parse("3C"), u.ElectricCharge)
t.assert_type(u.Speed.parse("3m/s"), u.Speed)
t.assert_type(u.Acceleration.parse("3m/s²"), u.Acceleration)


# Is unit math type safe?
area: u.Area = (u.m * u.m)(1)
# distance: u.Distance = (u.m2 / u.m)(1)
# accel: u.Acceleration = ((u.kelvin * u.m) / u.s**2 / u.kelvin)(1)
# accel: u.Acceleration = ((u.kelvin / u.s) * (u.m / u.s) / u.kelvin)(1)

# In the calculations above, the type checker knows the exact type of each expression. Make sure
# math also works with unions.
t.reveal_type(t.cast(u.Unit[u.ACCELERATION], ...) * u.s)
# speed: u.Speed = (t.cast(u.Unit[u.ACCELERATION], ...) * u.s)(1)

# Is quantity math type safe?
duration: u.Duration = u.min(2) + u.s(1)
area: u.Area = u.m(1) * u.m(1)
# distance: u.Distance = u.m2(1) / u.m(1)
# accel: u.Acceleration = (u.kelvin(1) * u.m(1)) / u.s(1) ** 2 / u.kelvin(1)
# accel: u.Acceleration = (u.kelvin(1) / u.s(1)) * (u.m(1) / u.s(1)) / u.kelvin(1)
# speed: u.Speed = accel * u.s(1)

# speed: u.Speed = t.cast(u.Acceleration, ...) * u.s(1)

# Math with numbers
print(-accel)
print(accel * 3)
print(1 / accel)

# Operations with 0
print(accel + 0, 0 + accel, accel - 0, 0 - accel)
print(accel < 0, accel <= 0, accel == 0, accel != 0, accel >= 0, accel > 0)

# Make sure TypeVars work as expected
Q = t.TypeVar("Q", bound=u.QUANTITY)

ZeroOrQuantity = t.Union[t.Literal[0], u.Quantity[Q]]
ZeroOrDuration = ZeroOrQuantity[u.DURATION]

Speed = u.Quantity[u.DIV[Q, u.DURATION]]
DownloadSpeed = Speed[u.DATA_VOLUME]
