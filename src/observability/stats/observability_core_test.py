# Auto-synced test for observability/stats/observability_core.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "observability_core.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "AlertSeverity"), "AlertSeverity missing"
    assert hasattr(mod, "Alert"), "Alert missing"
    assert hasattr(mod, "Threshold"), "Threshold missing"
    assert hasattr(mod, "RetentionPolicy"), "RetentionPolicy missing"
    assert hasattr(mod, "MetricSnapshot"), "MetricSnapshot missing"
    assert hasattr(mod, "AggregationType"), "AggregationType missing"
    assert hasattr(mod, "MetricNamespace"), "MetricNamespace missing"
    assert hasattr(mod, "MetricAnnotation"), "MetricAnnotation missing"
    assert hasattr(mod, "MetricCorrelation"), "MetricCorrelation missing"
    assert hasattr(mod, "MetricSubscription"), "MetricSubscription missing"
    assert hasattr(mod, "ExportDestination"), "ExportDestination missing"
    assert hasattr(mod, "FederatedSource"), "FederatedSource missing"
    assert hasattr(mod, "FederationMode"), "FederationMode missing"
    assert hasattr(mod, "RollupConfig"), "RollupConfig missing"
    assert hasattr(mod, "StreamingProtocol"), "StreamingProtocol missing"
    assert hasattr(mod, "StreamingConfig"), "StreamingConfig missing"
    assert hasattr(mod, "AgentMetric"), "AgentMetric missing"
    assert hasattr(mod, "ObservabilityCore"), "ObservabilityCore missing"
    assert hasattr(mod, "StatsCore"), "StatsCore missing"
    assert hasattr(mod, "StatsNamespace"), "StatsNamespace missing"
    assert hasattr(mod, "StatsNamespaceManager"), "StatsNamespaceManager missing"
    assert hasattr(mod, "StatsSnapshot"), "StatsSnapshot missing"
    assert hasattr(mod, "StatsSubscription"), "StatsSubscription missing"
    assert hasattr(mod, "ThresholdAlert"), "ThresholdAlert missing"
    assert hasattr(mod, "DerivedMetric"), "DerivedMetric missing"

