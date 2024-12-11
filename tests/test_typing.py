import re
import subprocess
import sys
import typing as t
from pathlib import Path

import mypy.api
import pytest

import u


def validate_typing(code: str, *, disabled_error_codes: t.Iterable[str] = ()) -> None:
    cmd = [sys.executable, "-m", "mypy", "-c", f"import typing\nimport u\n{code}"]

    for error_code in disabled_error_codes:
        cmd += ["--disable-error-code", error_code]

    process = subprocess.run(cmd, capture_output=True, text=True)

    if process.returncode == 0:
        return

    raise Exception(process.stdout)


def test_typevars_at_runtime():
    # PyRight *really* doesn't like typing stuff inside of a function, which is why there are so
    # many `type: ignore`s here.
    Q = t.TypeVar("Q", bound=u.QUANTITY)

    ZeroOrQuantity = t.Literal[0] | u.Quantity[Q]  # type: ignore
    ZeroOrDuration = ZeroOrQuantity[u.DURATION]  # type: ignore

    Speed = u.Quantity[u.DIV[Q, u.DURATION]]  # type: ignore
    DownloadSpeed = Speed[u.DATA_VOLUME]  # type: ignore


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

    # Note: Originally, this code passed the file path to mypy instead of reading the contents into
    # memory. But for some godforsaken reason, that made mypy detect all sorts of nonsensical
    # errors. (I even made sure that the CWD was set to the project directory and that PYTHONPATH
    # was cleared.)
    validate_typing(file_path.read_text())


def test_readme_code():
    file_path = Path(__file__).absolute().parent.parent / "README.md"

    code_block_regex = re.compile(r"```(?:python|py)?\n(.*?)```", flags=re.S)
    mypy_error_regex = re.compile(r"<string>:(\d+): error: (.*)")

    for match in code_block_regex.finditer(file_path.read_text()):
        snippet = match.group(1).strip()

        try:
            validate_typing(snippet, disabled_error_codes=["no-redef"])
        except Exception as error:
            lines_with_errors = {
                int(match.group(1)) - 2: match.group(2)
                for match in mypy_error_regex.finditer(str(error))
            }
        else:
            lines_with_errors = {}

        errors_expected_on_lines = {
            line_nr
            for line_nr, line in enumerate(snippet.splitlines(), 1)
            if "# Type checking error" in line
        }

        for line_nr, error in lines_with_errors.items():
            assert (
                line_nr in errors_expected_on_lines
            ), f"Unexpected type checking error.\nCode:\n{snippet}\nError in line {line_nr}: {error}"

        for line_nr in errors_expected_on_lines - lines_with_errors.keys():
            assert (
                False
            ), f"Expected error in line {line_nr}, but there wasn't one.\nCode:\n{snippet}"
