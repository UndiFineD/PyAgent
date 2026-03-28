"""Red-phase tests for CI workflow secret guardrail merge-block behavior."""

from __future__ import annotations

from pathlib import Path

WORKFLOW_PATH = Path(".github/workflows/security.yml")


def test_security_workflow_defines_secret_scan_job() -> None:
    """Verify security workflow defines dedicated secret-scan CI job."""
    content = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "secret_scan" in content or "secret-scan" in content


def test_security_workflow_fails_closed_on_secret_findings() -> None:
    """Verify security workflow enforces fail-closed secret scan gate."""
    content = WORKFLOW_PATH.read_text(encoding="utf-8")
    fail_closed_signals = [
        "--fail-on-severity",
        "--min-severity HIGH",
        "exit 1",
        "fail-on-findings",
    ]
    assert any(signal in content for signal in fail_closed_signals)
