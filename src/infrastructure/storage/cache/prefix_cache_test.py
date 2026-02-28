# Auto-synced test for infrastructure/storage/cache/prefix_cache.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "prefix_cache.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "EvictionPolicy"), "EvictionPolicy missing"
    assert hasattr(mod, "PrefixCacheConfig"), "PrefixCacheConfig missing"
    assert hasattr(mod, "CacheBlock"), "CacheBlock missing"
    assert hasattr(mod, "PrefixCacheStats"), "PrefixCacheStats missing"
    assert hasattr(mod, "compute_block_hash"), "compute_block_hash missing"
    assert hasattr(mod, "PrefixCacheManager"), "PrefixCacheManager missing"
    assert hasattr(mod, "BlockHasher"), "BlockHasher missing"
    assert hasattr(mod, "create_prefix_cache"), "create_prefix_cache missing"
    assert hasattr(mod, "get_request_block_hasher"), "get_request_block_hasher missing"

