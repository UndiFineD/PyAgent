# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_make_circuit_boards.py\tests.py\test_config_a2d12e0a1667.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-make-circuit-boards\tests\test_config.py

from atopile import config


def test_sanitise_dict_keys():
    """Test that dict keys are sanitised."""

    assert config._sanitise_dict_keys({"a-b": 1, "ato-version": {"e-f": 2}}) == {
        "a-b": 1,
        "ato_version": {"e-f": 2},
    }
