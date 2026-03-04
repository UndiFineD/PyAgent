#!/usr/bin/env python3
# Auto-synced test for observability/stats/storage_engine.py
import importlib.util
import pathlib


def _load_module():
    """Dynamically loads the module under test."""
    p = pathlib.Path(__file__).parent / "storage_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    if spec is None:
        raise RuntimeError(f"Failed to load module spec from {p}")
    if spec.loader is None:
        raise RuntimeError(f"Failed to load module loader from {p}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    """Test that the module can be imported and contains expected symbols."""
    mod = _load_module()
    assert hasattr(mod, "StatsBackup"), "StatsBackup missing"
    assert hasattr(mod, "StatsBackupManager"), "StatsBackupManager missing"
    assert hasattr(mod, "StatsSnapshotManager"), "StatsSnapshotManager missing"
    assert hasattr(mod, "StatsCompressor"), "StatsCompressor missing"

