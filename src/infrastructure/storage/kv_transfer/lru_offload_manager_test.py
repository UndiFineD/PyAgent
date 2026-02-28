# Auto-synced test for infrastructure/storage/kv_transfer/lru_offload_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "lru_offload_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "LRUEntry"), "LRUEntry missing"
    assert hasattr(mod, "LRUOffloadManager"), "LRUOffloadManager missing"
    assert hasattr(mod, "WeightedLRUManager"), "WeightedLRUManager missing"
    assert hasattr(mod, "TieredLRUManager"), "TieredLRUManager missing"
    assert hasattr(mod, "PrefetchingLRUManager"), "PrefetchingLRUManager missing"
    assert hasattr(mod, "AsyncLRUManager"), "AsyncLRUManager missing"
    assert hasattr(mod, "LRUManagerFactory"), "LRUManagerFactory missing"

