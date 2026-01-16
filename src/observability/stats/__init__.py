#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

"""Observability statistics and metrics collection module.

Provides comprehensive metrics collection, aggregation, and analysis
for monitoring PyAgent system performance and health.
"""

from __future__ import annotations
from src.core.base.Version import VERSION as VERSION

# Phase 317: Structured imports to restore package parity after Synaptic Modularization
from .ObservabilityCore import (
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
    StreamingConfig as StreamingConfig,
    StreamingProtocol as StreamingProtocol,
    DerivedMetric as DerivedMetric,
    StatsNamespace as StatsNamespace,
)

from .MetricsEngine import (
    ObservabilityEngine as ObservabilityEngine,
    TokenCostEngine as TokenCostEngine,
    ModelFallbackEngine as ModelFallbackEngine,
)

from .MetricsCore import (
    DerivedMetricCalculator as DerivedMetricCalculator,
    TokenCostCore as TokenCostCore,
    ModelFallbackCore as ModelFallbackCore,
)

from .Analysis import (
    CorrelationAnalyzer as CorrelationAnalyzer,
)

from .FormulaEngine import (
    FormulaEngine as FormulaEngine,
    FormulaEngineCore as FormulaEngineCore,
    FormulaValidation as FormulaValidation,
)

from .Monitoring import (
    ResourceMonitor as ResourceMonitor,
)

from .Alerting import (
    ThresholdAlertManager as ThresholdAlertManager,
    RetentionEnforcer as RetentionEnforcer,
)

from .RollupEngine import (
    StatsRollupCalculator as StatsRollupCalculator,
    StatsRollup as StatsRollup,
    StatsQueryEngine as StatsQueryEngine,
)

from .PredictionEngine import (
    StatsChangeDetector as StatsChangeDetector,
    StatsForecaster as StatsForecaster,
)

from .ABEngine import (
    ABComparisonEngine as ABComparisonEngine,
    ABComparator as ABComparator,
    ABComparisonResult as ABComparisonResult,
    ABSignificanceResult as ABSignificanceResult,
    ABComparison as ABComparison,
)

from .Exporters import (
    MetricsExporter as MetricsExporter,
    StatsExporter as StatsExporter,
    PrometheusExporter as PrometheusExporter,
    CloudExporter as CloudExporter,
    OTelManager as OTelManager,
    Span as Span,
)
from .StatsAgent import StatsAgent as StatsAgent
from .ReportingAgent import ReportingAgent as ReportingAgent
from .TransparencyAgent import TransparencyAgent as TransparencyAgent

from .API import StatsAPIServer as StatsAPIServer, APIEndpoint as APIEndpoint
from .Streaming import (
    StatsStreamManager as StatsStreamManager,
    StatsStreamer as StatsStreamer,
)
from .Engine import StatsNamespaceManager as StatsNamespaceManager
from .Namespaces import MetricNamespaceManager as MetricNamespaceManager
from .Federation import StatsFederation as StatsFederation
from .Access import StatsAccessController as StatsAccessController
from .StorageEngine import (
    StatsBackupManager as StatsBackupManager,
    StatsSnapshotManager as StatsSnapshotManager,
    StatsCompressor as StatsCompressor,
)
from .SubsEngine import (
    AnnotationManager as AnnotationManager,
    StatsAnnotationManager as StatsAnnotationManager,
    SubscriptionManager as SubscriptionManager,
    StatsSubscriptionManager as StatsSubscriptionManager,
)

__version__ = VERSION
