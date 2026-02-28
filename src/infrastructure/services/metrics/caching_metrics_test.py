# Auto-synced test for infrastructure/services/metrics/caching_metrics.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "caching_metrics.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "CacheType"), "CacheType missing"
    assert hasattr(mod, "EvictionReason"), "EvictionReason missing"
    assert hasattr(mod, "CacheEvent"), "CacheEvent missing"
    assert hasattr(mod, "EvictionEvent"), "EvictionEvent missing"
    assert hasattr(mod, "CacheStats"), "CacheStats missing"
    assert hasattr(mod, "SlidingWindowStats"), "SlidingWindowStats missing"
    assert hasattr(mod, "SlidingWindowMetrics"), "SlidingWindowMetrics missing"
    assert hasattr(mod, "CachingMetrics"), "CachingMetrics missing"
    assert hasattr(mod, "PrefixCacheStats"), "PrefixCacheStats missing"
    assert hasattr(mod, "MultiLevelCacheMetrics"), "MultiLevelCacheMetrics missing"
    assert hasattr(mod, "observe_with_rust"), "observe_with_rust missing"

