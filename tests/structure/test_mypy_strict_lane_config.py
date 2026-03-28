#!/usr/bin/env python3
"""Contract tests for strict-lane mypy configuration."""

from configparser import ConfigParser
from pathlib import Path

STRICT_CONFIG_PATH = Path("mypy-strict-lane.ini")
EXPECTED_ALLOWLIST = [
    "src/core/audit/AuditEvent.py",
    "src/core/audit/exceptions.py",
    "src/core/resilience/CircuitBreakerConfig.py",
    "src/core/resilience/CircuitBreakerState.py",
    "src/core/resilience/exceptions.py",
    "src/core/universal/exceptions.py",
    "src/core/fuzzing/exceptions.py",
    "src/core/n8nbridge/exceptions.py",
    "src/core/replay/exceptions.py",
    "src/core/sandbox/SandboxViolationError.py",
]


def _load_strict_config() -> ConfigParser:
    """Load strict-lane mypy config from disk.

    Returns:
        ConfigParser: Parsed configuration.

    """
    assert STRICT_CONFIG_PATH.exists(), (
        "Expected strict-lane config at mypy-strict-lane.ini. "
        "Create it with strict enforcement options and the locked allowlist."
    )

    parser = ConfigParser()
    parser.read(STRICT_CONFIG_PATH, encoding="utf-8")
    assert parser.has_section("mypy"), "mypy-strict-lane.ini must contain a [mypy] section."
    return parser


def _normalize_files_value(files_value: str) -> list[str]:
    """Normalize mypy files option to a deterministic list.

    Args:
        files_value: Raw value of the `files` key from config.

    Returns:
        list[str]: Ordered normalized path list.

    """
    normalized = files_value.replace(",", "\n")
    return [line.strip() for line in normalized.splitlines() if line.strip()]


def test_mypy_strict_lane_required_options() -> None:
    """Require strict-lane config to enforce strict mypy options.

    Returns:
        None.

    """
    parser = _load_strict_config()
    expected_options = {
        "strict": "True",
        "ignore_errors": "False",
        "show_error_codes": "True",
        "warn_unused_ignores": "True",
    }

    for key, expected in expected_options.items():
        assert parser.has_option("mypy", key), f"Missing '{key}' in mypy-strict-lane.ini [mypy] section."
        assert parser.get("mypy", key) == expected, (
            f"mypy-strict-lane.ini must set {key} = {expected} for strict-lane contract."
        )


def test_mypy_strict_lane_allowlist_locked() -> None:
    """Require strict-lane config to match the locked Wave 1 allowlist exactly.

    Returns:
        None.

    """
    parser = _load_strict_config()
    assert parser.has_option("mypy", "files"), "mypy-strict-lane.ini must define a [mypy] files allowlist."

    actual_allowlist = _normalize_files_value(parser.get("mypy", "files"))
    assert actual_allowlist == EXPECTED_ALLOWLIST, (
        "Strict-lane allowlist drift detected. The [mypy] files value must exactly match "
        "the locked Wave 1 10-file list."
    )
