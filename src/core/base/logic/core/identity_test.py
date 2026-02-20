#!/usr/bin/env python3
""
Minimal smoke test for IdentityCore importability.""
try:
    from src.core.base.logic.core.identity_core import IdentityCore  # type: ignore
except Exception:  # pragma: no cover - test shim
    IdentityCore = None  # type: ignore


def test_identity_core_importable() -> None:
    if IdentityCore is None:
        raise ImportError("IdentityCore not importable")
    core = IdentityCore()
    assert core is not None
