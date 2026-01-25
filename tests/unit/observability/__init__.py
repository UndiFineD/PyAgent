#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""Extracted test classes from test_agent_stats.py."""

__all__ = [
    "TestABComparisonEngine",
    "TestAggregation",
    "TestAggregationAdvanced",
    "TestAlertSeverity",
    "TestAlerting",
    "TestAnnotationManager",
    "TestAnomalyDetection",
    "TestBenchmarking",
    "TestBenchmarkingAdvanced",
    "TestCSVExport",
    "TestCaching",
    "TestCachingAdvanced",
    "TestCloudExporter",
    "TestComparison",
    "TestComparisonReports",
    "TestCompression",
    "TestCorrelationAnalyzer",
    "TestCoverageMetrics",
    "TestCustomMetrics",
    "TestDerivedMetricCalculator",
    "TestDocstrings",
    "TestEdgeCases",
    "TestExportFormats",
    "TestExportFormatsAdvanced",
    "TestFiltering",
    "TestForecasting",
    "TestIntegration",
    "TestIntegrationAdvanced",
    "TestMetricFiltering",
    "TestMetricNamespaceManager",
    "TestMetricType",
    "TestPathLibUsage",
    "TestPerformanceMetrics",
    "TestRealTimeStatsStreaming",
    "TestReporting",
    "TestReportingWithInsights",
    "TestRetentionPolicies",
    "TestSession7Dataclasses",
    "TestSession7Enums",
    "TestSnapshots",
    "TestStatisticalSummaries",
    "TestStatisticalSummariesAdvanced",
    "TestStatsABComparison",
    "TestStatsAPIServer",
    "TestStatsAccessControl",
    "TestStatsAgent",
    "TestStatsAnnotationPersistence",
    "TestStatsBackupAndRestore",
    "TestStatsChangeNotificationSystem",
    "TestStatsCompressionAlgorithms",
    "TestStatsExportToMonitoringPlatforms",
    "TestStatsFederation",
    "TestStatsFederationAcrossSources",
    "TestStatsForecastingAccuracy",
    "TestStatsMetricFormulaCalculation",
    "TestStatsNamespaceIsolation",
    "TestStatsQueryPerformance",
    "TestStatsRetentionPolicyEnforcement",
    "TestStatsRollup",
    "TestStatsRollupCalculations",
    "TestStatsSnapshotCreationAndRestore",
    "TestStatsStreamer",
    "TestStatsSubscriptionAndNotification",
    "TestStatsThresholdAlerting",
    "TestSubscriptionManager",
    "TestThresholdsAndAlerting",
    "TestTimeSeries",
    "TestTimeSeriesStorage",
    "TestTrendAnalysis",
    "TestTrendAnalysisAdvanced",
    "TestValidation",
    "TestVisualization",
    "TestVisualizationAdvanced",
    "TestVisualizationGeneration",
]

from .test_stats_unit import *  # noqa: F401, F403
from .test_stats_integration import *  # noqa: F401, F403
from .advanced import *  # noqa: F401, F403
from .edge_cases import *  # noqa: F401, F403
from .test_stats_performance import *  # noqa: F401, F403
