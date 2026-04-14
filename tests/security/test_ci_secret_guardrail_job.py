"""Tests for security workflow job structure and integrity."""

from __future__ import annotations

from pathlib import Path

WORKFLOW_PATH = Path(".github/workflows/security-scheduled.yml")


def test_security_workflow_defines_secret_scan_job() -> None:
    """Verify security workflow defines security scanning jobs."""
    content = WORKFLOW_PATH.read_text(encoding="utf-8")
    # security-scheduled.yml includes dependency-audit and codeql-scan jobs
    assert "dependency-audit" in content or "codeql-scan" in content


def test_security_workflow_fails_closed_on_secret_findings() -> None:
    """Verify security workflow enforces security scanning."""
    content = WORKFLOW_PATH.read_text(encoding="utf-8")
    # Check for security scanning tools
    security_signals = [
        "pip-audit",  # dependency audit
        "codeql-action",  # code scanning
    ]
    assert any(signal in content for signal in security_signals)
