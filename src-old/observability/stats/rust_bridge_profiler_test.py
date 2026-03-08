#!/usr/bin/env python3
# Auto-synced test for observability/stats/rust_bridge_profiler.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically loads the module under test."""
    p = pathlib.Path(__file__).parent / "rust_bridge_profiler.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise ImportError(f"Could not find spec for module at {p}")
    if spec.loader is None:
        raise ImportError(f"Could not find loader for module at {p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module can be imported and contains expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "RustBridgeProfiler"), "RustBridgeProfiler missing"
