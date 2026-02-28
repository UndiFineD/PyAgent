# Auto-synced test for infrastructure/engine/kv_cache_coordinator.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "kv_cache_coordinator.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AllocationStrategy"), "AllocationStrategy missing"
    assert hasattr(mod, "AsyncPrefetchCoordinator"), "AsyncPrefetchCoordinator missing"
    assert hasattr(mod, "BlockHash"), "BlockHash missing"
    assert hasattr(mod, "BlockHashCache"), "BlockHashCache missing"
    assert hasattr(mod, "BlockHashWithGroupId"), "BlockHashWithGroupId missing"
    assert hasattr(mod, "BlockPool"), "BlockPool missing"
    assert hasattr(mod, "CacheConfig"), "CacheConfig missing"
    assert hasattr(mod, "CacheGroupSpec"), "CacheGroupSpec missing"
    assert hasattr(mod, "CacheGroupType"), "CacheGroupType missing"
    assert hasattr(mod, "CrossAttentionManager"), "CrossAttentionManager missing"
    assert hasattr(mod, "EvictionPolicy"), "EvictionPolicy missing"
    assert hasattr(mod, "FreeBlockQueue"), "FreeBlockQueue missing"
    assert hasattr(mod, "FullAttentionManager"), "FullAttentionManager missing"
    assert hasattr(mod, "HierarchicalKVCacheCoordinator"), "HierarchicalKVCacheCoordinator missing"
    assert hasattr(mod, "KVCacheBlock"), "KVCacheBlock missing"
    assert hasattr(mod, "KVCacheBlocks"), "KVCacheBlocks missing"
    assert hasattr(mod, "KVCacheCoordinator"), "KVCacheCoordinator missing"
    assert hasattr(mod, "PackKVManager"), "PackKVManager missing"
    assert hasattr(mod, "PredictiveKVCacheCoordinator"), "PredictiveKVCacheCoordinator missing"
    assert hasattr(mod, "SingleTypeKVCacheManager"), "SingleTypeKVCacheManager missing"
    assert hasattr(mod, "SlidingWindowManager"), "SlidingWindowManager missing"
    assert hasattr(mod, "create_kv_cache_coordinator"), "create_kv_cache_coordinator missing"

