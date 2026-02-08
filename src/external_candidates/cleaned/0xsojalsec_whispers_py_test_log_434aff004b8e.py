# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_whispers.py\tests.py\unit.py\test_log_434aff004b8e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-whispers\tests\unit\test_log.py

from os import remove, urandom

import pytest

from whispers.log import cleanup_log, configure_log, debug

from tests.unit.conftest import does_not_raise


@pytest.mark.parametrize(
    ("logpath", "expectation"),
    [
        (None, pytest.raises(ValueError)),
        ("", does_not_raise()),
        ("/tmp", does_not_raise()),
    ],
)
def test_configure_log(logpath, expectation):

    with expectation:
        expected_file = configure_log(logpath)

        assert expected_file.exists()

        remove(expected_file.as_posix())


@pytest.mark.parametrize(
    ("data", "expectation"),
    [
        ("", False),
        ("a", True),
    ],
)
def test_cleanup_log(data, expectation):

    logfile = configure_log()

    logfile.write_text(data)

    cleanup_log()

    assert logfile.exists() == expectation

    if logfile.exists():
        remove(logfile.as_posix())


def test_debug():

    logfile = configure_log()

    message = urandom(30).hex()

    try:
        1 / 0

    except Exception:
        debug(message)

    logtext = logfile.read_text()

    assert "ZeroDivisionError: division by zero" in logtext

    assert message in logtext
