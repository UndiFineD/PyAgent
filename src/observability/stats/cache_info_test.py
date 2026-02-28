# Auto-synced test for observability/stats/cache_info.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "cache_info.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CacheStats"), "CacheStats missing"
    assert hasattr(mod, "CacheEntry"), "CacheEntry missing"
    assert hasattr(mod, "LRUCache"), "LRUCache missing"
    assert hasattr(mod, "TTLLRUCache"), "TTLLRUCache missing"

