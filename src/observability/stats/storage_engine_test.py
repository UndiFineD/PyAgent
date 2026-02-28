# Auto-synced test for observability/stats/storage_engine.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "storage_engine.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "StatsBackup"), "StatsBackup missing"
    assert hasattr(mod, "StatsBackupManager"), "StatsBackupManager missing"
    assert hasattr(mod, "StatsSnapshotManager"), "StatsSnapshotManager missing"
    assert hasattr(mod, "StatsCompressor"), "StatsCompressor missing"

