"""Red-phase tests for containment cleanup and runbook requirements."""

from __future__ import annotations

from pathlib import Path

RUNBOOK_PATH = Path("docs/security/private-key-remediation-runbook.md")
VERIFIER_SCRIPT_PATH = Path("scripts/security/verify_no_key_material.py")


def test_runbook_includes_containment_evidence_section() -> None:
    """Verify runbook includes containment evidence and incident linkage details."""
    assert RUNBOOK_PATH.exists(), "Runbook must exist for AC-005 remediation operations"
    content = RUNBOOK_PATH.read_text(encoding="utf-8")
    assert "Containment Evidence" in content
    assert "Incident ID" in content


def test_cleanup_verifier_exists_and_is_repo_path_scoped() -> None:
    """Verify cleanup verification script exists and scans deterministic repo paths."""
    assert VERIFIER_SCRIPT_PATH.exists(), "Verifier script is required for deterministic cleanup checks"
    content = VERIFIER_SCRIPT_PATH.read_text(encoding="utf-8")
    assert "rust_core" in content
    assert "docs/security" in content
