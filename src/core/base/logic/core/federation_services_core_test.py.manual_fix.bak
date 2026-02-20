#!/usr/bin/env python3
"""Smoke test for FederationServicesCore importability."""
try:
    from src.core.base.logic.core.federation_services_core import FederationServicesCore  # type: ignore
except Exception:  # pragma: no cover - test shim
    FederationServicesCore = None  # type: ignore


def test_federation_services_core_importable() -> None:
    if FederationServicesCore is None:
        raise ImportError("FederationServicesCore not importable")
    core = FederationServicesCore()
    assert core is not None
