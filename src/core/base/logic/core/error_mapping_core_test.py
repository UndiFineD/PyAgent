#!/usr/bin/env python3
""
Minimal smoke test for ErrorMappingCore importability.""
try:
    from src.core.base.logic.core.error_mapping_core import ErrorMappingCore  # type: ignore
except Exception:  # pragma: no cover - test shim
    ErrorMappingCore = None  # type: ignore


def test_error_mapping_core_importable() -> None:
    if ErrorMappingCore is None:
        raise ImportError("ErrorMappingCore not importable")
    em = ErrorMappingCore()
    assert em is not None
