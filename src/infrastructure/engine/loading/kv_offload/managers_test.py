# Auto-synced test for infrastructure/engine/loading/kv_offload/managers.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "managers.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LRUOffloadingManager"), "LRUOffloadingManager missing"
    assert hasattr(mod, "ARCOffloadingManager"), "ARCOffloadingManager missing"
    assert hasattr(mod, "TieredOffloadManager"), "TieredOffloadManager missing"
    assert hasattr(mod, "compute_lru_eviction_rust"), "compute_lru_eviction_rust missing"
    assert hasattr(mod, "compute_arc_target_rust"), "compute_arc_target_rust missing"

