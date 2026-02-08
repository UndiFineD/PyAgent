# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_make_circuit_boards.py\tests.py\test_telemetry_7ccfc897f823.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-make-circuit-boards\tests\test_telemetry.py

import pytest

from atopile import telemetry


@pytest.mark.parametrize(
    ("git_remote",),
    [
        ("https://github.com/atopile/atopile.git",),
        ("git@github.com:atopile/atopile.git",),
    ],
)
def test_commonise_project_url(git_remote):

    assert telemetry.commonise_project_url(git_remote) == "github.com/atopile/atopile"
