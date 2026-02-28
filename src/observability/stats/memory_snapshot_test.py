# Auto-synced test for observability/stats/memory_snapshot.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "memory_snapshot.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MemorySnapshot"), "MemorySnapshot missing"
    assert hasattr(mod, "capture_memory_snapshot"), "capture_memory_snapshot missing"
    assert hasattr(mod, "MemoryProfiler"), "MemoryProfiler missing"
    assert hasattr(mod, "memory_profile"), "memory_profile missing"
    assert hasattr(mod, "GCDebugger"), "GCDebugger missing"
    assert hasattr(mod, "freeze_gc_heap"), "freeze_gc_heap missing"
    assert hasattr(mod, "unfreeze_gc_heap"), "unfreeze_gc_heap missing"
    assert hasattr(mod, "gc_stats"), "gc_stats missing"

