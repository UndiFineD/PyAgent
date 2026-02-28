# Auto-synced test for infrastructure/storage/cache/block_pool_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "block_pool_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "BlockState"), "BlockState missing"
    assert hasattr(mod, "Block"), "Block missing"
    assert hasattr(mod, "BlockPoolConfig"), "BlockPoolConfig missing"
    assert hasattr(mod, "EvictionEvent"), "EvictionEvent missing"
    assert hasattr(mod, "CacheMetrics"), "CacheMetrics missing"
    assert hasattr(mod, "KVCacheMetricsCollector"), "KVCacheMetricsCollector missing"
    assert hasattr(mod, "ARCPolicy"), "ARCPolicy missing"
    assert hasattr(mod, "BlockPool"), "BlockPool missing"
    assert hasattr(mod, "compute_block_hash"), "compute_block_hash missing"

