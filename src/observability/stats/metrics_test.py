# Auto-synced test for observability/stats/metrics.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "metrics.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MetricType"), "MetricType missing"
    assert hasattr(mod, "Metric"), "Metric missing"
    assert hasattr(mod, "AgentMetric"), "AgentMetric missing"
    assert hasattr(mod, "MetricSnapshot"), "MetricSnapshot missing"
    assert hasattr(mod, "AggregationType"), "AggregationType missing"
    assert hasattr(mod, "AggregationResult"), "AggregationResult missing"
    assert hasattr(mod, "MetricNamespace"), "MetricNamespace missing"
    assert hasattr(mod, "MetricAnnotation"), "MetricAnnotation missing"
    assert hasattr(mod, "MetricCorrelation"), "MetricCorrelation missing"
    assert hasattr(mod, "MetricSubscription"), "MetricSubscription missing"
    assert hasattr(mod, "StatsNamespace"), "StatsNamespace missing"
    assert hasattr(mod, "StatsSnapshot"), "StatsSnapshot missing"
    assert hasattr(mod, "StatsSubscription"), "StatsSubscription missing"
    assert hasattr(mod, "DerivedMetric"), "DerivedMetric missing"
    assert hasattr(mod, "RetentionPolicy"), "RetentionPolicy missing"
    assert hasattr(mod, "ABComparisonResult"), "ABComparisonResult missing"
    assert hasattr(mod, "ABSignificanceResult"), "ABSignificanceResult missing"

