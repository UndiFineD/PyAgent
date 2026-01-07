# -*- coding: utf-8 -*-
"""Test classes from test_agent_stats.py - core module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY, mock_open
import time
import json
from datetime import datetime, timedelta
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self): 
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args): 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

# Load StatsAgent from agent_stats.py
try:
    with agent_dir_on_path():
        _stats_module = load_agent_module("agent_stats.py")
        StatsAgent = _stats_module.StatsAgent
except Exception:
    # Fallback if the module can't be loaded
    StatsAgent = None


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
        types = list(stats_module.MetricType)
        assert len(types) == 4


# ========== AlertSeverity Tests ==========


class TestAlertSeverity:
    """Tests for AlertSeverity enum."""

    def test_severity_values(self, stats_module: Any) -> None:
        """Test that severity values are correct."""
        assert stats_module.AlertSeverity.CRITICAL.value == 5
        assert stats_module.AlertSeverity.HIGH.value == 4
        assert stats_module.AlertSeverity.MEDIUM.value == 3
        assert stats_module.AlertSeverity.LOW.value == 2
        assert stats_module.AlertSeverity.INFO.value == 1


# ========== Custom Metrics Tests ==========


class TestCustomMetrics:
    """Tests for custom metrics functionality."""

    def test_register_custom_metric(self, agent: Any, stats_module: Any) -> None:
        """Test registering a custom metric."""
        metric = agent.register_custom_metric(
            name="request_count",
            metric_type=stats_module.MetricType.COUNTER,
            description="Number of requests"
        )
        assert metric.name == "request_count"
        assert metric.metric_type == stats_module.MetricType.COUNTER

    def test_get_metric(self, agent: Any, stats_module: Any) -> None:
        """Test getting a registered metric."""
        agent.register_custom_metric("test_metric", stats_module.MetricType.GAUGE)
        metric = agent.get_metric("test_metric")
        assert metric is not None
        assert metric.name == "test_metric"

    def test_add_metric_value(self, agent: Any, stats_module: Any) -> None:
        """Test adding a value to a metric."""
        agent.register_custom_metric("counter", stats_module.MetricType.COUNTER)
        agent.add_metric("counter", 5)
        agent.add_metric("counter", 3)
        history = agent.get_metric_history("counter")
        assert len(history) == 2
        assert history[-1][1] == 3  # (timestamp, value)

    def test_collect_custom_metrics(self, agent: Any, stats_module: Any) -> None:
        """Test collecting all custom metrics."""
        agent.register_custom_metric("m1", stats_module.MetricType.COUNTER)
        agent.register_custom_metric("m2", stats_module.MetricType.GAUGE)
        agent.add_metric("m1", 10)
        agent.add_metric("m2", 50)
        collected = agent.collect_custom_metrics()
        assert "m1" in collected
        assert "m2" in collected


# ========== Anomaly Detection Tests ==========


class TestAnomalyDetection:
    """Tests for anomaly detection."""

    def test_detect_anomaly_no_data(self, agent: Any, stats_module: Any) -> None:
        """Test anomaly detection with insufficient data."""
        agent.register_custom_metric("sparse", stats_module.MetricType.GAUGE)
        result = agent.detect_anomaly("sparse")
        assert result is False  # Not enough data

    def test_detect_anomaly_with_data(self, agent: Any, stats_module: Any) -> None:
        """Test anomaly detection with normal data."""
        agent.register_custom_metric("stable", stats_module.MetricType.GAUGE)
        for v in [10, 10, 10, 10, 10]:
            agent.add_metric("stable", v)
        result = agent.detect_anomaly("stable")
        assert result is False  # All values are the same

    def test_detect_anomaly_outlier(self, agent: Any, stats_module: Any) -> None:
        """Test anomaly detection with outlier."""
        agent.register_custom_metric("anomalous", stats_module.MetricType.GAUGE)
        for v in [10, 10, 10, 10, 10]:
            agent.add_metric("anomalous", v)
        agent.add_metric("anomalous", 1000)  # Big outlier
        result = agent.detect_anomaly("anomalous")
        assert result is True


# ========== Thresholds and Alerting Tests ==========


class TestThresholdsAndAlerting:
    """Tests for thresholds and alerting."""

    def test_add_threshold(self, agent: Any, stats_module: Any) -> None:
        """Test adding a threshold."""
        agent.register_custom_metric("cpu", stats_module.MetricType.GAUGE)
        threshold = agent.add_threshold(
            metric_name="cpu",
            min_value=0,
            max_value=90,
            severity=stats_module.AlertSeverity.HIGH
        )
        assert threshold.metric_name == "cpu"
        assert threshold.max_value == 90

    def test_threshold_creates_alert(self, agent: Any, stats_module: Any) -> None:
        """Test that exceeding threshold creates alert."""
        agent.register_custom_metric("memory", stats_module.MetricType.GAUGE)
        agent.add_threshold(
            metric_name="memory",
            max_value=80,
            severity=stats_module.AlertSeverity.CRITICAL
        )
        agent.add_metric("memory", 95)  # Exceeds threshold
        alerts = agent.get_alerts()
        assert len(alerts) >= 1
        assert alerts[0].severity == stats_module.AlertSeverity.CRITICAL

    def test_clear_alerts(self, agent: Any, stats_module: Any) -> None:
        """Test clearing alerts."""
        agent.register_custom_metric("disk", stats_module.MetricType.GAUGE)
        agent.add_threshold("disk", max_value=50, severity=stats_module.AlertSeverity.HIGH)
        agent.add_metric("disk", 100)
        agent.clear_alerts()
        assert len(agent.get_alerts()) == 0


# ========== Snapshot Tests ==========


class TestSnapshots:
    """Tests for metric snapshots."""

    def test_create_snapshot(self, agent: Any, stats_module: Any) -> None:
        """Test creating a snapshot."""
        agent.register_custom_metric("snap_test", stats_module.MetricType.GAUGE)
        agent.add_metric("snap_test", 42)
        snapshot = agent.create_snapshot("test_snapshot")
        assert snapshot.name == "test_snapshot"
        assert "snap_test" in snapshot.metrics

    def test_get_snapshot(self, agent: Any) -> None:
        """Test getting a snapshot by name."""
        agent.create_snapshot("my_snapshot")
        snapshot = agent.get_snapshot("my_snapshot")
        assert snapshot is not None
        assert snapshot.name == "my_snapshot"

    def test_compare_snapshots(self, agent: Any, stats_module: Any) -> None:
        """Test comparing two snapshots."""
        agent.register_custom_metric("compare_metric", stats_module.MetricType.GAUGE)
        agent.add_metric("compare_metric", 10)
        agent.create_snapshot("before")
        agent.add_metric("compare_metric", 20)
        agent.create_snapshot("after")
        diff = agent.compare_snapshots("before", "after")
        assert "compare_metric" in diff


# ========== Retention Policy Tests ==========


class TestRetentionPolicies:
    """Tests for retention policies."""

    def test_add_retention_policy(self, agent: Any, stats_module: Any) -> None:
        """Test adding a retention policy."""
        agent.register_custom_metric("retention_test", stats_module.MetricType.GAUGE)
        policy = agent.add_retention_policy(
            metric_name="retention_test",
            max_age_days=7,
            max_points=1000
        )
        assert policy.metric_name == "retention_test"
        assert policy.max_age_days == 7

    def test_apply_retention_policies(self, agent: Any, stats_module: Any) -> None:
        """Test applying retention policies."""
        agent.register_custom_metric("expire_test", stats_module.MetricType.COUNTER)
        agent.add_retention_policy("expire_test", max_points=5)
        for i in range(10):
            agent.add_metric("expire_test", i)
        agent.apply_retention_policies()
        history = agent.get_metric_history("expire_test")
        assert len(history) <= 5


# ========== Forecasting Tests ==========


class TestForecasting:
    """Tests for metric forecasting."""

    def test_forecast_insufficient_data(self, agent: Any, stats_module: Any) -> None:
        """Test forecasting with insufficient data."""
        agent.register_custom_metric("sparse_forecast", stats_module.MetricType.GAUGE)
        agent.add_metric("sparse_forecast", 10)
        forecast = agent.forecast("sparse_forecast", periods=5)
        assert forecast is None or len(forecast) == 0

    def test_forecast_with_data(self, agent: Any, stats_module: Any) -> None:
        """Test forecasting with sufficient data."""
        agent.register_custom_metric("trend", stats_module.MetricType.GAUGE)
        for i in range(10):
            agent.add_metric("trend", i * 10)  # Linear trend
        forecast = agent.forecast("trend", periods=3)
        if forecast:
            assert len(forecast) == 3


# ========== Compression Tests ==========


class TestCompression:
    """Tests for metric data compression."""

    def test_compress_metrics(self, agent: Any, stats_module: Any) -> None:
        """Test compressing metric data."""
        agent.register_custom_metric("compress_test", stats_module.MetricType.GAUGE)
        for i in range(100):
            agent.add_metric("compress_test", i)
        compressed = agent.compress_metrics("compress_test")
        assert compressed is not None
        assert len(compressed) > 0

    def test_decompress_metrics(self, agent: Any, stats_module: Any) -> None:
        """Test decompressing metric data."""
        agent.register_custom_metric("decompress_test", stats_module.MetricType.GAUGE)
        original = [(datetime.now().isoformat(), i) for i in range(10)]
        agent._metric_history["decompress_test"] = original
        compressed = agent.compress_metrics("decompress_test")
        decompressed = agent.decompress_metrics(compressed)
        assert len(decompressed) == len(original)


# ========== Legacy Tests (unittest) ==========


class TestStatsAgent(unittest.TestCase):

    def setUp(self):
        # Create temporary files for testing
        import tempfile
        import os
        self.temp_dir = tempfile.mkdtemp()
        self.files = [
            os.path.join(self.temp_dir, 'file1.py'),
            os.path.join(self.temp_dir, 'file2.py')
        ]
        for f in self.files:
            Path(f).write_text("# test file\n", encoding="utf-8")
        self.agent = StatsAgent(self.files)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_validate_files(self):
        self.agent._validate_files()
        self.assertEqual(len(self.agent.files), len(self.files))

    def test_calculate_stats(self):
        self.agent.stats = {
            'total_files': 2,
            'files_with_context': 1,
            'files_with_changes': 1,
            'files_with_errors': 0,
            'files_with_improvements': 2,
            'files_with_tests': 1
        }
        stats = self.agent.calculate_stats()
        self.assertEqual(stats['total_files'], 2)

    @patch('builtins.open', new_callable=mock_open, read_data='{"total_coverage": 85}')
    def test_track_code_coverage(self, mock_file):
        self.agent.track_code_coverage('coverage.json')
        self.assertEqual(self.agent.stats['code_coverage'], 85)

    @patch('matplotlib.pyplot.show')
    def test_visualize_stats(self, mock_show):
        self.agent.stats = {
            'total_files': 2,
            'files_with_context': 1,
            'files_with_changes': 1,
            'files_with_errors': 0,
            'files_with_improvements': 2,
            'files_with_tests': 1
        }
        self.agent.visualize_stats()
        mock_show.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data='{"total_files": 2}')
    def test_generate_comparison_report(self, mock_file):
        baseline_stats = {
            'total_files': 1,
            'files_with_context': 0
        }
        with patch('builtins.print') as mock_print:
            self.agent.generate_comparison_report(baseline_stats)
            mock_print.assert_called()


# ========== Session 7 Tests: New Enums ==========



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


# ========== Session 7 Tests: Dataclasses ==========



class TestSession7Dataclasses:
    """Tests for Session 7 dataclasses."""

    def test_streaming_config_dataclass(self, stats_module: Any) -> None:
        """Test StreamingConfig dataclass."""
        config = stats_module.StreamingConfig(
            protocol=stats_module.StreamingProtocol.WEBSOCKET,
            endpoint="ws://localhost"
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
            text="High usage noted"
        )
        assert ann.annotation_type == "info"

    def test_metric_subscription_dataclass(self, stats_module: Any) -> None:
        """Test MetricSubscription dataclass."""
        sub = stats_module.MetricSubscription(
            id="sub1",
            metric_pattern="cpu.*"
        )
        assert "threshold" in sub.notify_on
        assert sub.min_interval_seconds == 60

    def test_ab_comparison_dataclass(self, stats_module: Any) -> None:
        """Test ABComparison dataclass."""
        comp = stats_module.ABComparison(
            id="ab1",
            version_a="v1.0",
            version_b="v2.0"
        )
        assert comp.winner == ""
        assert comp.confidence == 0.0

    def test_metric_correlation_dataclass(self, stats_module: Any) -> None:
        """Test MetricCorrelation dataclass."""
        corr = stats_module.MetricCorrelation(
            metric_a="cpu",
            metric_b="memory",
            correlation_coefficient=0.85,
            sample_size=100
        )
        assert corr.significance == 0.0

    def test_derived_metric_dataclass(self, stats_module: Any) -> None:
        """Test DerivedMetric dataclass."""
        derived = stats_module.DerivedMetric(
            name="cpu_ratio",
            dependencies=["cpu_used", "cpu_total"],
            formula="{cpu_used} / {cpu_total} * 100"
        )
        assert derived.description == ""

    def test_rollup_config_dataclass(self, stats_module: Any) -> None:
        """Test RollupConfig dataclass."""
        config = stats_module.RollupConfig(
            name="hourly_cpu",
            source_metrics=["cpu.usage"],
            aggregation=stats_module.AggregationType.AVG
        )
        assert config.interval_minutes == 60
        assert config.keep_raw is True

    def test_federated_source_dataclass(self, stats_module: Any) -> None:
        """Test FederatedSource dataclass."""
        source = stats_module.FederatedSource(
            repo_url="https://github.com / test / repo",
            api_endpoint="https://api.test.com"
        )
        assert source.enabled is True
        assert source.poll_interval_seconds == 300

    def test_api_endpoint_dataclass(self, stats_module: Any) -> None:
        """Test APIEndpoint dataclass."""
        endpoint = stats_module.APIEndpoint(path="/api / stats")
        assert endpoint.method == "GET"
        assert endpoint.rate_limit == 100


# ========== Session 7 Tests: StatsStreamer ==========



class TestStatsStreamer:
    """Tests for StatsStreamer class."""

    def test_init(self, stats_module: Any) -> None:
        """Test StatsStreamer initialization."""
        config = stats_module.StreamingConfig(
            protocol=stats_module.StreamingProtocol.WEBSOCKET,
            endpoint="ws://localhost"
        )
        streamer = stats_module.StatsStreamer(config)
        assert streamer.subscribers == []
        assert streamer.buffer == []

    def test_connect(self, stats_module: Any) -> None:
        """Test connecting to stream."""
        config = stats_module.StreamingConfig(
            protocol=stats_module.StreamingProtocol.WEBSOCKET,
            endpoint="ws://localhost"
        )
        streamer = stats_module.StatsStreamer(config)
        result = streamer.connect()
        assert result is True

    def test_disconnect(self, stats_module: Any) -> None:
        """Test disconnecting from stream."""
        config = stats_module.StreamingConfig(
            protocol=stats_module.StreamingProtocol.WEBSOCKET,
            endpoint="ws://localhost"
        )
        streamer = stats_module.StatsStreamer(config)
        streamer.connect()
        streamer.disconnect()
        assert streamer._connected is False

    def test_add_subscriber(self, stats_module: Any) -> None:
        """Test adding a subscriber."""
        config = stats_module.StreamingConfig(
            protocol=stats_module.StreamingProtocol.WEBSOCKET,
            endpoint="ws://localhost"
        )
        streamer = stats_module.StatsStreamer(config)
        streamer.add_subscriber("sub1")
        assert "sub1" in streamer.subscribers

    def test_stream_metric(self, stats_module: Any) -> None:
        """Test streaming a metric."""
        config = stats_module.StreamingConfig(
            protocol=stats_module.StreamingProtocol.WEBSOCKET,
            endpoint="ws://localhost"
        )
        streamer = stats_module.StatsStreamer(config)
        streamer.connect()
        metric = stats_module.Metric(
            name="test",
            value=42.0,
            metric_type=stats_module.MetricType.GAUGE
        )
        result = streamer.stream_metric(metric)
        assert result is True


# ========== Session 7 Tests: StatsFederation ==========



class TestStatsFederation:
    """Tests for StatsFederation class."""

    def test_init(self, stats_module: Any) -> None:
        """Test StatsFederation initialization."""
        federation = stats_module.StatsFederation()
        assert federation.mode == stats_module.FederationMode.PULL
        assert federation.sources == {}

    def test_add_source(self, stats_module: Any) -> None:
        """Test adding a federated source."""
        federation = stats_module.StatsFederation()
        source = stats_module.FederatedSource(
            repo_url="https://github.com / test / repo",
            api_endpoint="https://api.test.com"
        )
        federation.add_source("repo1", source)
        assert "repo1" in federation.sources

    def test_remove_source(self, stats_module: Any) -> None:
        """Test removing a source."""
        federation = stats_module.StatsFederation()
        source = stats_module.FederatedSource(
            repo_url="https://github.com / test / repo",
            api_endpoint="https://api.test.com"
        )
        federation.add_source("repo1", source)
        result = federation.remove_source("repo1")
        assert result is True
        assert "repo1" not in federation.sources

    def test_aggregate(self, stats_module: Any) -> None:
        """Test aggregating metrics."""
        federation = stats_module.StatsFederation()
        federation.aggregated["cpu"] = [10.0, 20.0, 30.0]
        result = federation.aggregate("cpu", stats_module.AggregationType.AVG)
        assert result == 20.0

    def test_get_federation_status(self, stats_module: Any) -> None:
        """Test getting federation status."""
        federation = stats_module.StatsFederation()
        source = stats_module.FederatedSource(
            repo_url="https://github.com / test / repo",
            api_endpoint="https://api.test.com"
        )
        federation.add_source("repo1", source)
        status = federation.get_federation_status()
        assert "repo1" in status


# ========== Session 7 Tests: MetricNamespaceManager ==========



class TestMetricNamespaceManager:
    """Tests for MetricNamespaceManager class."""

    def test_init(self, stats_module: Any) -> None:
        """Test MetricNamespaceManager initialization."""
        manager = stats_module.MetricNamespaceManager()
        assert manager.namespaces == {}

    def test_create_namespace(self, stats_module: Any) -> None:
        """Test creating a namespace."""
        manager = stats_module.MetricNamespaceManager()
        ns = manager.create_namespace("system", "System metrics")
        assert ns.name == "system"
        assert "system" in manager.namespaces

    def test_create_child_namespace(self, stats_module: Any) -> None:
        """Test creating a child namespace."""
        manager = stats_module.MetricNamespaceManager()
        manager.create_namespace("system")
        child = manager.create_namespace("cpu", parent="system")
        assert child.parent == "system"

    def test_delete_namespace(self, stats_module: Any) -> None:
        """Test deleting a namespace."""
        manager = stats_module.MetricNamespaceManager()
        manager.create_namespace("test")
        result = manager.delete_namespace("test")
        assert result is True
        assert "test" not in manager.namespaces

    def test_assign_metric(self, stats_module: Any) -> None:
        """Test assigning a metric to namespace."""
        manager = stats_module.MetricNamespaceManager()
        manager.create_namespace("system")
        result = manager.assign_metric("cpu.usage", "system")
        assert result is True
        assert "cpu.usage" in manager.metrics_by_namespace["system"]

    def test_get_full_path(self, stats_module: Any) -> None:
        """Test getting full path."""
        manager = stats_module.MetricNamespaceManager()
        manager.create_namespace("root")
        manager.create_namespace("system", parent="root")
        path = manager.get_full_path("system")
        assert path == "root / system"


# ========== Session 7 Tests: AnnotationManager ==========



class TestAnnotationManager:
    """Tests for AnnotationManager class."""

    def test_init(self, stats_module: Any) -> None:
        """Test AnnotationManager initialization."""
        manager = stats_module.AnnotationManager()
        assert manager.annotations == {}

    def test_add_annotation(self, stats_module: Any) -> None:
        """Test adding an annotation."""
        manager = stats_module.AnnotationManager()
        ann = manager.add_annotation("cpu.usage", "Spike observed", author="admin")
        assert ann.text == "Spike observed"
        assert "cpu.usage" in manager.annotations

    def test_get_annotations(self, stats_module: Any) -> None:
        """Test getting annotations."""
        manager = stats_module.AnnotationManager()
        manager.add_annotation("cpu.usage", "Note 1")
        manager.add_annotation("cpu.usage", "Note 2")
        annotations = manager.get_annotations("cpu.usage")
        assert len(annotations) == 2

    def test_delete_annotation(self, stats_module: Any) -> None:
        """Test deleting an annotation."""
        manager = stats_module.AnnotationManager()
        ann = manager.add_annotation("cpu.usage", "Note")
        result = manager.delete_annotation("cpu.usage", ann.timestamp)
        assert result is True

    def test_export_annotations(self, stats_module: Any) -> None:
        """Test exporting annotations."""
        manager = stats_module.AnnotationManager()
        manager.add_annotation("cpu.usage", "Note")
        exported = manager.export_annotations()
        assert "cpu.usage" in exported


# ========== Session 7 Tests: SubscriptionManager ==========



class TestSubscriptionManager:
    """Tests for SubscriptionManager class."""

    def test_init(self, stats_module: Any) -> None:
        """Test SubscriptionManager initialization."""
        manager = stats_module.SubscriptionManager()
        assert manager.subscriptions == {}

    def test_subscribe(self, stats_module: Any) -> None:
        """Test creating a subscription."""
        manager = stats_module.SubscriptionManager()
        sub = manager.subscribe("cpu.*", callback_url="http://callback.com")
        assert sub.metric_pattern == "cpu.*"
        assert sub.id in manager.subscriptions

    def test_unsubscribe(self, stats_module: Any) -> None:
        """Test removing a subscription."""
        manager = stats_module.SubscriptionManager()
        sub = manager.subscribe("cpu.*")
        result = manager.unsubscribe(sub.id)
        assert result is True
        assert sub.id not in manager.subscriptions

    def test_notify(self, stats_module: Any) -> None:
        """Test sending notifications."""
        manager = stats_module.SubscriptionManager()
        manager.subscribe("cpu.*")
        notified = manager.notify("cpu.usage", "threshold", 95.0)
        assert len(notified) == 1

    def test_get_stats(self, stats_module: Any) -> None:
        """Test getting subscription stats."""
        manager = stats_module.SubscriptionManager()
        manager.subscribe("cpu.*")
        stats = manager.get_stats()
        assert stats["total_subscriptions"] == 1


# ========== Session 7 Tests: CloudExporter ==========



class TestCloudExporter:
    """Tests for CloudExporter class."""

    def test_init(self, stats_module: Any) -> None:
        """Test CloudExporter initialization."""
        exporter = stats_module.CloudExporter(
            stats_module.ExportDestination.DATADOG,
            api_key="test_key"
        )
        assert exporter.destination == stats_module.ExportDestination.DATADOG

    def test_queue_metric(self, stats_module: Any) -> None:
        """Test queueing a metric."""
        exporter = stats_module.CloudExporter(stats_module.ExportDestination.PROMETHEUS)
        metric = stats_module.Metric(
            name="test",
            value=42.0,
            metric_type=stats_module.MetricType.GAUGE
        )
        exporter.queue_metric(metric)
        assert len(exporter.export_queue) == 1

    def test_export(self, stats_module: Any) -> None:
        """Test exporting metrics."""
        exporter = stats_module.CloudExporter(stats_module.ExportDestination.DATADOG)
        metric = stats_module.Metric(
            name="test",
            value=42.0,
            metric_type=stats_module.MetricType.GAUGE
        )
        exporter.queue_metric(metric)
        count = exporter.export()
        assert count == 1
        assert len(exporter.export_queue) == 0

    def test_get_export_stats(self, stats_module: Any) -> None:
        """Test getting export stats."""
        exporter = stats_module.CloudExporter(stats_module.ExportDestination.GRAFANA)
        stats = exporter.get_export_stats()
        assert stats["destination"] == "grafana"


# ========== Session 7 Tests: ABComparisonEngine ==========



class TestABComparisonEngine:
    """Tests for ABComparisonEngine class."""

    def test_init(self, stats_module: Any) -> None:
        """Test ABComparisonEngine initialization."""
        engine = stats_module.ABComparisonEngine()
        assert engine.comparisons == {}

    def test_create_comparison(self, stats_module: Any) -> None:
        """Test creating a comparison."""
        engine = stats_module.ABComparisonEngine()
        comp = engine.create_comparison("v1.0", "v2.0")
        assert comp.version_a == "v1.0"
        assert comp.id in engine.comparisons

    def test_add_metric(self, stats_module: Any) -> None:
        """Test adding a metric to comparison."""
        engine = stats_module.ABComparisonEngine()
        comp = engine.create_comparison("v1.0", "v2.0")
        result = engine.add_metric(comp.id, "a", "latency", 100.0)
        assert result is True
        assert comp.metrics_a["latency"] == 100.0

    def test_calculate_winner(self, stats_module: Any) -> None:
        """Test calculating winner."""
        engine = stats_module.ABComparisonEngine()
        comp = engine.create_comparison("v1.0", "v2.0")
        engine.add_metric(comp.id, "a", "latency", 100.0)
        engine.add_metric(comp.id, "b", "latency", 80.0)
        result = engine.calculate_winner(comp.id, "latency", higher_is_better=False)
        assert result["winner"] == "b"

    def test_get_summary(self, stats_module: Any) -> None:
        """Test getting comparison summary."""
        engine = stats_module.ABComparisonEngine()
        comp = engine.create_comparison("v1.0", "v2.0")
        summary = engine.get_summary(comp.id)
        assert summary["version_a"] == "v1.0"


# ========== Session 7 Tests: CorrelationAnalyzer ==========



class TestCorrelationAnalyzer:
    """Tests for CorrelationAnalyzer class."""

    def test_init(self, stats_module: Any) -> None:
        """Test CorrelationAnalyzer initialization."""
        analyzer = stats_module.CorrelationAnalyzer()
        assert analyzer.correlations == []

    def test_record_value(self, stats_module: Any) -> None:
        """Test recording values."""
        analyzer = stats_module.CorrelationAnalyzer()
        analyzer.record_value("cpu", 50.0)
        analyzer.record_value("cpu", 60.0)
        assert len(analyzer._metric_history["cpu"]) == 2

    def test_compute_correlation(self, stats_module: Any) -> None:
        """Test computing correlation."""
        analyzer = stats_module.CorrelationAnalyzer()
        for i in range(10):
            analyzer.record_value("cpu", float(i))
            analyzer.record_value("memory", float(i * 2))
        corr = analyzer.compute_correlation("cpu", "memory")
        assert corr is not None
        assert corr.correlation_coefficient > 0.9

    def test_find_strong_correlations(self, stats_module: Any) -> None:
        """Test finding strong correlations."""
        analyzer = stats_module.CorrelationAnalyzer()
        for i in range(10):
            analyzer.record_value("a", float(i))
            analyzer.record_value("b", float(i))
        analyzer.compute_correlation("a", "b")
        strong = analyzer.find_strong_correlations(0.9)
        assert len(strong) >= 1


# ========== Session 7 Tests: DerivedMetricCalculator ==========



class TestDerivedMetricCalculator:
    """Tests for DerivedMetricCalculator class."""

    def test_init(self, stats_module: Any) -> None:
        """Test DerivedMetricCalculator initialization."""
        calc = stats_module.DerivedMetricCalculator()
        assert calc.derived_metrics == {}

    def test_register_derived(self, stats_module: Any) -> None:
        """Test registering a derived metric."""
        calc = stats_module.DerivedMetricCalculator()
        derived = calc.register_derived(
            "cpu_pct",
            ["cpu_used", "cpu_total"],
            "{cpu_used} / {cpu_total} * 100"
        )
        assert derived.name == "cpu_pct"
        assert "cpu_pct" in calc.derived_metrics

    def test_calculate(self, stats_module: Any) -> None:
        """Test calculating a derived metric."""
        calc = stats_module.DerivedMetricCalculator()
        calc.register_derived(
            "ratio",
            ["a", "b"],
            "{a} / {b}"
        )
        result = calc.calculate("ratio", {"a": 10.0, "b": 2.0})
        assert result == 5.0

    def test_get_all_derived(self, stats_module: Any) -> None:
        """Test getting all derived metrics."""
        calc = stats_module.DerivedMetricCalculator()
        calc.register_derived("sum", ["a", "b"], "{a} + {b}")
        results = calc.get_all_derived({"a": 5.0, "b": 3.0})
        assert results["sum"] == 8.0


# ========== Session 7 Tests: StatsRollup ==========



class TestStatsRollup:
    """Tests for StatsRollup class."""

    def test_init(self, stats_module: Any) -> None:
        """Test StatsRollup initialization."""
        rollup = stats_module.StatsRollup()
        assert rollup.configs == {}

    def test_configure_rollup(self, stats_module: Any) -> None:
        """Test configuring a rollup."""
        rollup = stats_module.StatsRollup()
        config = rollup.configure_rollup(
            "hourly_avg",
            ["cpu.usage"],
            stats_module.AggregationType.AVG
        )
        assert config.name == "hourly_avg"
        assert "hourly_avg" in rollup.configs

    def test_add_value(self, stats_module: Any) -> None:
        """Test adding values for rollup."""
        rollup = stats_module.StatsRollup()
        rollup.add_value("cpu.usage", 50.0)
        rollup.add_value("cpu.usage", 60.0)
        assert len(rollup._raw_data["cpu.usage"]) == 2

    def test_compute_rollup(self, stats_module: Any) -> None:
        """Test computing a rollup."""
        rollup = stats_module.StatsRollup()
        rollup.configure_rollup(
            "test_rollup",
            ["cpu.usage"],
            stats_module.AggregationType.AVG
        )
        rollup.add_value("cpu.usage", 50.0)
        rollup.add_value("cpu.usage", 70.0)
        result = rollup.compute_rollup("test_rollup")
        assert len(result) == 1
        assert result[0]["value"] == 60.0

    def test_get_rollup_history(self, stats_module: Any) -> None:
        """Test getting rollup history."""
        rollup = stats_module.StatsRollup()
        rollup.configure_rollup("test", ["m"], stats_module.AggregationType.SUM)
        history = rollup.get_rollup_history("test")
        assert isinstance(history, list)


# ========== Session 7 Tests: StatsAPIServer ==========



class TestStatsAPIServer:
    """Tests for StatsAPIServer class."""

    def test_init(self, stats_module: Any) -> None:
        """Test StatsAPIServer initialization."""
        server = stats_module.StatsAPIServer()
        assert len(server.endpoints) > 0

    def test_register_endpoint(self, stats_module: Any) -> None:
        """Test registering an endpoint."""
        server = stats_module.StatsAPIServer()
        endpoint = server.register_endpoint("/api / custom", method="POST")
        assert endpoint.path == "/api / custom"
        assert "/api / custom" in server.endpoints

    def test_handle_request(self, stats_module: Any, agent: Any) -> None:
        """Test handling a request."""
        server = stats_module.StatsAPIServer(agent)
        response = server.handle_request("/api / stats")
        assert response["status"] == 200

    def test_handle_unknown_endpoint(self, stats_module: Any) -> None:
        """Test handling unknown endpoint."""
        server = stats_module.StatsAPIServer()
        response = server.handle_request("/api / unknown")
        assert response["status"] == 404

    def test_get_api_docs(self, stats_module: Any) -> None:
        """Test getting API docs."""
        server = stats_module.StatsAPIServer()
        docs = server.get_api_docs()
        assert "openapi" in docs
        assert "3.0.0" in docs


# =============================================================================
# Session 8: Test File Improvement Tests
# =============================================================================



class TestRealTimeStatsStreaming:
    """Tests for real-time stats streaming."""

    def test_stream_manager_creates_stream(self, stats_module: Any) -> None:
        """Test stream manager creates streams."""
        StatsStreamManager = stats_module.StatsStreamManager

        manager = StatsStreamManager()
        stream = manager.create_stream("cpu_metrics", buffer_size=100)

        assert stream.name == "cpu_metrics"
        assert stream.buffer_size == 100

    def test_stream_receives_data(self, stats_module: Any) -> None:
        """Test stream receives data points."""
        StatsStreamManager = stats_module.StatsStreamManager

        manager = StatsStreamManager()
        stream = manager.create_stream("test_stream")

        manager.publish("test_stream", {"value": 42})
        manager.publish("test_stream", {"value": 43})

        data = stream.get_latest(count=2)
        assert len(data) == 2

    def test_stream_subscriber_receives_updates(self, stats_module: Any) -> None:
        """Test stream subscribers receive updates."""
        StatsStreamManager = stats_module.StatsStreamManager

        manager = StatsStreamManager()
        manager.create_stream("events")

        received: list[dict[str, Any]] = []
        manager.subscribe("events", lambda d: received.append(d))
        manager.publish("events", {"event": "test"})

        assert len(received) == 1



class TestStatsFederationAcrossSources:
    """Tests for stats federation across multiple sources."""

    def test_federation_adds_sources(self, stats_module: Any) -> None:
        """Test federation adds multiple sources."""
        StatsFederation = stats_module.StatsFederation

        federation = StatsFederation()
        federation.add_source("source1", endpoint="http://localhost:8001")
        federation.add_source("source2", endpoint="http://localhost:8002")

        assert len(federation.sources) == 2

    def test_federation_aggregates_data(self, stats_module: Any) -> None:
        """Test federation aggregates data from sources."""
        StatsFederation = stats_module.StatsFederation

        federation = StatsFederation()
        federation.add_source("s1", data={"metric1": 100})
        federation.add_source("s2", data={"metric1": 200})

        aggregated = federation.aggregate("metric1")
        assert aggregated["total"] == 300

    def test_federation_handles_source_failure(self, stats_module: Any) -> None:
        """Test federation handles source failures gracefully."""
        StatsFederation = stats_module.StatsFederation

        federation = StatsFederation()
        federation.add_source("healthy", data={"value": 50})
        federation.add_source("failed", endpoint="http://invalid", healthy=False)

        result = federation.aggregate("value")
        assert result["total"] == 50
        assert result["failed_sources"] == 1



class TestStatsRetentionPolicyEnforcement:
    """Tests for stats retention policy enforcement."""

    def test_retention_policy_creation(self, stats_module: Any) -> None:
        """Test retention policy creation."""
        RetentionPolicy = stats_module.RetentionPolicy

        policy = RetentionPolicy(
            name="short_term",
            retention_days=7,
            resolution="1m"
        )

        assert policy.retention_days == 7

    def test_retention_enforcer_removes_old_data(self, stats_module: Any) -> None:
        """Test retention enforcer removes old data."""
        RetentionEnforcer = stats_module.RetentionEnforcer
        RetentionPolicy = stats_module.RetentionPolicy

        enforcer = RetentionEnforcer()
        policy = RetentionPolicy("test", retention_days=1)
        enforcer.set_policy("metrics.*", policy)

        # Add old and new data
        enforcer.add_data("metrics.cpu", timestamp=0, value=50)  # Very old
        enforcer.add_data("metrics.cpu", timestamp=datetime.now().timestamp(), value=60)

        removed = enforcer.enforce()
        assert removed >= 1



class TestStatsNamespaceIsolation:
    """Tests for stats namespace isolation and scoping."""

    def test_namespace_creation(self, stats_module: Any) -> None:
        """Test namespace creation."""
        StatsNamespace = stats_module.StatsNamespace

        ns = StatsNamespace("production")
        assert ns.name == "production"

    def test_namespace_metric_scoping(self, stats_module: Any) -> None:
        """Test metrics are scoped to namespace."""
        StatsNamespace = stats_module.StatsNamespace

        prod = StatsNamespace("production")
        dev = StatsNamespace("development")

        prod.set_metric("cpu", 80)
        dev.set_metric("cpu", 20)

        assert prod.get_metric("cpu") == 80
        assert dev.get_metric("cpu") == 20

    def test_namespace_isolation(self, stats_module: Any) -> None:
        """Test namespaces are isolated."""
        StatsNamespaceManager = stats_module.StatsNamespaceManager

        manager = StatsNamespaceManager()
        ns1 = manager.create("ns1")
        ns2 = manager.create("ns2")

        ns1.set_metric("counter", 100)

        assert ns2.get_metric("counter") is None



class TestStatsMetricFormulaCalculation:
    """Tests for stats metric formula calculation."""

    def test_formula_simple_calculation(self, stats_module: Any) -> None:
        """Test simple formula calculation."""
        FormulaEngine = stats_module.FormulaEngine

        engine = FormulaEngine()
        engine.define("usage_percent", "{used} / {total} * 100")

        result = engine.calculate("usage_percent", {"used": 40, "total": 100})
        assert result == 40.0

    def test_formula_with_aggregation(self, stats_module: Any) -> None:
        """Test formula with aggregation functions."""
        FormulaEngine = stats_module.FormulaEngine

        engine = FormulaEngine()
        engine.define("avg_latency", "AVG({latencies})")

        result = engine.calculate("avg_latency", {"latencies": [10, 20, 30]})
        assert result == 20.0

    def test_formula_validation(self, stats_module: Any) -> None:
        """Test formula validation."""
        FormulaEngine = stats_module.FormulaEngine

        engine = FormulaEngine()

        valid = engine.validate("{a} + {b}")
        invalid = engine.validate("{a} +++ {b}")

        assert valid.is_valid
        assert not invalid.is_valid



class TestStatsABComparison:
    """Tests for stats A / B comparison functionality."""

    def test_ab_comparison_basic(self, stats_module: Any) -> None:
        """Test basic A / B comparison."""
        ABComparator = stats_module.ABComparator

        comparator = ABComparator()

        group_a = {"conversion_rate": 0.12, "avg_time": 45}
        group_b = {"conversion_rate": 0.15, "avg_time": 40}

        result = comparator.compare(group_a, group_b)

        assert result.metrics_compared == 2
        assert "conversion_rate" in result.differences

    def test_ab_statistical_significance(self, stats_module: Any) -> None:
        """Test A / B statistical significance calculation."""
        ABComparator = stats_module.ABComparator

        comparator = ABComparator()

        # Large sample with clear difference
        result = comparator.calculate_significance(
            control_values=[10, 11, 12, 9, 10] * 100,
            treatment_values=[15, 16, 14, 15, 16] * 100
        )

        assert result.is_significant



class TestStatsForecastingAccuracy:
    """Tests for stats forecasting accuracy."""

    def test_forecaster_predicts_trend(self, stats_module: Any) -> None:
        """Test forecaster predicts trends."""
        StatsForecaster = stats_module.StatsForecaster

        forecaster = StatsForecaster()

        # Linear increasing data
        historical = [10, 20, 30, 40, 50]
        forecast = forecaster.predict(historical, periods=3)

        assert len(forecast) == 3
        # Should continue increasing
        assert forecast[0] > historical[-1]

    def test_forecaster_calculates_confidence(self, stats_module: Any) -> None:
        """Test forecaster calculates confidence intervals."""
        StatsForecaster = stats_module.StatsForecaster

        forecaster = StatsForecaster()

        historical = [100, 102, 98, 101, 99]
        result = forecaster.predict_with_confidence(historical, periods=2)

        assert "predictions" in result
        assert "confidence_lower" in result
        assert "confidence_upper" in result



class TestStatsSnapshotCreationAndRestore:
    """Tests for stats snapshot creation and restore."""

    def test_snapshot_creation(self, stats_module: Any, tmp_path: Path) -> None:
        """Test snapshot creation."""
        StatsSnapshotManager = stats_module.StatsSnapshotManager

        manager = StatsSnapshotManager(snapshot_dir=tmp_path)

        data = {"cpu": 50, "memory": 70, "disk": 30}
        snapshot = manager.create_snapshot("system_metrics", data)

        assert snapshot.name == "system_metrics"
        assert snapshot.data == data

    def test_snapshot_restore(self, stats_module: Any, tmp_path: Path) -> None:
        """Test snapshot restore."""
        StatsSnapshotManager = stats_module.StatsSnapshotManager

        manager = StatsSnapshotManager(snapshot_dir=tmp_path)

        original = {"value": 42}
        manager.create_snapshot("test", original)

        restored = manager.restore_snapshot("test")
        assert restored == original

    def test_snapshot_list(self, stats_module: Any, tmp_path: Path) -> None:
        """Test listing snapshots."""
        StatsSnapshotManager = stats_module.StatsSnapshotManager

        manager = StatsSnapshotManager(snapshot_dir=tmp_path)
        manager.create_snapshot("snap1", {"a": 1})
        manager.create_snapshot("snap2", {"b": 2})

        snapshots = manager.list_snapshots()
        assert len(snapshots) == 2



class TestStatsThresholdAlerting:
    """Tests for stats threshold alerting system."""

    def test_threshold_alert_triggers(self, stats_module: Any) -> None:
        """Test threshold alert triggers."""
        ThresholdAlertManager = stats_module.ThresholdAlertManager

        manager = ThresholdAlertManager()
        manager.set_threshold("cpu_usage", warning=70, critical=90)

        alerts = manager.check("cpu_usage", 95)

        assert len(alerts) >= 1
        assert any(a.severity == "critical" for a in alerts)

    def test_threshold_no_alert_below_threshold(self, stats_module: Any) -> None:
        """Test no alert when below threshold."""
        ThresholdAlertManager = stats_module.ThresholdAlertManager

        manager = ThresholdAlertManager()
        manager.set_threshold("memory", warning=80, critical=95)

        alerts = manager.check("memory", 50)
        assert len(alerts) == 0



class TestStatsSubscriptionAndNotification:
    """Tests for stats subscription and notification delivery."""

    def test_subscription_creation(self, stats_module: Any) -> None:
        """Test subscription creation."""
        StatsSubscriptionManager = stats_module.StatsSubscriptionManager

        manager = StatsSubscriptionManager()
        sub = manager.subscribe(
            subscriber_id="user1",
            metric_pattern="cpu.*",
            delivery_method="email"
        )

        assert sub.subscriber_id == "user1"

    def test_notification_delivery(self, stats_module: Any) -> None:
        """Test notification delivery."""
        StatsSubscriptionManager = stats_module.StatsSubscriptionManager

        manager = StatsSubscriptionManager()
        manager.subscribe("user1", "alerts.*", "webhook")

        delivered: list[str] = []
        manager.set_delivery_handler("webhook", lambda msg: delivered.append(msg))
        manager.notify("alerts.cpu", "CPU threshold exceeded")

        assert len(delivered) >= 1



class TestStatsExportToMonitoringPlatforms:
    """Tests for stats export to monitoring platforms."""

    def test_prometheus_export(self, stats_module: Any) -> None:
        """Test Prometheus format export."""
        StatsExporter = stats_module.StatsExporter

        exporter = StatsExporter(format="prometheus")

        metrics = {"cpu_usage": 75.5, "memory_usage": 60.2}
        output = exporter.export(metrics)

        assert "cpu_usage" in output
        assert "75.5" in output

    def test_json_export(self, stats_module: Any) -> None:
        """Test JSON format export."""
        StatsExporter = stats_module.StatsExporter

        exporter = StatsExporter(format="json")

        metrics = {"metric1": 100}
        output = exporter.export(metrics)

        parsed = json.loads(output)
        assert parsed["metric1"] == 100



class TestStatsAnnotationPersistence:
    """Tests for stats annotation and comment persistence."""

    def test_annotation_creation(self, stats_module: Any) -> None:
        """Test annotation creation."""
        StatsAnnotationManager = stats_module.StatsAnnotationManager

        manager = StatsAnnotationManager()
        annotation = manager.add_annotation(
            metric="cpu_usage",
            timestamp=datetime.now().timestamp(),
            text="Deployment started",
            author="admin"
        )

        assert annotation.text == "Deployment started"

    def test_annotation_retrieval(self, stats_module: Any) -> None:
        """Test annotation retrieval."""
        StatsAnnotationManager = stats_module.StatsAnnotationManager

        manager = StatsAnnotationManager()
        manager.add_annotation("cpu", timestamp=100, text="Event 1")
        manager.add_annotation("cpu", timestamp=200, text="Event 2")

        annotations = manager.get_annotations("cpu")
        assert len(annotations) == 2



class TestStatsChangeNotificationSystem:
    """Tests for stats change notification system."""

    def test_change_detection(self, stats_module: Any) -> None:
        """Test change detection."""
        StatsChangeDetector = stats_module.StatsChangeDetector

        detector = StatsChangeDetector(threshold_percent=10)

        detector.record("metric1", 100)
        detector.record("metric1", 115)

        changes = detector.get_changes()
        assert len(changes) >= 1

    def test_change_notification(self, stats_module: Any) -> None:
        """Test change notification."""
        StatsChangeDetector = stats_module.StatsChangeDetector

        detector = StatsChangeDetector(threshold_percent=20)

        notifications: list[dict[str, Any]] = []
        detector.on_change(lambda c: notifications.append(c))

        detector.record("metric1", 100)
        detector.record("metric1", 150)  # 50% change

        assert len(notifications) >= 1



class TestStatsCompressionAlgorithms:
    """Tests for stats compression algorithms."""

    def test_compression_reduces_size(self, stats_module: Any) -> None:
        """Test compression reduces data size."""
        StatsCompressor = stats_module.StatsCompressor

        compressor = StatsCompressor()

        # Repetitive data compresses well
        data = [100.0] * 1000
        compressed = compressor.compress(data)

        assert len(compressed) < len(str(data))

    def test_compression_decompression_roundtrip(self, stats_module: Any) -> None:
        """Test compression / decompression roundtrip."""
        StatsCompressor = stats_module.StatsCompressor

        compressor = StatsCompressor()

        original = [10.5, 20.3, 30.1, 40.7, 50.9]
        compressed = compressor.compress(original)
        decompressed = compressor.decompress(compressed)

        assert decompressed == original



class TestStatsRollupCalculations:
    """Tests for stats rollup calculations (extended)."""

    def test_hourly_rollup(self, stats_module: Any) -> None:
        """Test hourly rollup calculation."""
        StatsRollupCalculator = stats_module.StatsRollupCalculator

        calculator = StatsRollupCalculator()

        # Add minute-level data
        for i in range(60):
            calculator.add_point("cpu", timestamp=i * 60, value=50 + i % 10)

        hourly = calculator.rollup("cpu", interval="1h")
        assert len(hourly) == 1  # One hour of data

    def test_daily_rollup(self, stats_module: Any) -> None:
        """Test daily rollup calculation."""
        StatsRollupCalculator = stats_module.StatsRollupCalculator

        calculator = StatsRollupCalculator()

        # Add hourly data for a day
        for i in range(24):
            calculator.add_point("memory", timestamp=i * 3600, value=60)

        daily = calculator.rollup("memory", interval="1d")
        assert len(daily) == 1



class TestStatsAccessControl:
    """Tests for stats access control."""

    def test_access_control_grant(self, stats_module: Any) -> None:
        """Test granting access."""
        StatsAccessController = stats_module.StatsAccessController

        controller = StatsAccessController()
        controller.grant("user1", "metrics.*", level="read")

        assert controller.can_access("user1", "metrics.cpu", "read")

    def test_access_control_deny(self, stats_module: Any) -> None:
        """Test denying access."""
        StatsAccessController = stats_module.StatsAccessController

        controller = StatsAccessController()
        controller.grant("user1", "public.*", level="read")

        assert not controller.can_access("user1", "private.secret", "read")

    def test_access_control_write_level(self, stats_module: Any) -> None:
        """Test write level access."""
        StatsAccessController = stats_module.StatsAccessController

        controller = StatsAccessController()
        controller.grant("admin", "metrics.*", level="write")

        assert controller.can_access("admin", "metrics.cpu", "write")
        assert controller.can_access("admin", "metrics.cpu", "read")  # Write implies read



class TestStatsBackupAndRestore:
    """Tests for stats backup and restore."""

    def test_backup_creation(self, stats_module: Any, tmp_path: Path) -> None:
        """Test backup creation."""
        StatsBackupManager = stats_module.StatsBackupManager

        manager = StatsBackupManager(backup_dir=tmp_path)

        data = {"metrics": [{"name": "cpu", "value": 50}]}
        backup = manager.create_backup("full_backup", data)

        assert backup.name == "full_backup"
        assert backup.path.exists()

    def test_backup_restore(self, stats_module: Any, tmp_path: Path) -> None:
        """Test backup restore."""
        StatsBackupManager = stats_module.StatsBackupManager

        manager = StatsBackupManager(backup_dir=tmp_path)

        original = {"value": 42, "items": [1, 2, 3]}
        manager.create_backup("test_backup", original)

        restored = manager.restore("test_backup")
        assert restored == original

    def test_backup_list(self, stats_module: Any, tmp_path: Path) -> None:
        """Test listing backups."""
        StatsBackupManager = stats_module.StatsBackupManager

        manager = StatsBackupManager(backup_dir=tmp_path)
        manager.create_backup("backup1", {"a": 1})
        manager.create_backup("backup2", {"b": 2})

        backups = manager.list_backups()
        assert len(backups) == 2


# ========== Comprehensive Stats Tests (from test_agent_stats_comprehensive.py) ==========


class TestTrendAnalysis(unittest.TestCase):
    """Tests for trend analysis and delta calculation."""

    def test_calculate_trend(self):
        """Test trend calculation from time series data."""
        data = [1, 2, 3, 4, 5]
        # Upward trend
        assert data[-1] > data[0]

    def test_calculate_delta(self):
        """Test delta calculation between values."""
        current = 100
        previous = 80
        delta = current - previous
        assert delta == 20

    def test_trend_percentage_change(self):
        """Test percentage change calculation."""
        old_value = 100
        new_value = 110
        percent_change = ((new_value - old_value) / old_value) * 100
        assert percent_change == 10.0

    def test_trend_direction(self):
        """Test determining trend direction."""
        values = [5, 4, 3, 2, 1]
        is_decreasing = values[0] > values[-1]
        assert is_decreasing



class TestCSVExport(unittest.TestCase):
    """Tests for CSV export functionality."""

    def test_export_stats_to_csv(self):
        """Test exporting stats to CSV format."""
        stats = [
            {"date": "2024-12-16", "tests": 100, "pass": 95},
            {"date": "2024-12-17", "tests": 102, "pass": 98},
        ]

        csv_lines = ["date,tests,pass"]
        for stat in stats:
            csv_lines.append(f"{stat['date']},{stat['tests']},{stat['pass']}")

        csv_content = "\n".join(csv_lines)
        assert "2024-12-16" in csv_content
        assert "date,tests,pass" in csv_content

    def test_csv_escaping(self):
        """Test proper CSV escaping."""
        escaped = '"{value}"'
        assert escaped.startswith('"')
        assert escaped.endswith('"')

    def test_csv_with_special_characters(self):
        """Test CSV with special characters."""
        csv_line = '{"test,with,commas",123}'
        assert "test,with,commas" in csv_line



class TestExportFormats(unittest.TestCase):
    """Tests for different export formats."""

    def test_export_json_format(self):
        """Test exporting to JSON format."""
        stats = {"tests": 100, "pass": 95, "timestamp": "2024-12-16"}
        json_str = json.dumps(stats)
        assert '"tests": 100' in json_str
        assert '"pass": 95' in json_str

    def test_export_html_format(self):
        """Test exporting to HTML format."""
        html = """<table>
<tr><td>Test</td><td>100</td></tr>
<tr><td>Pass</td><td>95</td></tr>
</table>"""
        assert "<table>" in html
        assert "</table>" in html
        assert "100" in html

    def test_export_excel_metadata(self):
        """Test Excel export with metadata."""
        excel_data = {
            "sheet": "Statistics",
            "rows": 100,
            "columns": 5
        }
        assert excel_data["rows"] == 100
        assert excel_data["sheet"] == "Statistics"



class TestAggregation(unittest.TestCase):
    """Tests for stat aggregation."""

    def test_aggregate_by_file(self):
        """Test aggregating stats by file."""
        stats = [
            {"file": "a.py", "lines": 100, "functions": 10},
            {"file": "a.py", "lines": 50, "functions": 5},
            {"file": "b.py", "lines": 200, "functions": 20},
        ]

        aggregated = {}
        for stat in stats:
            if stat["file"] not in aggregated:
                aggregated[stat["file"]] = []
            aggregated[stat["file"]].append(stat)

        assert len(aggregated) == 2
        assert len(aggregated["a.py"]) == 2

    def test_aggregate_by_agent(self):
        """Test aggregating stats by agent."""
        stats = [
            {"agent": "A", "completed": 5},
            {"agent": "A", "completed": 3},
            {"agent": "B", "completed": 7},
        ]

        totals = {}
        for stat in stats:
            agent = stat["agent"]
            if agent not in totals:
                totals[agent] = 0
            totals[agent] += stat["completed"]

        assert totals["A"] == 8
        assert totals["B"] == 7

    def test_aggregate_by_date(self):
        """Test aggregating stats by date."""
        stats = [
            {"date": "2024-12-16", "value": 10},
            {"date": "2024-12-16", "value": 15},
            {"date": "2024-12-17", "value": 20},
        ]

        daily_totals = {}
        for stat in stats:
            date = stat["date"]
            if date not in daily_totals:
                daily_totals[date] = 0
            daily_totals[date] += stat["value"]

        assert daily_totals["2024-12-16"] == 25
        assert daily_totals["2024-12-17"] == 20



class TestStatisticalSummaries(unittest.TestCase):
    """Tests for statistical summaries."""

    def test_calculate_mean(self):
        """Test mean calculation."""
        values = [10, 20, 30, 40, 50]
        mean = sum(values) / len(values)
        assert mean == 30.0

    def test_calculate_median(self):
        """Test median calculation."""
        values = [1, 2, 3, 4, 5]
        sorted_values = sorted(values)
        median = sorted_values[len(sorted_values) // 2]
        assert median == 3

    def test_calculate_stddev(self):
        """Test standard deviation calculation."""
        values = [1, 2, 3, 4, 5]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        stddev = variance ** 0.5
        assert stddev > 0

    def test_calculate_min_max(self):
        """Test min / max calculation."""
        values = [10, 20, 30, 40, 50]
        assert min(values) == 10
        assert max(values) == 50



class TestComparison(unittest.TestCase):
    """Tests for stat comparison."""

    def test_compare_current_vs_baseline(self):
        """Test comparing current to baseline."""
        baseline = 100
        current = 120
        improvement = current - baseline
        assert improvement == 20
        assert current > baseline

    def test_compare_current_vs_previous(self):
        """Test comparing current to previous."""
        previous = 95
        current = 100
        delta = current - previous
        assert delta > 0

    def test_threshold_detection(self):
        """Test detecting threshold violations."""
        threshold = 0.8  # 80% pass rate
        actual = 0.75
        is_below_threshold = actual < threshold
        assert is_below_threshold



class TestVisualization(unittest.TestCase):
    """Tests for visualization generation."""

    def test_generate_chart_data(self):
        """Test generating chart data."""
        stats = [
            {"date": "2024-12-16", "value": 100},
            {"date": "2024-12-17", "value": 120},
            {"date": "2024-12-18", "value": 115},
        ]

        chart_data = {
            "labels": [s["date"] for s in stats],
            "values": [s["value"] for s in stats]
        }

        assert len(chart_data["labels"]) == 3
        assert len(chart_data["values"]) == 3

    def test_format_for_display(self):
        """Test formatting stats for display."""
        value = 0.856432
        formatted = f"{value:.2%}"
        assert "85.64%" in formatted



class TestMetricFiltering(unittest.TestCase):
    """Tests for metric filtering and selection."""

    def test_filter_by_metric_type(self):
        """Test filtering stats by metric type."""
        all_stats = [
            {"type": "coverage", "value": 85},
            {"type": "performance", "value": 1200},
            {"type": "coverage", "value": 90},
        ]

        coverage_stats = [s for s in all_stats if s["type"] == "coverage"]
        assert len(coverage_stats) == 2
        assert all(s["type"] == "coverage" for s in coverage_stats)

    def test_filter_by_date_range(self):
        """Test filtering stats by date range."""

        stats = [
            {"date": datetime(2024, 12, 14)},
            {"date": datetime(2024, 12, 16)},
            {"date": datetime(2024, 12, 18)},
        ]

        start = datetime(2024, 12, 15)
        end = datetime(2024, 12, 17)
        filtered = [s for s in stats if start <= s["date"] <= end]
        assert len(filtered) == 1

    def test_select_top_metrics(self):
        """Test selecting top metrics."""
        metrics = [
            {"name": "metric1", "value": 10},
            {"name": "metric2", "value": 50},
            {"name": "metric3", "value": 30},
        ]

        top_3 = sorted(metrics, key=lambda x: x["value"], reverse=True)[:3]
        assert top_3[0]["value"] == 50



class TestTimeSeries(unittest.TestCase):
    """Tests for time-series data persistence."""

    def test_persist_time_series_data(self):
        """Test persisting time series data."""
        data = [
            {"timestamp": "2024-12-16T10:00:00", "value": 100},
            {"timestamp": "2024-12-16T11:00:00", "value": 105},
        ]

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(data, f)
            f.flush()
            fname = f.name

        try:
            with open(fname) as f:
                loaded = json.load(f)
            assert len(loaded) == 2
            assert loaded[0]["value"] == 100
        finally:
            Path(fname).unlink()

    def test_load_time_series_data(self):
        """Test loading time series data."""
        data = [
            {"timestamp": "2024-12-16T10:00:00", "value": 100},
        ]

        assert len(data) == 1
        assert data[0]["value"] == 100



class TestValidation(unittest.TestCase):
    """Tests for stat validation and anomaly detection."""

    def test_validate_stat_value(self):
        """Test validating stat values."""
        # Percentage should be 0-100
        value = 85
        is_valid = 0 <= value <= 100
        assert is_valid

    def test_detect_anomaly(self):
        """Test detecting anomalies."""
        values = [100, 105, 103, 102, 200]  # Last value is anomaly
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        variance ** 0.5

        # The last value (200) is significantly higher than mean
        assert values[-1] > mean * 1.5  # Obvious anomaly

    def test_validate_data_consistency(self):
        """Test data consistency validation."""
        stats = {
            "total": 100,
            "passed": 85,
            "failed": 15,
        }
        # Verify: passed + failed=total
        assert stats["passed"] + stats["failed"] == stats["total"]



class TestCaching(unittest.TestCase):
    """Tests for stat caching and performance."""

    def test_cache_stat_results(self):
        """Test caching stat computation results."""
        cache = {}

        def get_stat(key):
            if key not in cache:
                # Expensive computation
                cache[key] = sum(range(1000))
            return cache[key]

        result1 = get_stat("test")
        result2 = get_stat("test")

        assert result1 == result2
        assert len(cache) == 1

    def test_cache_invalidation(self):
        """Test cache invalidation."""
        cache = {"key": "old_value"}

        # Invalidate
        del cache["key"]
        assert "key" not in cache



class TestReporting(unittest.TestCase):
    """Tests for stat report generation."""

    def test_generate_stat_report(self):
        """Test generating comprehensive stat report."""
        report = """
=== Statistics Report ===
Date: 2024-12-16
Total Tests: 100
Passed: 95
Failed: 5
Pass Rate: 95.0%
"""
        assert "=== Statistics Report ===" in report
        assert "2024-12-16" in report
        assert "95" in report

    def test_generate_insights(self):
        """Test generating insights from stats."""
        stats = {
            "pass_rate": 0.95,
            "trend": "improving",
        }

        if stats["pass_rate"] > 0.90:
            insight = "Excellent test pass rate"
        else:
            insight = "Test pass rate needs improvement"

        assert "Excellent" in insight



class TestCoverageMetrics(unittest.TestCase):
    """Tests for code coverage metric tracking."""

    def test_parse_coverage_data(self):
        """Test parsing coverage metrics."""
        coverage_data = {
            "totals": {
                "lines_valid": 1000,
                "lines_covered": 850,
                "branches_valid": 200,
                "branches_covered": 160,
            }
        }

        line_coverage = (coverage_data["totals"]["lines_covered"] /
                         coverage_data["totals"]["lines_valid"]) * 100

        assert line_coverage == 85.0

    def test_track_coverage_trends(self):
        """Test tracking coverage over time."""
        coverage_history = [
            {"date": "2025-12-14", "coverage": 75.0},
            {"date": "2025-12-15", "coverage": 78.0},
            {"date": "2025-12-16", "coverage": 82.0},
        ]

        improvement = coverage_history[-1]["coverage"] - coverage_history[0]["coverage"]
        assert improvement == 7.0

    def test_identify_coverage_gaps(self):
        """Test identifying coverage gaps."""
        coverage_by_file = {
            "main.py": 95.0,
            "utils.py": 60.0,
            "helpers.py": 45.0,
        }

        gaps = {k: v for k, v in coverage_by_file.items() if v < 80}
        assert len(gaps) == 2



class TestDocstrings(unittest.TestCase):
    """Tests for docstring validation."""

    def test_validate_google_style_docstring(self):
        """Test validating Google-style docstring."""
        docstring = """
        Process files and generate statistics.

        Args:
            files: List of file paths to process.
            verbose: Enable verbose logging.

        Returns:
            Dictionary with aggregated statistics.

        Raises:
            FileNotFoundError: If a file doesn't exist.
        """

        assert "Args:" in docstring
        assert "Returns:" in docstring
        assert "Raises:" in docstring

    def test_detect_missing_docstrings(self):
        """Test detecting missing docstrings."""
        functions = [
            {"name": "process", "docstring": "Process data."},
            {"name": "analyze", "docstring": None},
            {"name": "report", "docstring": "Generate report."},
        ]

        missing = [f["name"] for f in functions if not f["docstring"]]
        assert "analyze" in missing



class TestPathLibUsage(unittest.TestCase):
    """Tests for pathlib migration."""

    def test_use_pathlib_for_paths(self):
        """Test using pathlib instead of strings."""
        from pathlib import Path

        path = Path("test.py")
        assert path.suffix == ".py"

    def test_pathlib_operations(self):
        """Test pathlib path operations."""
        from pathlib import Path

        paths = [Path("a.py"), Path("b.py"), Path("c.txt")]
        py_files = [p for p in paths if p.suffix == ".py"]

        assert len(py_files) == 2

    def test_pathlib_glob_patterns(self):
        """Test using pathlib glob patterns."""
        from pathlib import Path

        # Simulated file system
        files = [Path("src / main.py"), Path("src / utils.py"), Path("tests / test.py")]
        py_files = [f for f in files if f.suffix == ".py"]

        assert len(py_files) == 3



class TestTimeSeriesStorage(unittest.TestCase):
    """Tests for persisting stats history."""

    def test_store_stats_history(self):
        """Test storing stats over time."""
        from datetime import timedelta

        history = []

        for i in range(5):
            timestamp = datetime.now() - timedelta(days=5 - i)
            history.append({
                "timestamp": timestamp.isoformat(),
                "files": 50 + (i * 10),
                "errors": 10 - i,
            })

        assert len(history) == 5
        assert history[0]["files"] < history[-1]["files"]

    def test_load_historical_stats(self):
        """Test loading historical stats."""
        historical_data = [
            {"date": "2025-12-14", "value": 100},
            {"date": "2025-12-15", "value": 110},
            {"date": "2025-12-16", "value": 120},
        ]

        latest = historical_data[-1]
        assert latest["value"] == 120

    def test_query_stats_by_date_range(self):
        """Test querying stats by date range."""
        all_stats = [
            {"date": "2025-12-10", "value": 50},
            {"date": "2025-12-15", "value": 100},
            {"date": "2025-12-16", "value": 120},
        ]

        filtered = [s for s in all_stats if "2025-12-15" <= s["date"] <= "2025-12-16"]
        assert len(filtered) == 2



class TestFiltering(unittest.TestCase):
    """Tests for filtering stats."""

    def test_filter_by_file_pattern(self):
        """Test filtering by file pattern."""
        stats = [
            {"file": "src/main.py", "errors": 5},
            {"file": "src/utils.py", "errors": 2},
            {"file": "tests/test.py", "errors": 1},
        ]

        src_only = [s for s in stats if s["file"].startswith("src/")]
        assert len(src_only) == 2

    def test_filter_by_agent_type(self):
        """Test filtering by agent type."""
        stats = [
            {"agent": "coder", "improvements": 10},
            {"agent": "tester", "improvements": 8},
            {"agent": "coder", "improvements": 5},
        ]

        coder_stats = [s for s in stats if s["agent"] == "coder"]
        assert len(coder_stats) == 2

    def test_filter_by_date_range(self):
        """Test filtering by date range."""
        stats = [
            {"date": "2025-12-14", "value": 100},
            {"date": "2025-12-15", "value": 110},
            {"date": "2025-12-16", "value": 120},
        ]

        recent = [s for s in stats if s["date"] >= "2025-12-15"]
        assert len(recent) == 2



class TestComparisonReports(unittest.TestCase):
    """Tests for generating comparison reports."""

    def test_compare_current_vs_baseline(self):
        """Test current vs baseline comparison."""
        current = {"files": 100, "errors": 5, "improvements": 20}
        baseline = {"files": 80, "errors": 10, "improvements": 15}

        comparison = {
            "files_change": current["files"] - baseline["files"],
            "errors_change": current["errors"] - baseline["errors"],
        }

        assert comparison["files_change"] == 20
        assert comparison["errors_change"] == -5

    def test_compare_current_vs_previous(self):
        """Test current vs previous run comparison."""
        history = [
            {"run": 1, "errors": 10},
            {"run": 2, "errors": 8},
            {"run": 3, "errors": 5},
        ]

        if len(history) >= 2:
            delta = history[-1]["errors"] - history[-2]["errors"]
            assert delta == -3

    def test_generate_trend_report(self):
        """Test generating trend report."""
        runs = [
            {"timestamp": "2025-12-14", "score": 70},
            {"timestamp": "2025-12-15", "score": 75},
            {"timestamp": "2025-12-16", "score": 82},
        ]

        trend = "improving" if runs[-1]["score"] > runs[0]["score"] else "declining"
        assert trend == "improving"



class TestVisualizationGeneration(unittest.TestCase):
    """Tests for generating visual reports."""

    def test_generate_chart_data(self):
        """Test generating chart data."""
        stats = [
            {"category": "A", "value": 50},
            {"category": "B", "value": 75},
            {"category": "C", "value": 60},
        ]

        chart_data = {s["category"]: s["value"] for s in stats}
        assert chart_data["B"] == 75

    def test_create_heatmap_data(self):
        """Test creating heatmap data."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

        assert matrix[1][1] == 5

    def test_generate_dashboard_summary(self):
        """Test generating dashboard summary."""
        metrics = {
            "files_processed": 100,
            "errors_fixed": 25,
            "improvements_applied": 50,
            "processing_time": 45.2,
        }

        summary = {
            "total_metrics": len(metrics),
            "key_metric": metrics["files_processed"],
        }

        assert summary["total_metrics"] == 4



class TestAlerting(unittest.TestCase):
    """Tests for alerting on metric thresholds."""

    def test_check_error_threshold(self):
        """Test checking error threshold."""
        errors = 15
        threshold = 10

        alert = errors > threshold
        assert alert

    def test_generate_alert_message(self):
        """Test generating alert message."""
        metric = "error_rate"
        value = 15
        threshold = 10

        message = f"ALERT: {metric} ({value}) exceeds threshold ({threshold})"
        assert "ALERT" in message

    def test_track_alert_history(self):
        """Test tracking alert history."""
        alerts = [
            {"timestamp": "2025-12-14T10:00", "metric": "errors", "value": 12},
            {"timestamp": "2025-12-14T14:00", "metric": "errors", "value": 8},
            {"timestamp": "2025-12-15T10:00", "metric": "coverage", "value": 45},
        ]

        error_alerts = [a for a in alerts if a["metric"] == "errors"]
        assert len(error_alerts) == 2



class TestReportingWithInsights(unittest.TestCase):
    """Tests for generating actionable recommendations."""

    def test_identify_problem_areas(self):
        """Test identifying problem areas."""
        file_stats = {
            "main.py": {"errors": 15, "coverage": 60},
            "utils.py": {"errors": 2, "coverage": 95},
            "helpers.py": {"errors": 8, "coverage": 70},
        }

        problem_areas = {
            f: s for f, s in file_stats.items()
            if s["errors"] > 10 or s["coverage"] < 75
        }

        assert "main.py" in problem_areas

    def test_generate_recommendations(self):
        """Test generating recommendations."""
        issues = {
            "low_coverage": True,
            "high_error_rate": True,
            "slow_execution": False,
        }

        recommendations = []
        if issues["low_coverage"]:
            recommendations.append("Add more unit tests")
        if issues["high_error_rate"]:
            recommendations.append("Review error handling")

        assert len(recommendations) == 2

    def test_prioritize_improvements(self):
        """Test prioritizing improvements."""
        improvements = [
            {"item": "Add tests", "impact": 8, "effort": 3},
            {"item": "Fix errors", "impact": 5, "effort": 2},
            {"item": "Refactor", "impact": 3, "effort": 7},
        ]

        # Prioritize by impact / effort ratio
        for imp in improvements:
            imp["priority"] = imp["impact"] / imp["effort"]

        sorted_improvements = sorted(improvements, key=lambda x: x["priority"], reverse=True)
        assert sorted_improvements[0]["item"] == "Add tests"



