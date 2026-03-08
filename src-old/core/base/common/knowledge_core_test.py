#!/usr/bin/env python3
"""Auto-synced test for core/base/common/knowledge_core.py"""
# Auto-synced test for core/base/common/knowledge_core.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically load the knowledge_core module for testing."""
    p = pathlib.Path(__file__).parent / "knowledge_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise RuntimeError(f"Failed to load module spec from {p}")
    if spec.loader is None:
        raise RuntimeError(f"Failed to load module loader from {p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module can be imported and key symbols are present."""
    mod = _load_module()
    assert hasattr(mod, "KnowledgeCore"), "KnowledgeCore missing"
