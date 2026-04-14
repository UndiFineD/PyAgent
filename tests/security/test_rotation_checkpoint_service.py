"""Red-phase tests for rotation checkpoint service lifecycle behavior."""

from __future__ import annotations

import importlib
from typing import Any

import pytest


def _load_rotation_symbol(module_name: str, symbol_name: str) -> Any:
    """Load rotation symbols with assertion-style red failure behavior.

    Args:
        module_name: Module name under src.security.
        symbol_name: Required symbol name inside module.

    Returns:
        Loaded symbol.

    """
    module_path = f"src.security.{module_name}"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing remediation module '{module_path}'. Implement chunk 001 rotation contracts. {exc}",
            pytrace=False,
        )

    if not hasattr(module, symbol_name):
        pytest.fail(f"Module '{module_path}' must expose '{symbol_name}'.", pytrace=False)
    return getattr(module, symbol_name)


def test_begin_incident_records_incident_and_fingerprint() -> None:
    """Verify incident creation persists incident_id and compromised fingerprint."""
    service_cls = _load_rotation_symbol("rotation_checkpoint_service", "RotationCheckpointService")
    service = service_cls()

    created = service.begin_incident(
        incident_id="INC-20260328-001",
        compromised_fingerprint="fp-tree-001",
        required_systems=["git-signing", "deployment-keys"],
    )
    assert created.incident_id == "INC-20260328-001"
    assert created.compromised_fingerprint == "fp-tree-001"
    assert created.required_systems == ["git-signing", "deployment-keys"]


def test_record_rotation_step_requires_evidence_uri() -> None:
    """Verify evidence URI is mandatory for checkpoint step persistence."""
    service_cls = _load_rotation_symbol("rotation_checkpoint_service", "RotationCheckpointService")
    service = service_cls()

    service.begin_incident(
        incident_id="INC-20260328-002",
        compromised_fingerprint="fp-tree-002",
        required_systems=["git-signing"],
    )

    with pytest.raises(ValueError):
        service.record_rotation_step(
            incident_id="INC-20260328-002",
            system="git-signing",
            evidence_uri="",
        )
