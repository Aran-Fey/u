import u


accel: u.Acceleration = u.mps2(5)  # Is this a valid type annotation?

# Do quantities have the expected attributes/methods?
u.Speed.exponents
u.Quantity[u.SPEED].exponents

u.Area.units

u.Distance.parse("3m")
u.Area.parse("3m²")
u.ElectricCharge.parse("3C")
u.Speed.parse("3m/s")
u.Acceleration.parse("3m/s²")


# Math with numbers
print(-accel)
print(accel * 3)
print(1 / accel)

# Operations with 0
print(accel + 0, 0 + accel, accel - 0, 0 - accel)
print(accel < 0, accel <= 0, accel == 0, accel != 0, accel >= 0, accel > 0)

# Make sure Unions work as expected
a: u.Quantity[u.DISTANCE | u.DURATION] = u.seconds(3)
b: u.Quantity[u.MUL[u.DISTANCE | u.DURATION, u.DATA_VOLUME]] = (u.seconds * u.bytes)(3)
c: u.Quantity[u.DIV[u.DISTANCE | u.DURATION, u.DATA_VOLUME]] = (u.seconds / u.bytes)(3)
