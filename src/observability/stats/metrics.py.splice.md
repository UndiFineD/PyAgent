# Splice: src/observability/stats/metrics.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MetricType
- Metric
- AgentMetric
- MetricSnapshot
- AggregationType
- AggregationResult
- MetricNamespace
- MetricAnnotation
- MetricCorrelation
- MetricSubscription
- StatsNamespace
- StatsSnapshot
- StatsSubscription
- DerivedMetric
- RetentionPolicy
- ABComparisonResult
- ABSignificanceResult

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
