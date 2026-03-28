"""Red-phase contract tests for secret scanning service behavior."""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from tests.security.fixtures.scan_samples import sample_history_findings, sample_tree_findings


def _load_symbol(module_name: str, symbol_name: str) -> Any:
    """Load src.security symbol with assertion-style red failure behavior.

    Args:
        module_name: Module name under src.security.
        symbol_name: Required symbol in the loaded module.

    Returns:
        The loaded symbol object.

    """
    module_path = f"src.security.{module_name}"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing remediation module '{module_path}'. Implement chunk 001 scanner contracts. {exc}",
            pytrace=False,
        )

    if not hasattr(module, symbol_name):
        pytest.fail(
            f"Module '{module_path}' is missing required symbol '{symbol_name}'.",
            pytrace=False,
        )
    return getattr(module, symbol_name)


def test_secret_scan_service_exposes_profile_specific_scan_methods() -> None:
    """Verify scan service exposes tree, refs, and history profile entry points."""
    secret_scan_service = _load_symbol("secret_scan_service", "SecretScanService")
    service = secret_scan_service()

    assert callable(getattr(service, "scan_tree", None)), "scan_tree must exist for AC-001 tree scanning"
    assert callable(getattr(service, "scan_refs", None)), "scan_refs must exist for AC-004 rewrite verification"
    assert callable(
        getattr(service, "scan_history", None),
    ), "scan_history must exist for AC-004 historical purge checks"


def test_secret_scan_service_deterministically_orders_finding_keys() -> None:
    """Verify deterministic finding-key ordering for reproducible gate decisions."""
    secret_scan_service = _load_symbol("secret_scan_service", "SecretScanService")
    service = secret_scan_service()

    normalize_keys = getattr(service, "normalize_finding_keys", None)
    assert callable(normalize_keys), "normalize_finding_keys must exist to enforce deterministic ordering"

    normalized = normalize_keys(sample_history_findings())
    normalized_fingerprints = [item["fingerprint"] for item in normalized]
    assert normalized_fingerprints == ["fp-hist-001", "fp-hist-009"]


def test_secret_scan_service_fails_closed_on_scanner_execution_error() -> None:
    """Verify scanner execution exceptions produce blocking ERROR status reports."""
    secret_scan_service = _load_symbol("secret_scan_service", "SecretScanService")
    service = secret_scan_service()

    def _raise_tool_error(*_: Any, **__: Any) -> dict[str, Any]:
        """Raise deterministic scanner failure for fail-closed assertions.

        Raises:
            RuntimeError: Always raised to simulate scanner failure.

        """
        raise RuntimeError("scanner crashed")

    service._execute_profile = _raise_tool_error

    report = service.scan_tree(sample_tree_findings())
    assert report.status == "ERROR"
    assert report.blocking is True
    assert "scanner crashed" in report.error_message
