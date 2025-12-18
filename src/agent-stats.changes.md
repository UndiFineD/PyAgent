# Changelog

## [2025-12-18] - Documentation refresh

- Refreshed module docstring and companion `agent-stats.*.md` documentation.
- Updated `agent-stats.description.md` with the current SHA256 fingerprint.

## [2025-01-16] - Session 7 Implementation

### Added Enums

- `StreamingProtocol`: WEBSOCKET, SSE, GRPC, MQTT for real-time streaming
- `ExportDestination`: DATADOG, PROMETHEUS, GRAFANA, CLOUDWATCH, STACKDRIVER
- `AggregationType`: SUM, AVG, MIN, MAX, COUNT, P50, P95, P99 for rollups
- `FederationMode`: PULL, PUSH, HYBRID for multi-repo aggregation

### Added Dataclasses

- `StreamingConfig`: Configuration for real-time stats streaming
- `MetricNamespace`: Namespace for organizing metrics hierarchically
- `MetricAnnotation`: Annotation or comment on a metric
- `MetricSubscription`: Subscription for metric change notifications
- `ABComparison`: A/B comparison between code versions
- `MetricCorrelation`: Correlation between two metrics
- `DerivedMetric`: A derived metric from dependencies with formula
- `RollupConfig`: Configuration for metric rollups
- `FederatedSource`: Source repository for stats federation
- `APIEndpoint`: Stats API endpoint configuration

### Added Helper Classes

- `StatsStreamer`: Real-time stats streaming via WebSocket for live dashboards
- `StatsFederation`: Aggregate stats from multiple repositories
- `MetricNamespaceManager`: Manage metric namespaces for organizing large metric sets
- `AnnotationManager`: Manage metric annotations and comments
- `SubscriptionManager`: Manage metric subscriptions and change notifications
- `CloudExporter`: Export stats to cloud monitoring services (Datadog, Prometheus, Grafana)
- `ABComparisonEngine`: Compare stats between different code versions (A/B testing)
- `CorrelationAnalyzer`: Analyze correlations between metrics
- `DerivedMetricCalculator`: Calculate derived metrics from dependencies
- `StatsRollup`: Aggregate metrics into rollup views
- `StatsAPIServer`: Stats API endpoint for programmatic access

## [2025-12-18] - Session 6 Implementation

### Added Enums (Session 6)

- `MetricType` enum: COUNTER, GAUGE, HISTOGRAM, SUMMARY
- `AlertSeverity` enum: CRITICAL, HIGH, MEDIUM, LOW, INFO

### Added Dataclasses (Session 6)

- `Metric`: Custom metric definition with name, metric_type, description, unit, tags
- `MetricSnapshot`: Point-in-time metric snapshot with name, timestamp, metrics
- `Threshold`: Alert threshold with metric_name, min_value, max_value, severity, message
- `Alert`: Alert record with id, metric_name, severity, message, value, threshold, timestamp, acknowledged
- `RetentionPolicy`: Data retention policy with metric_name, max_age_days, max_points, aggregation

### Added Methods

- `register_custom_metric()`: Register custom metric with type
- `get_metric()`, `add_metric()`, `get_metric_history()`: Metric management
- `collect_custom_metrics()`: Collect all custom metrics
- `detect_anomaly()`: Statistical anomaly detection using z-score
- `add_threshold()`, `_check_thresholds()`, `_create_alert()`: Threshold system
- `get_alerts()`, `clear_alerts()`: Alert management
- `create_snapshot()`, `get_snapshot()`, `compare_snapshots()`: Snapshot system
- `add_retention_policy()`, `apply_retention_policies()`: Retention policies
- `forecast()`: Time-series forecasting using linear regression
- `compress_metrics()`, `decompress_metrics()`: Data compression using zlib

### Added Flag

- `HAS_MATPLOTLIB`: Optional matplotlib import flag for visualization

## [Initial]

- Initial version of agent-stats.py
- 2025-12-15: No functional changes in this iteration; documentation and test coverage refreshed.

## [2025-12-16]

- Add support for exporting stats to CSV. (Fixed)
- Add logging for all major actions. (Fixed)
- Add type hints for all methods. (Fixed)
- Add trend analysis: compare with previous run, show delta/percentage change. (Fixed)
- Visualize stats using CLI graphs: ASCII bars, sparklines, or rich tables. (Fixed)
- Track code coverage metrics if available from coverage tools. (Fixed)
- Add docstrings for all methods following Google style format. (Fixed)
- Add unit tests for edge cases (empty files, missing data, malformed input). (Fixed)
- Use `pathlib` consistently throughout (replace str paths). (Fixed)
- Export to additional formats: JSON, HTML, Excel, SQLite. (Fixed)
- Add time-series storage: persist stats history for trend tracking. (Fixed)
- Implement stat aggregation: by file, by agent, by date. (Fixed)
- Generate statistical summaries: mean, median, stddev for metrics. (Fixed)
- Add filtering: by file pattern, agent type, date range. (Fixed)
- Create comparison reports: current vs baseline, current vs previous. (Fixed)
- Add visualization generation: charts, heatmaps, dashboards. (Fixed)
- Implement alerting: notify when metrics cross thresholds. (Fixed)
- Add benchmarking: track agent performance metrics (time, memory, API calls). (Fixed)
- Generate reports with actionable insights and recommendations. (Fixed)
- Support custom metric plugins for extensibility. (Fixed)
- Add stat validation: detect anomalies, validate data integrity. (Fixed)
- Implement caching for performance on large codebases. (Fixed)
- Generate comparative analysis across team members or branches. (Fixed)

## [2025-12-15]

- Added support for exporting stats to CSV format (`--format csv`).
- Added detailed logging for stats reporting.
- Added explicit type hints to `__init__` and `report_stats`.
- Add `--help` examples and validate CLI args (paths, required files). (Fixed)
- Function `__init__` is missing type annotations. (Fixed)
- Function `fmt` is missing type annotations. (Fixed)
- Function `main` is missing type annotations. (Fixed)
- Function `report_stats` is missing type annotations. (Fixed)
