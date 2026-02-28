# Auto-synced test for infrastructure/engine/iteration_metrics.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "iteration_metrics.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MetricType"), "MetricType missing"
    assert hasattr(mod, "BaseCacheStats"), "BaseCacheStats missing"
    assert hasattr(mod, "PrefixCacheStats"), "PrefixCacheStats missing"
    assert hasattr(mod, "MultiModalCacheStats"), "MultiModalCacheStats missing"
    assert hasattr(mod, "KVCacheEvictionEvent"), "KVCacheEvictionEvent missing"
    assert hasattr(mod, "CachingMetrics"), "CachingMetrics missing"
    assert hasattr(mod, "RequestStateStats"), "RequestStateStats missing"
    assert hasattr(mod, "FinishedRequestStats"), "FinishedRequestStats missing"
    assert hasattr(mod, "SchedulerStats"), "SchedulerStats missing"
    assert hasattr(mod, "IterationStats"), "IterationStats missing"
    assert hasattr(mod, "PercentileTracker"), "PercentileTracker missing"
    assert hasattr(mod, "TrendAnalyzer"), "TrendAnalyzer missing"
    assert hasattr(mod, "AnomalyDetector"), "AnomalyDetector missing"
    assert hasattr(mod, "MetricsCollector"), "MetricsCollector missing"

