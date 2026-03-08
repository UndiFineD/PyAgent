# Splice: src/observability/stats/observability_core.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- AlertSeverity
- Alert
- Threshold
- RetentionPolicy
- MetricSnapshot
- AggregationType
- MetricNamespace
- MetricAnnotation
- MetricCorrelation
- MetricSubscription
- ExportDestination
- FederatedSource
- FederationMode
- RollupConfig
- StreamingProtocol
- StreamingConfig
- AgentMetric
- ObservabilityCore
- StatsCore
- StatsNamespace
- StatsNamespaceManager
- StatsSnapshot
- StatsSubscription
- ThresholdAlert
- DerivedMetric

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
