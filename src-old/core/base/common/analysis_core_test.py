#!/usr/bin/env python3
# Auto-synced test for core/base/common/analysis_core.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically load the module under test."""
    p = pathlib.Path(__file__).parent / "analysis_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise ValueError(f"Failed to load spec from {p}")
    mod = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ValueError(f"Failed to get loader from spec for {p}")
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module imports and key symbols are present."""
    mod = _load_module()
    assert hasattr(mod, "AnalysisCore"), "AnalysisCore missing"
