# Auto-synced test for infrastructure/storage/cache/kv_cache_manager.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "kv_cache_manager.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "DeviceType"), "DeviceType missing"
    assert hasattr(mod, "DType"), "DType missing"
    assert hasattr(mod, "KVCacheConfig"), "KVCacheConfig missing"
    assert hasattr(mod, "KVCacheBlock"), "KVCacheBlock missing"
    assert hasattr(mod, "KVCacheBlocks"), "KVCacheBlocks missing"
    assert hasattr(mod, "KVCacheAllocator"), "KVCacheAllocator missing"
    assert hasattr(mod, "PagedKVCache"), "PagedKVCache missing"
    assert hasattr(mod, "KVCacheTransfer"), "KVCacheTransfer missing"
    assert hasattr(mod, "KVCacheManager"), "KVCacheManager missing"
    assert hasattr(mod, "create_kv_cache_manager"), "create_kv_cache_manager missing"

