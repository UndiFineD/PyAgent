"""Red-phase tests for scan report schema and status guarantees."""

from __future__ import annotations

import importlib
from typing import Any

import pytest


def _load_scan_report_model() -> Any:
    """Load ScanReport model with assertion-style red failure behavior.

    Returns:
        The ScanReport model class.

    """
    module_path = "src.security.models.scan_report"
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"Missing remediation model module '{module_path}'. Implement chunk 001 report schema. {exc}",
            pytrace=False,
        )

    if not hasattr(module, "ScanReport"):
        pytest.fail(f"Module '{module_path}' must expose ScanReport.", pytrace=False)
    return module.ScanReport


def test_scan_report_requires_run_id_and_status_enum() -> None:
    """Verify ScanReport enforces run_id and PASS/FAIL/ERROR status values."""
    scan_report = _load_scan_report_model()

    with pytest.raises((TypeError, ValueError, AssertionError)):
        scan_report(status="PASS")

    with pytest.raises((TypeError, ValueError, AssertionError)):
        scan_report(run_id="run-001", status="WARN")

    valid = scan_report(run_id="run-001", status="PASS", findings=[])
    assert valid.run_id == "run-001"
    assert valid.status == "PASS"


def test_scan_report_computes_blocking_from_high_and_critical_findings() -> None:
    """Verify ScanReport marks HIGH/CRITICAL findings as blocking by default."""
    scan_report = _load_scan_report_model()

    report = scan_report(
        run_id="run-002",
        status="FAIL",
        findings=[
            {"fingerprint": "fp-low", "severity": "LOW"},
            {"fingerprint": "fp-high", "severity": "HIGH"},
        ],
    )
    assert report.blocking is True
