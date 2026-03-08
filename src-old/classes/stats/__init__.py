from __future__ import annotations

"""Auto-generated module exports.

Prefer the observability implementation where available; fall back to
the local auto-generated shims when needed.
"""


try:
    # Import the observability stats module but only copy attributes
    # that can be accessed without raising (skip heavy deps).
    from importlib import import_module

    _obs = import_module("src.observability.stats")
    _names = [
        "ABComparator",
        "ABComparison",
        "ABComparisonEngine",
        "ABComparisonResult",
        "ABSignificanceResult",
        "APIEndpoint",
        "AggregationType",
        "Alert",
        "AlertSeverity",
        "AnnotationManager",
        "CloudExporter",
        "CorrelationAnalyzer",
        "DerivedMetric",
        "DerivedMetricCalculator",
        "ExportDestination",
        "FederatedSource",
        "FederationMode",
        "FormulaEngine",
        "FormulaValidation",
        "Metric",
        "MetricAnnotation",
        "MetricCorrelation",
        "MetricNamespace",
        "MetricNamespaceManager",
        "MetricSnapshot",
        "MetricSubscription",
        "MetricType",
        "RetentionEnforcer",
        "RetentionPolicy",
        "RollupConfig",
        "StatsAPIServer",
        "StatsAccessController",
        "StatsAgent",
        "StatsAnnotationManager",
        "StatsBackup",
        "StatsBackupManager",
        "StatsChangeDetector",
        "StatsCompressor",
        "StatsExporter",
        "StatsFederation",
        "StatsForecaster",
        "StatsNamespace",
        "StatsNamespaceManager",
        "StatsQueryEngine",
        "StatsRollup",
        "StatsRollupCalculator",
        "StatsSnapshot",
        "StatsSnapshotManager",
        "StatsStream",
        "StatsStreamManager",
        "StatsStreamer",
        "StatsSubscription",
        "StatsSubscriptionManager",
        "StreamingConfig",
        "StreamingProtocol",
        "SubscriptionManager",
        "Threshold",
        "ThresholdAlert",
        "ThresholdAlertManager",
    ]

    _loaded = False
    for _n in _names:
        try:
            _val = getattr(_obs, _n)
        except Exception:
            continue
        globals()[_n] = _val
        _loaded = True

    if _loaded:
        __all__ = [n for n in _names if n in globals()]
    else:
        raise ImportError("no observability stats names available")
except Exception:
    # Observability stats package not available; provide a minimal fallback namespace
    # to avoid import-time failures during test collection. Tests depending on full
    # observability implementations should enable the optional package.
    __all__ = []
