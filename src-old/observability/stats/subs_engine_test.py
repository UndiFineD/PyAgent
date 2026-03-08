#!/usr/bin/env python3
"""Auto-synced test for observability/stats/subs_engine.py."""
# Auto-synced test for observability/stats/subs_engine.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically loads the module under test."""
    p = pathlib.Path(__file__).parent / "subs_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise ImportError(f"Could not load module spec from {p}")
    mod = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(f"Could not load module loader from {p}")
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module can be imported and contains expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "AnnotationManager"), "AnnotationManager missing"
    assert hasattr(mod, "StatsAnnotationManager"), "StatsAnnotationManager missing"
    assert hasattr(mod, "SubscriptionManager"), "SubscriptionManager missing"
    assert hasattr(mod, "StatsSubscriptionManager"), "StatsSubscriptionManager missing"
