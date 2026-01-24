#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

"""Observability statistics and metrics collection module.

Provides comprehensive metrics collection, aggregation, and analysis
for monitoring PyAgent system performance and health.
"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .ab_engine import (ABComparator, ABComparison, ABComparisonEngine,  # noqa: F401
                        ABComparisonResult, ABSignificanceResult)
from .access import StatsAccessController  # noqa: F401
from .alerting import RetentionEnforcer, ThresholdAlertManager  # noqa: F401
from .analysis import CorrelationAnalyzer  # noqa: F401
from .api import APIEndpoint, StatsAPIServer  # noqa: F401
from .engine import StatsNamespaceManager  # noqa: F401
from .exporters import (CloudExporter, MetricsExporter, OTelManager,  # noqa: F401
                        PrometheusExporter, Span, StatsExporter)
from .federation import StatsFederation  # noqa: F401
from .formula_engine import FormulaEngine, FormulaEngineCore, FormulaValidation  # noqa: F401
from .metrics_core import (DerivedMetricCalculator, ModelFallbackCore,  # noqa: F401
                           TokenCostCore)
from .metrics_engine import (ModelFallbackEngine, ObservabilityEngine,  # noqa: F401
                             TokenCostEngine)
from .monitoring import ResourceMonitor  # noqa: F401
from .namespaces import MetricNamespaceManager  # noqa: F401
# Phase 317: Structured imports to restore package parity after Synaptic Modularization
from .observability_core import (AggregationType, Alert, AlertSeverity,  # noqa: F401
                                 DerivedMetric, ExportDestination,
                                 FederatedSource, FederationMode, Metric,
                                 MetricAnnotation, MetricCorrelation,
                                 MetricNamespace, MetricSnapshot,
                                 MetricSubscription, MetricType,
                                 RetentionPolicy, RollupConfig, StatsNamespace,
                                 StreamingConfig, StreamingProtocol, Threshold)
from .prediction_engine import StatsChangeDetector, StatsForecaster  # noqa: F401
from .reporting_agent import ReportingAgent  # noqa: F401
from .rollup_engine import StatsQueryEngine, StatsRollup, StatsRollupCalculator  # noqa: F401
from .stats_agent import StatsAgent  # noqa: F401
from .storage_engine import (StatsBackupManager, StatsCompressor,  # noqa: F401
                             StatsSnapshotManager)
from .streaming import StatsStreamer, StatsStreamManager  # noqa: F401
from .subs_engine import (AnnotationManager, StatsAnnotationManager,  # noqa: F401
                          StatsSubscriptionManager, SubscriptionManager)
from .transparency_agent import TransparencyAgent  # noqa: F401

__version__ = VERSION

__all__ = [
    "VERSION",
    "Metric",
    "MetricType",
    "Alert",
    "AlertSeverity",
    "Threshold",
    "RetentionPolicy",
    "MetricSnapshot",
    "AggregationType",
    "MetricNamespace",
    "MetricAnnotation",
    "MetricCorrelation",
    "MetricSubscription",
    "ExportDestination",
    "FederatedSource",
    "FederationMode",
    "RollupConfig",
    "StreamingConfig",
    "StreamingProtocol",
    "DerivedMetric",
    "StatsNamespace",
    "ObservabilityEngine",
    "TokenCostEngine",
    "ModelFallbackEngine",
    "DerivedMetricCalculator",
    "TokenCostCore",
    "ModelFallbackCore",
    "CorrelationAnalyzer",
    "FormulaEngine",
    "FormulaEngineCore",
    "FormulaValidation",
    "ResourceMonitor",
    "ThresholdAlertManager",
    "RetentionEnforcer",
    "StatsRollupCalculator",
    "StatsRollup",
    "StatsQueryEngine",
    "StatsChangeDetector",
    "StatsForecaster",
    "ABComparisonEngine",
    "ABComparator",
    "ABComparisonResult",
    "ABSignificanceResult",
    "ABComparison",
    "MetricsExporter",
    "StatsExporter",
    "PrometheusExporter",
    "CloudExporter",
    "OTelManager",
    "Span",
    "StatsAgent",
    "ReportingAgent",
    "TransparencyAgent",
    "StatsAPIServer",
    "APIEndpoint",
    "StatsStreamManager",
    "StatsStreamer",
    "StatsNamespaceManager",
    "MetricNamespaceManager",
    "StatsFederation",
    "StatsAccessController",
    "StatsBackupManager",
    "StatsSnapshotManager",
    "StatsCompressor",
    "AnnotationManager",
    "StatsAnnotationManager",
    "SubscriptionManager",
    "StatsSubscriptionManager",
]
