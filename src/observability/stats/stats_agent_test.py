#!/usr/bin/env python3
"""Test suite for storage_engine.py."""
# Auto-synced test for observability/stats/stats_agent.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically loads the module under test."""
    p = pathlib.Path(__file__).parent / "stats_agent.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise RuntimeError(f"Failed to create module spec for {p}")
    if spec.loader is None:
        raise RuntimeError(f"Failed to create loader for {p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module can be imported and contains expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "StatsAgent"), "StatsAgent missing"
