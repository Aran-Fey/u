# fmt: off
from ..prefixes import (
    kilo, mega, giga, tera, peta, exa, zetta, yotta,
    kibi, mebi, gibi, tebi, pebi, exbi, zebi, yobi,
)
# fmt: on
from ..quantity_and_unit import Quantity, Unit


# fmt: off
__all__ = [
    "DataVolume",
    "bytes", "byte", "B",
]
# fmt: on


class DataVolume(Quantity):
    pass


# TODO: Bits don't really fit in here. I initially wanted to define a byte as 8 bits, but that's not
# true - 8 bits is an octet. Bytes don't have a fixed amount of bits.
# bits = bit = b = Unit[FileSize]('b', 1)

bytes = byte = B = Unit[DataVolume]("B", 1)

kilobytes = kilobyte = kB = kilo(bytes)
megabytes = megabyte = MB = mega(bytes)
gigabytes = gigabyte = GB = giga(bytes)
terabytes = terabyte = TB = tera(bytes)
petabytes = petabyte = PB = peta(bytes)
exabytes = exabyte = EB = exa(bytes)
zettabytes = zettabyte = ZB = zetta(bytes)
yottabytes = yottabyte = YB = yotta(bytes)

kibibytes = kibibyte = kiB = kibi(bytes)
mebibytes = mebibyte = MiB = mebi(bytes)
gibibytes = gibibyte = GiB = gibi(bytes)
tebibytes = tebibyte = TiB = tebi(bytes)
pebibytes = pebibyte = PiB = pebi(bytes)
exbibytes = exbibyte = EiB = exbi(bytes)
zebibytes = zebibyte = ZiB = zebi(bytes)
yobibytes = yobibyte = YiB = yobi(bytes)
