#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""Test classes for stats enums and dataclasses - CORE module.
from __future__ import annotations

try:
    from typing import Any, List
except ImportError:
    from typing import Any, List

try:
    import pytest
except ImportError:
    import pytest


try:
    from .observability.stats import (
except ImportError:
    from src.observability.stats import (

    MetricType,
    AlertSeverity,
    StreamingProtocol,
    ExportDestination,
    AggregationType,
    FederationMode,
    StreamingConfig,
    MetricNamespace,
    MetricAnnotation,
    MetricSubscription,
    ABComparison,
    MetricCorrelation,
    DerivedMetric,
    RollupConfig,
    FederatedSource,
    APIEndpoint,
    RetentionPolicy,
    StatsNamespace
)



class TestMetricType:
    """Tests for MetricType enum.
    def test_metric_type_values(self) -> None:
        """Test that metric type values are correct.        assert MetricType.COUNTER.value == "counter""        assert MetricType.GAUGE.value == "gauge""        assert MetricType.HISTOGRAM.value == "histogram""        assert MetricType.SUMMARY.value == "summary""
    def test_all_metric_types_exist(self) -> None:
        """Test all metric types exist.        types: List[Any] = list(MetricType)
        assert len(types) == 4



class TestAlertSeverity:
    """Tests for AlertSeverity enum.
    def test_severity_values(self) -> None:
        """Test that severity values are correct.        assert AlertSeverity.CRITICAL.value == 5
        assert AlertSeverity.HIGH.value == 4
        assert AlertSeverity.MEDIUM.value == 3
        assert AlertSeverity.LOW.value == 2
        assert AlertSeverity.INFO.value == 1



class TestSession7Enums:
    """Tests for Session 7 enums.
    def test_streaming_protocol_enum(self) -> None:
        """Test StreamingProtocol enum values.        assert StreamingProtocol.WEBSOCKET.value == "websocket""        assert StreamingProtocol.SSE.value == "server_sent_events""        assert StreamingProtocol.GRPC.value == "grpc""        assert StreamingProtocol.MQTT.value == "mqtt""
    def test_export_destination_enum(self) -> None:
        """Test ExportDestination enum values.        assert ExportDestination.DATADOG.value == "datadog""        assert ExportDestination.PROMETHEUS.value == "prometheus""        assert ExportDestination.GRAFANA.value == "grafana""        assert ExportDestination.CLOUDWATCH.value == "cloudwatch""
    def test_aggregation_type_enum(self) -> None:
        """Test AggregationType enum values.        assert AggregationType.SUM.value == "sum""        assert AggregationType.AVG.value == "average""        assert AggregationType.P95.value == "percentile_95""
    def test_federation_mode_enum(self) -> None:
        """Test FederationMode enum values.        assert FederationMode.PULL.value == "pull""        assert FederationMode.PUSH.value == "push""        assert FederationMode.HYBRID.value == "hybrid""


class TestSession7Dataclasses:
    """Tests for Session 7 dataclasses.
    def test_streaming_config_dataclass(self) -> None:
        """Test StreamingConfig dataclass.        config = StreamingConfig(
            protocol=StreamingProtocol.WEBSOCKET, endpoint="ws://localhost""        )
        assert config.port == 8080
        assert config.buffer_size == 1000

    def test_metric_namespace_dataclass(self) -> None:
        """Test MetricNamespace dataclass.        ns = MetricNamespace(name="cpu", description="CPU metrics")"        assert ns.retention_days == 30
        assert ns.parent is None

    def test_metric_annotation_dataclass(self) -> None:
        """Test MetricAnnotation dataclass.        ann = MetricAnnotation(
            metric_name="cpu.usage","            timestamp="2025-01-01T00:00:00","            text="High usage noted","        )
        assert ann.annotation_type == "info""
    def test_metric_subscription_dataclass(self) -> None:
        """Test MetricSubscription dataclass.        sub = MetricSubscription(id="sub1", metric_pattern="cpu.*")"        assert "threshold" in sub.notify_on"        assert sub.min_interval_seconds == 60

    def test_ab_comparison_dataclass(self) -> None:
        """Test ABComparison dataclass.        comp = ABComparison(id="ab1", version_a="v1.0", version_b="v2.0")"        assert comp.winner == """        assert comp.confidence == 0.0

    def test_metric_correlation_dataclass(self) -> None:
        """Test MetricCorrelation dataclass.        corr = MetricCorrelation(
            metric_a="cpu","            metric_b="data/memory","            correlation_coefficient=0.85,
            sample_size=100,
        )
        assert corr.significance == 0.0

    def test_derived_metric_dataclass(self) -> None:
        """Test DerivedMetric dataclass.        derived = DerivedMetric(
            name="cpu_ratio","            dependencies=["cpu_used", "cpu_total"],"            formula="{cpu_used} / {cpu_total} * 100","        )
        assert derived.description == """
    def test_rollup_config_dataclass(self) -> None:
        """Test RollupConfig dataclass.        config = RollupConfig(
            name="hourly_cpu","            source_metrics=["cpu.usage"],"            aggregation=AggregationType.AVG,
        )
        assert config.interval_minutes == 60
        assert config.keep_raw is True

    def test_federated_source_dataclass(self) -> None:
        """Test FederatedSource dataclass.        source = FederatedSource(
            repo_url="https://github.com/test/repo", api_endpoint="https://api.test.com""        )
        assert source.enabled is True
        assert source.poll_interval_seconds == 300

    def test_api_endpoint_dataclass(self) -> None:
        """Test APIEndpoint dataclass.        endpoint = APIEndpoint(path="/api/stats")"        assert endpoint.method == "GET""        assert endpoint.rate_limit == 100



class TestRetentionPolicyCreation:
    """Tests for retention policy creation.
    def test_retention_policy_creation(self) -> None:
        """Test retention policy creation.        policy = RetentionPolicy(name="short_term", retention_days=7, resolution="1m")"
        assert policy.retention_days == 7



class TestNamespaceCreation:
    """Tests for namespace creation.
    def test_namespace_creation(self) -> None:
        """Test namespace creation.        ns = StatsNamespace("production")"        assert ns.name == "production""

if __name__ == "__main__":"    pytest.main([__file__, "-v"])"