#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
<<<<<<< HEAD

"""Lazy-loading entry point for observability.stats."""

=======
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
from __future__ import annotations
from typing import Any, TYPE_CHECKING
from src.core.base.lifecycle.version import VERSION
from src.core.lazy_loader import ModuleLazyLoader

if TYPE_CHECKING:
    from .ab_engine import (
        ABComparator, ABComparison, ABComparisonEngine,
        ABComparisonResult, ABSignificanceResult
    )
    from .api import APIEndpoint, StatsAPIServer
    from .observability_core import (
        AggregationType, Alert, AlertSeverity, DerivedMetric,
        ExportDestination, FederatedSource, FederationMode,
        Metric, MetricAnnotation, MetricCorrelation, MetricNamespace,
        MetricSnapshot, MetricSubscription, MetricType, RetentionPolicy,
        RollupConfig, StatsNamespace, StreamingConfig, StreamingProtocol, Threshold
    )
    from .subs_engine import (
        AnnotationManager, StatsAnnotationManager, StatsSubscriptionManager,
        SubscriptionManager
    )
    from .exporters import (
        CloudExporter, MetricsExporter, OTelManager, PrometheusExporter,
        Span, StatsExporter
    )
    from .analysis import CorrelationAnalyzer
    from .metrics_core import DerivedMetricCalculator, ModelFallbackCore, TokenCostCore
    from .namespaces import MetricNamespaceManager
    from .metrics_engine import (
        ModelFallbackEngine, ObservabilityEngine, TokenCostEngine
    )
    from .reporting_agent import ReportingAgent
    from .monitoring import ResourceMonitor
    from .alerting import RetentionEnforcer, ThresholdAlertManager
    from .access import StatsAccessController
    from .stats_agent import StatsAgent
    from .formula_engine import (
        FormulaEngine, FormulaEngineCore, FormulaValidation
    )
    from .storage_engine import (
        StatsBackupManager, StatsCompressor, StatsSnapshotManager
    )
    from .prediction_engine import StatsChangeDetector, StatsForecaster
    from .federation import StatsFederation
    from .engine import StatsNamespaceManager
    from .rollup_engine import (
        StatsQueryEngine, StatsRollup, StatsRollupCalculator
    )
    from .streaming import StatsStreamManager, StatsStreamer
    from .transparency_agent import TransparencyAgent

<<<<<<< HEAD
_LAZY_REGISTRY = {
    "ABComparator": ("src.observability.stats.ab_engine", "ABComparator"),
    "ABComparison": ("src.observability.stats.ab_engine", "ABComparison"),
    "ABComparisonEngine": ("src.observability.stats.ab_engine", "ABComparisonEngine"),
    "ABComparisonResult": ("src.observability.stats.ab_engine", "ABComparisonResult"),
    "ABSignificanceResult": ("src.observability.stats.ab_engine", "ABSignificanceResult"),
    "APIEndpoint": ("src.observability.stats.api", "APIEndpoint"),
    "AggregationType": ("src.observability.stats.observability_core", "AggregationType"),
    "Alert": ("src.observability.stats.observability_core", "Alert"),
    "AlertSeverity": ("src.observability.stats.observability_core", "AlertSeverity"),
    "AnnotationManager": ("src.observability.stats.subs_engine", "AnnotationManager"),
    "CloudExporter": ("src.observability.stats.exporters", "CloudExporter"),
    "CorrelationAnalyzer": ("src.observability.stats.analysis", "CorrelationAnalyzer"),
    "DerivedMetric": ("src.observability.stats.observability_core", "DerivedMetric"),
    "DerivedMetricCalculator": ("src.observability.stats.metrics_core", "DerivedMetricCalculator"),
    "ExportDestination": ("src.observability.stats.observability_core", "ExportDestination"),
    "FederatedSource": ("src.observability.stats.observability_core", "FederatedSource"),
    "FederationMode": ("src.observability.stats.observability_core", "FederationMode"),
    "FormulaEngine": ("src.observability.stats.formula_engine", "FormulaEngine"),
    "FormulaEngineCore": ("src.observability.stats.formula_engine", "FormulaEngineCore"),
    "FormulaValidation": ("src.observability.stats.formula_engine", "FormulaValidation"),
    "Metric": ("src.observability.stats.observability_core", "Metric"),
    "MetricAnnotation": ("src.observability.stats.observability_core", "MetricAnnotation"),
    "MetricCorrelation": ("src.observability.stats.observability_core", "MetricCorrelation"),
    "MetricNamespace": ("src.observability.stats.observability_core", "MetricNamespace"),
    "MetricNamespaceManager": ("src.observability.stats.namespaces", "MetricNamespaceManager"),
    "MetricSnapshot": ("src.observability.stats.observability_core", "MetricSnapshot"),
    "MetricSubscription": ("src.observability.stats.observability_core", "MetricSubscription"),
    "MetricType": ("src.observability.stats.observability_core", "MetricType"),
    "MetricsExporter": ("src.observability.stats.exporters", "MetricsExporter"),
    "ModelFallbackCore": ("src.observability.stats.metrics_core", "ModelFallbackCore"),
    "ModelFallbackEngine": ("src.observability.stats.metrics_engine", "ModelFallbackEngine"),
    "OTelManager": ("src.observability.stats.exporters", "OTelManager"),
    "ObservabilityEngine": ("src.observability.stats.metrics_engine", "ObservabilityEngine"),
    "PrometheusExporter": ("src.observability.stats.exporters", "PrometheusExporter"),
    "ReportingAgent": ("src.observability.stats.reporting_agent", "ReportingAgent"),
    "ResourceMonitor": ("src.observability.stats.monitoring", "ResourceMonitor"),
    "RetentionEnforcer": ("src.observability.stats.alerting", "RetentionEnforcer"),
    "RetentionPolicy": ("src.observability.stats.observability_core", "RetentionPolicy"),
    "RollupConfig": ("src.observability.stats.observability_core", "RollupConfig"),
    "Span": ("src.observability.stats.exporters", "Span"),
    "StatsAPIServer": ("src.observability.stats.api", "StatsAPIServer"),
    "StatsAccessController": ("src.observability.stats.access", "StatsAccessController"),
    "StatsAgent": ("src.observability.stats.stats_agent", "StatsAgent"),
    "StatsAnnotationManager": ("src.observability.stats.subs_engine", "StatsAnnotationManager"),
    "StatsBackupManager": ("src.observability.stats.storage_engine", "StatsBackupManager"),
    "StatsChangeDetector": ("src.observability.stats.prediction_engine", "StatsChangeDetector"),
    "StatsCompressor": ("src.observability.stats.storage_engine", "StatsCompressor"),
    "StatsExporter": ("src.observability.stats.exporters", "StatsExporter"),
    "StatsFederation": ("src.observability.stats.federation", "StatsFederation"),
    "StatsForecaster": ("src.observability.stats.prediction_engine", "StatsForecaster"),
    "StatsNamespace": ("src.observability.stats.observability_core", "StatsNamespace"),
    "StatsNamespaceManager": ("src.observability.stats.engine", "StatsNamespaceManager"),
    "StatsQueryEngine": ("src.observability.stats.rollup_engine", "StatsQueryEngine"),
    "StatsRollup": ("src.observability.stats.rollup_engine", "StatsRollup"),
    "StatsRollupCalculator": ("src.observability.stats.rollup_engine", "StatsRollupCalculator"),
    "StatsSnapshotManager": ("src.observability.stats.storage_engine", "StatsSnapshotManager"),
    "StatsStreamManager": ("src.observability.stats.streaming", "StatsStreamManager"),
    "StatsStreamer": ("src.observability.stats.streaming", "StatsStreamer"),
    "StatsSubscriptionManager": ("src.observability.stats.subs_engine", "StatsSubscriptionManager"),
    "StreamingConfig": ("src.observability.stats.observability_core", "StreamingConfig"),
    "StreamingProtocol": ("src.observability.stats.observability_core", "StreamingProtocol"),
    "SubscriptionManager": ("src.observability.stats.subs_engine", "SubscriptionManager"),
    "Threshold": ("src.observability.stats.observability_core", "Threshold"),
    "ThresholdAlertManager": ("src.observability.stats.alerting", "ThresholdAlertManager"),
    "TokenCostCore": ("src.observability.stats.metrics_core", "TokenCostCore"),
    "TokenCostEngine": ("src.observability.stats.metrics_engine", "TokenCostEngine"),
    "TransparencyAgent": ("src.observability.stats.transparency_agent", "TransparencyAgent"),
}

_loader = ModuleLazyLoader(_LAZY_REGISTRY)

def __getattr__(name: str) -> Any:
    return _loader.load(name)

__all__ = ["VERSION"] + list(_LAZY_REGISTRY.keys())
=======
from .observability_core import *
from .metrics_engine import *
from .exporters import *
from .StatsAgent import StatsAgent
from .ReportingAgent import ReportingAgent
from .TransparencyAgent import TransparencyAgent
>>>>>>> a0089ee17 (Phase 154 Complete: Stats & Observability Consolidation (77 files -> 3 modules))
