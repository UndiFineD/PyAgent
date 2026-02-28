# Auto-synced test for infrastructure/storage/cache/kv_cache_metrics.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "kv_cache_metrics.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MetricType"), "MetricType missing"
    assert hasattr(mod, "AlertLevel"), "AlertLevel missing"
    assert hasattr(mod, "MetricsConfig"), "MetricsConfig missing"
    assert hasattr(mod, "BlockMetricsState"), "BlockMetricsState missing"
    assert hasattr(mod, "KVCacheEvictionEvent"), "KVCacheEvictionEvent missing"
    assert hasattr(mod, "CacheAlert"), "CacheAlert missing"
    assert hasattr(mod, "CacheMetricsSummary"), "CacheMetricsSummary missing"
    assert hasattr(mod, "KVCacheMetricsCollector"), "KVCacheMetricsCollector missing"
    assert hasattr(mod, "BatchMetricsCollector"), "BatchMetricsCollector missing"
    assert hasattr(mod, "create_metrics_collector"), "create_metrics_collector missing"

