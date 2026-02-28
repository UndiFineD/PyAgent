# Auto-synced test for infrastructure/storage/cache/prefix_cache_optimizer.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "prefix_cache_optimizer.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CacheTier"), "CacheTier missing"
    assert hasattr(mod, "PrefixCacheConfig"), "PrefixCacheConfig missing"
    assert hasattr(mod, "PrefixEntry"), "PrefixEntry missing"
    assert hasattr(mod, "CacheHitResult"), "CacheHitResult missing"
    assert hasattr(mod, "RadixTreeNode"), "RadixTreeNode missing"
    assert hasattr(mod, "PrefixTree"), "PrefixTree missing"
    assert hasattr(mod, "PrefixCacheOptimizer"), "PrefixCacheOptimizer missing"

