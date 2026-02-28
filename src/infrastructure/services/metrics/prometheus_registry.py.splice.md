# Splice: src/infrastructure/services/metrics/prometheus_registry.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MetricType
- MetricsBackend
- MetricSpec
- MetricValue
- MetricCollector
- Counter
- Gauge
- HistogramBucket
- Histogram
- Summary
- MetricsRegistry
- SampledCounter
- RateLimitedGauge
- VLLMMetrics

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
