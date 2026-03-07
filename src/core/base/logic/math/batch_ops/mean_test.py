#!/usr/bin/env python3
"""Auto-synced test for core/base/logic/math/batch_ops/mean.py"""
# Auto-synced test for core/base/logic/math/batch_ops/mean.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically load the module under test."""
    p = pathlib.Path(__file__).parent / "mean.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    assert spec is not None, f"Failed to load spec from {p}"
    assert spec.loader is not None, f"Failed to load loader from {p}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module imports and contains the expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "mean_batch_invariant"), "mean_batch_invariant missing"
