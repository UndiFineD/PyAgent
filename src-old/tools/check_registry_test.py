#!/usr/bin/env python3
"""Auto-synced test for tools/check_registry.py."""
# Auto-synced test for tools/check_registry.py
import importlib.util
import pathlib


def _load_module() -> object:
    """Dynamically load the module under test."""
    p = pathlib.Path(__file__).parent / "check_registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load spec from {p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols() -> None:
    """Test that the module imports and contains expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "run_diagnostic"), "run_diagnostic missing"
