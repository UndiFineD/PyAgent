"""Red-phase tests for secret guardrail policy decision outcomes."""

from __future__ import annotations

import importlib
from typing import Any

import pytest


def _load_policy_class() -> Any:
    """Load SecretGuardrailPolicy with assertion-style red failure behavior.

    Returns:
        SecretGuardrailPolicy class.

    """
    module_path = "src.security.secret_guardrail_policy"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing remediation module '{module_path}'. Implement chunk 001 guardrail policy. {exc}",
            pytrace=False,
        )
    if not hasattr(module, "SecretGuardrailPolicy"):
        pytest.fail("SecretGuardrailPolicy symbol is required for AC-003 guardrail decisions.", pytrace=False)
    return module.SecretGuardrailPolicy


def test_validate_pr_blocks_when_high_or_critical_findings_exist() -> None:
    """Verify PR validation blocks when findings include HIGH/CRITICAL severities."""
    policy_cls = _load_policy_class()
    policy = policy_cls()

    decision = policy.validate_pr(
        findings=[
            {"fingerprint": "fp-low", "severity": "LOW"},
            {"fingerprint": "fp-high", "severity": "HIGH"},
        ],
    )
    assert decision.status == "BLOCK"
    assert "HIGH" in decision.blocking_reasons[0]


def test_validate_push_blocks_when_critical_findings_exist() -> None:
    """Verify push validation blocks when CRITICAL findings are detected."""
    policy_cls = _load_policy_class()
    policy = policy_cls()

    decision = policy.validate_push(findings=[{"fingerprint": "fp-critical", "severity": "CRITICAL"}])
    assert decision.status == "BLOCK"
    assert any("CRITICAL" in item for item in decision.blocking_reasons)
