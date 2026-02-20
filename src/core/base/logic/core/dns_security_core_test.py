#!/usr/bin/env python3
"""
Minimal smoke test for DNS security core importability.""
try:
    from src.core.base.logic.core.dns_security_core import DnsSecurityCore  # type: ignore
except Exception:  # pragma: no cover - test shim
    DnsSecurityCore = None  # type: ignore


def test_dns_security_core_importable() -> None:
"""
Simple import/instantiate smoke test.""
if DnsSecurityCore is None:
        # Let pytest record the import error instead of failing here
        raise ImportError("DnsSecurityCore not importable")
    core = DnsSecurityCore()
    assert core is not None
