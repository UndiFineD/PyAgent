#!/usr/bin/env python3
"""Test suite for inference_core.py."""
# Auto-synced test for core/base/common/inference_core.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically load the module under test."""
    p = pathlib.Path(__file__).parent / "inference_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to load spec from {p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module can be imported and key symbols are present."""
    mod = _load_module()
    assert hasattr(mod, "InferenceCore"), "InferenceCore missing"
