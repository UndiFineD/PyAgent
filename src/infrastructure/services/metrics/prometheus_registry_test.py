# Auto-synced test for infrastructure/services/metrics/prometheus_registry.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "prometheus_registry.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MetricType"), "MetricType missing"
    assert hasattr(mod, "MetricsBackend"), "MetricsBackend missing"
    assert hasattr(mod, "MetricSpec"), "MetricSpec missing"
    assert hasattr(mod, "MetricValue"), "MetricValue missing"
    assert hasattr(mod, "MetricCollector"), "MetricCollector missing"
    assert hasattr(mod, "Counter"), "Counter missing"
    assert hasattr(mod, "Gauge"), "Gauge missing"
    assert hasattr(mod, "HistogramBucket"), "HistogramBucket missing"
    assert hasattr(mod, "Histogram"), "Histogram missing"
    assert hasattr(mod, "Summary"), "Summary missing"
    assert hasattr(mod, "MetricsRegistry"), "MetricsRegistry missing"
    assert hasattr(mod, "SampledCounter"), "SampledCounter missing"
    assert hasattr(mod, "RateLimitedGauge"), "RateLimitedGauge missing"
    assert hasattr(mod, "VLLMMetrics"), "VLLMMetrics missing"
    assert hasattr(mod, "get_metrics"), "get_metrics missing"

