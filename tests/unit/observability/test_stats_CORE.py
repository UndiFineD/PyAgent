# -*- coding: utf-8 -*-
"""Test classes for stats enums and dataclasses - CORE module."""

from __future__ import annotations
from typing import Any, List


class TestMetricType:
    """Tests for MetricType enum."""

    def test_metric_type_values(self, stats_module: Any) -> None:
        """Test that metric type values are correct."""
        assert stats_module.MetricType.COUNTER.value == "counter"
        assert stats_module.MetricType.GAUGE.value == "gauge"
        assert stats_module.MetricType.HISTOGRAM.value == "histogram"
        assert stats_module.MetricType.SUMMARY.value == "summary"

    def test_all_metric_types_exist(self, stats_module: Any) -> None:
        """Test all metric types exist."""
        types: List[Any] = list(stats_module.MetricType)
        assert len(types) == 4


class TestAlertSeverity:
    """Tests for AlertSeverity enum."""

    def test_severity_values(self, stats_module: Any) -> None:
        """Test that severity values are correct."""
        assert stats_module.AlertSeverity.CRITICAL.value == 5
        assert stats_module.AlertSeverity.HIGH.value == 4
        assert stats_module.AlertSeverity.MEDIUM.value == 3
        assert stats_module.AlertSeverity.LOW.value == 2
        assert stats_module.AlertSeverity.INFO.value == 1


class TestSession7Enums:
    """Tests for Session 7 enums."""

    def test_streaming_protocol_enum(self, stats_module: Any) -> None:
        """Test StreamingProtocol enum values."""
        assert stats_module.StreamingProtocol.WEBSOCKET.value == "websocket"
        assert stats_module.StreamingProtocol.SSE.value == "server_sent_events"
        assert stats_module.StreamingProtocol.GRPC.value == "grpc"
        assert stats_module.StreamingProtocol.MQTT.value == "mqtt"

    def test_export_destination_enum(self, stats_module: Any) -> None:
        """Test ExportDestination enum values."""
        assert stats_module.ExportDestination.DATADOG.value == "datadog"
        assert stats_module.ExportDestination.PROMETHEUS.value == "prometheus"
        assert stats_module.ExportDestination.GRAFANA.value == "grafana"
        assert stats_module.ExportDestination.CLOUDWATCH.value == "cloudwatch"

    def test_aggregation_type_enum(self, stats_module: Any) -> None:
        """Test AggregationType enum values."""
        assert stats_module.AggregationType.SUM.value == "sum"
        assert stats_module.AggregationType.AVG.value == "average"
        assert stats_module.AggregationType.P95.value == "percentile_95"

    def test_federation_mode_enum(self, stats_module: Any) -> None:
        """Test FederationMode enum values."""
        assert stats_module.FederationMode.PULL.value == "pull"
        assert stats_module.FederationMode.PUSH.value == "push"
        assert stats_module.FederationMode.HYBRID.value == "hybrid"


class TestSession7Dataclasses:
    """Tests for Session 7 dataclasses."""

    def test_streaming_config_dataclass(self, stats_module: Any) -> None:
        """Test StreamingConfig dataclass."""
        config = stats_module.StreamingConfig(
            protocol=stats_module.StreamingProtocol.WEBSOCKET, endpoint="ws://localhost"
        )
        assert config.port == 8080
        assert config.buffer_size == 1000

    def test_metric_namespace_dataclass(self, stats_module: Any) -> None:
        """Test MetricNamespace dataclass."""
        ns = stats_module.MetricNamespace(name="cpu", description="CPU metrics")
        assert ns.retention_days == 30
        assert ns.parent is None

    def test_metric_annotation_dataclass(self, stats_module: Any) -> None:
        """Test MetricAnnotation dataclass."""
        ann = stats_module.MetricAnnotation(
            metric_name="cpu.usage",
            timestamp="2025-01-01T00:00:00",
            text="High usage noted",
        )
        assert ann.annotation_type == "info"

    def test_metric_subscription_dataclass(self, stats_module: Any) -> None:
        """Test MetricSubscription dataclass."""
        sub = stats_module.MetricSubscription(id="sub1", metric_pattern="cpu.*")
        assert "threshold" in sub.notify_on
        assert sub.min_interval_seconds == 60

    def test_ab_comparison_dataclass(self, stats_module: Any) -> None:
        """Test ABComparison dataclass."""
        comp = stats_module.ABComparison(id="ab1", version_a="v1.0", version_b="v2.0")
        assert comp.winner == ""
        assert comp.confidence == 0.0

    def test_metric_correlation_dataclass(self, stats_module: Any) -> None:
        """Test MetricCorrelation dataclass."""
        corr = stats_module.MetricCorrelation(
            metric_a="cpu",
            metric_b="data/memory",
            correlation_coefficient=0.85,
            sample_size=100,
        )
        assert corr.significance == 0.0

    def test_derived_metric_dataclass(self, stats_module: Any) -> None:
        """Test DerivedMetric dataclass."""
        derived = stats_module.DerivedMetric(
            name="cpu_ratio",
            dependencies=["cpu_used", "cpu_total"],
            formula="{cpu_used} / {cpu_total} * 100",
        )
        assert derived.description == ""

    def test_rollup_config_dataclass(self, stats_module: Any) -> None:
        """Test RollupConfig dataclass."""
        config = stats_module.RollupConfig(
            name="hourly_cpu",
            source_metrics=["cpu.usage"],
            aggregation=stats_module.AggregationType.AVG,
        )
        assert config.interval_minutes == 60
        assert config.keep_raw is True

    def test_federated_source_dataclass(self, stats_module: Any) -> None:
        """Test FederatedSource dataclass."""
        source = stats_module.FederatedSource(
            repo_url="https://github.com/test/repo", api_endpoint="https://api.test.com"
        )
        assert source.enabled is True
        assert source.poll_interval_seconds == 300

    def test_api_endpoint_dataclass(self, stats_module: Any) -> None:
        """Test APIEndpoint dataclass."""
        endpoint = stats_module.APIEndpoint(path="/api/stats")
        assert endpoint.method == "GET"
        assert endpoint.rate_limit == 100


class TestRetentionPolicyCreation:
    """Tests for retention policy creation."""

    def test_retention_policy_creation(self, stats_module: Any) -> None:
        """Test retention policy creation."""
        RetentionPolicy = stats_module.RetentionPolicy

        policy = RetentionPolicy(name="short_term", retention_days=7, resolution="1m")

        assert policy.retention_days == 7


class TestNamespaceCreation:
    """Tests for namespace creation."""

    def test_namespace_creation(self, stats_module: Any) -> None:
        """Test namespace creation."""
        StatsNamespace = stats_module.StatsNamespace

        ns = StatsNamespace("production")
        assert ns.name == "production"
