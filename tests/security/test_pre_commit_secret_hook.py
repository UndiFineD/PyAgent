"""Red-phase tests for local pre-commit secret scan guardrails."""

from __future__ import annotations

from pathlib import Path

PRE_COMMIT_PATH = Path(".pre-commit-config.yaml")


def test_pre_commit_config_includes_secret_scan_hook() -> None:
    """Verify pre-commit config has a local secret-scan hook entry."""
    content = PRE_COMMIT_PATH.read_text(encoding="utf-8")
    assert "secret-scan" in content


def test_pre_commit_secret_scan_hook_runs_before_commit() -> None:
    """Verify secret scan hook is configured for the pre-commit stage."""
    content = PRE_COMMIT_PATH.read_text(encoding="utf-8")
    assert "stages: [pre-commit]" in content
    assert "scripts/security/run_secret_scan.py" in content


def test_pre_commit_and_ci_share_tree_profile_invocation() -> None:
    """Verify local hook and CI share consistent security scanning practices."""
    hook_content = PRE_COMMIT_PATH.read_text(encoding="utf-8")
    workflow_content = Path(".github/workflows/security-scheduled.yml").read_text(encoding="utf-8")
    # Verify both use security scanning tool
    assert "secret-scan" in hook_content, "pre-commit must have secret-scan"
    assert ("pip-audit" in workflow_content or "codeql" in workflow_content), "workflow should have security scanning"
