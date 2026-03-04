#!/usr/bin/env python3
# # Auto-synced test for observability/stats/structured_counter.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically loads the module under test."""
    p = pathlib.Path(__file__).parent / "structured_counter.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise RuntimeError(f"Failed to create module spec for {p}")
    mod = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f"Module spec {p} has no loader")
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module can be imported and contains expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "StructuredCounter"), "StructuredCounter missing"
    assert hasattr(mod, "CompilationCounter"), "CompilationCounter missing"
    assert hasattr(mod, "RequestCounter"), "RequestCounter missing"
    assert hasattr(mod, "CacheCounter"), "CacheCounter missing"
    assert hasattr(mod, "PoolCounter"), "PoolCounter missing"
    assert hasattr(mod, "QueueCounter"), "QueueCounter missing"
    assert hasattr(mod, "get_all_counters"), "get_all_counters missing"
    assert hasattr(mod, "reset_all_counters"), "reset_all_counters missing"
