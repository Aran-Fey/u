from ..quantity_and_unit import Div
from .data_volume import DataVolume, bytes, kilobytes, megabytes, gigabytes, terabytes
from .duration import Duration, second


# fmt: off
__all__ = [
    "DataTransferSpeed",
    "bytes_per_second", "Bps",
    "kilobytes_per_second", "Bps",
    "megabytes_per_second", "MBps",
    "gigabytes_per_second", "GBps",
    "terabytes_per_second", "TBps",
]
# fmt: on


DataTransferSpeed = Div[DataVolume, Duration]

bytes_per_second = Bps = bytes / second
kilobytes_per_second = KBps = kilobytes / second
megabytes_per_second = MBps = megabytes / second
gigabytes_per_second = GBps = gigabytes / second
terabytes_per_second = TBps = terabytes / second
