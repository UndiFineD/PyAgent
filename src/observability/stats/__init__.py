#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

"""Observability statistics and metrics collection module.

Provides comprehensive metrics collection, aggregation, and analysis
for monitoring PyAgent system performance and health.
"""

from __future__ import annotations
from src.core.base.version import VERSION as VERSION
from .observability_core import (
    Metric as Metric,
    MetricType as MetricType,
    Alert as Alert,
    AlertSeverity as AlertSeverity,
    Threshold as Threshold,
    RetentionPolicy as RetentionPolicy,
    MetricSnapshot as MetricSnapshot,
    AggregationType as AggregationType,
    MetricNamespace as MetricNamespace,
    MetricAnnotation as MetricAnnotation,
    MetricCorrelation as MetricCorrelation,
    MetricSubscription as MetricSubscription,
    ExportDestination as ExportDestination,
    FederatedSource as FederatedSource,
    FederationMode as FederationMode,
    RollupConfig as RollupConfig,
    StreamingConfig as StreamingConfig
)
from .metrics_engine import (
    ObservabilityEngine as ObservabilityEngine,
    DerivedMetricCalculator as DerivedMetricCalculator,
    CorrelationAnalyzer as CorrelationAnalyzer,
    FormulaEngine as FormulaEngine,
    FormulaEngineCore as FormulaEngineCore,
    FormulaValidation as FormulaValidation,
    ResourceMonitor as ResourceMonitor,
    RetentionEnforcer as RetentionEnforcer,
    TokenCostEngine as TokenCostEngine,
    TokenCostCore as TokenCostCore,
    ModelFallbackEngine as ModelFallbackEngine,
    ModelFallbackCore as ModelFallbackCore,
    StatsRollupCalculator as StatsRollupCalculator,
    StatsRollup as StatsRollup,
    StatsChangeDetector as StatsChangeDetector,
    StatsForecaster as StatsForecaster,
    StatsQueryEngine as StatsQueryEngine,
    ABComparisonEngine as ABComparisonEngine,
    ABComparator as ABComparator,
    ABComparisonResult as ABComparisonResult,
    ABSignificanceResult as ABSignificanceResult
)
from .exporters import (
    MetricsExporter as MetricsExporter,
    StatsExporter as StatsExporter,
    PrometheusExporter as PrometheusExporter,
    CloudExporter as CloudExporter,
    OTelManager as OTelManager,
    Span as Span
)
from .StatsAgent import StatsAgent as StatsAgent
from .ReportingAgent import ReportingAgent as ReportingAgent
from .TransparencyAgent import TransparencyAgent as TransparencyAgent

__version__ = VERSION