"""Red-phase tests for rotation gate decision transition semantics."""

from __future__ import annotations

import importlib
from typing import Any

import pytest


def _load_rotation_service() -> Any:
    """Load RotationCheckpointService with assertion-style red failure behavior.

    Returns:
        RotationCheckpointService class.

    """
    module_path = "src.security.rotation_checkpoint_service"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing remediation module '{module_path}'. Implement chunk 001 gate contracts. {exc}",
            pytrace=False,
        )
    if not hasattr(module, "RotationCheckpointService"):
        pytest.fail("RotationCheckpointService is required for AC-002 gate transitions.", pytrace=False)
    return module.RotationCheckpointService


def test_evaluate_gate_transitions_blocked_to_partial_to_complete() -> None:
    """Verify deterministic gate transitions for evidence completeness."""
    service_cls = _load_rotation_service()
    service = service_cls()

    service.begin_incident(
        incident_id="INC-20260328-003",
        compromised_fingerprint="fp-tree-003",
        required_systems=["git-signing", "deployment-keys"],
    )

    blocked = service.evaluate_gate("INC-20260328-003")
    assert blocked.status == "BLOCKED"
    assert blocked.missing_systems == ["git-signing", "deployment-keys"]

    service.record_rotation_step(
        incident_id="INC-20260328-003",
        system="git-signing",
        evidence_uri="evidence://rotation/git-signing",
    )
    partial = service.evaluate_gate("INC-20260328-003")
    assert partial.status == "PARTIAL"
    assert partial.missing_systems == ["deployment-keys"]

    service.record_rotation_step(
        incident_id="INC-20260328-003",
        system="deployment-keys",
        evidence_uri="evidence://rotation/deployment-keys",
    )
    complete = service.evaluate_gate("INC-20260328-003")
    assert complete.status == "COMPLETE"
    assert complete.missing_systems == []
