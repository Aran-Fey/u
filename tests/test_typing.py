import subprocess
import sys
import typing as t
from pathlib import Path

import pytest

import u


def test_typevar():
    Q = t.TypeVar("Q", bound=u.QUANTITY)

    ZeroOrQuantity = t.Literal[0] | u.Quantity[Q]  # type: ignore
    ZeroOrDuration = ZeroOrQuantity[u.DURATION]  # type: ignore

    Speed = u.Quantity[u.DIV[Q, u.DURATION]]  # type: ignore
    DownloadSpeed = Speed[u.DATA_VOLUME]  # type: ignore


def validate_typing(code: str) -> None:
    process = subprocess.run(
        [sys.executable, "-m", "mypy", "-c", f"import u\n{code}"],
        capture_output=True,
        text=True,
    )

    if process.returncode == 0:
        return

    raise Exception(process.stderr)


@pytest.mark.parametrize(
    "expr",
    [
        "duration: u.Duration = u.seconds(5)",
        "u.seconds(120) + u.minutes(3)",
        "speed: u.Speed = u.km(5) / u.hours(1)",
        "speed: u.Speed = (u.km / u.hours)(5)",
        "charge: u.ElectricCharge = u.sec(3) * u.amperes(2)",
        "charge: u.ElectricCharge = u.amperes(2) * u.sec(3)",
        "freq: u.Frequency = 1 / u.sec(4)",
        "u.megabytes(5) == u.mega(u.bytes)(5)",
        """
class TASTINESS(u.QUANTITY):
    pass

Tastiness = u.Quantity[TASTINESS]

mmm = u.Unit(Tastiness, symbol='mmm', multiplier=1)
yum = u.Unit(Tastiness, 'yum', 10)

taste: Tastiness = yum(42)
""",
    ],
)
def test_typing_is_correct(expr: str):
    validate_typing(expr)


@pytest.mark.parametrize(
    "expr",
    [
        "d: Distance = seconds(3)",
        "s: Speed = seconds(5) / meters(2)",
    ],
)
def test_typing_error(expr: str):
    with pytest.raises(Exception):
        validate_typing(expr)


def test_static_tests_file():
    file_path = Path(__file__).parent / "static_tests.py"
    process = subprocess.run(
        [sys.executable, "-m", "mypy", str(file_path)],
        capture_output=True,
        text=True,
    )

    if process.returncode == 0:
        return

    raise Exception(process.stderr)
