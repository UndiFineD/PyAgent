"""
LLM_CONTEXT_START

## Source: src-old/classes/stats/__init__.description.md

# __init__

**File**: `src\classes\stats\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 60 imports  
**Lines**: 70  
**Complexity**: 0 (simple)

## Overview

Auto-generated module exports.

## Dependencies

**Imports** (60):
- `ABComparator.ABComparator`
- `ABComparison.ABComparison`
- `ABComparisonEngine.ABComparisonEngine`
- `ABComparisonResult.ABComparisonResult`
- `ABSignificanceResult.ABSignificanceResult`
- `APIEndpoint.APIEndpoint`
- `AggregationType.AggregationType`
- `Alert.Alert`
- `AlertSeverity.AlertSeverity`
- `AnnotationManager.AnnotationManager`
- `CloudExporter.CloudExporter`
- `CorrelationAnalyzer.CorrelationAnalyzer`
- `DerivedMetric.DerivedMetric`
- `DerivedMetricCalculator.DerivedMetricCalculator`
- `ExportDestination.ExportDestination`
- ... and 45 more

---
*Auto-generated documentation*
## Source: src-old/classes/stats/__init__.improvements.md

# Improvements for __init__

**File**: `src\classes\stats\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 70 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

"""Auto-generated module exports.

Prefer the observability implementation where available; fall back to
the local auto-generated shims when needed.
"""


try:
    # Import the observability stats module but only copy attributes
    # that can be accessed without raising (skip heavy deps).
    from importlib import import_module

    _obs = import_module("src.observability.stats")
    _names = [
        "ABComparator",
        "ABComparison",
        "ABComparisonEngine",
        "ABComparisonResult",
        "ABSignificanceResult",
        "APIEndpoint",
        "AggregationType",
        "Alert",
        "AlertSeverity",
        "AnnotationManager",
        "CloudExporter",
        "CorrelationAnalyzer",
        "DerivedMetric",
        "DerivedMetricCalculator",
        "ExportDestination",
        "FederatedSource",
        "FederationMode",
        "FormulaEngine",
        "FormulaValidation",
        "Metric",
        "MetricAnnotation",
        "MetricCorrelation",
        "MetricNamespace",
        "MetricNamespaceManager",
        "MetricSnapshot",
        "MetricSubscription",
        "MetricType",
        "RetentionEnforcer",
        "RetentionPolicy",
        "RollupConfig",
        "StatsAPIServer",
        "StatsAccessController",
        "StatsAgent",
        "StatsAnnotationManager",
        "StatsBackup",
        "StatsBackupManager",
        "StatsChangeDetector",
        "StatsCompressor",
        "StatsExporter",
        "StatsFederation",
        "StatsForecaster",
        "StatsNamespace",
        "StatsNamespaceManager",
        "StatsQueryEngine",
        "StatsRollup",
        "StatsRollupCalculator",
        "StatsSnapshot",
        "StatsSnapshotManager",
        "StatsStream",
        "StatsStreamManager",
        "StatsStreamer",
        "StatsSubscription",
        "StatsSubscriptionManager",
        "StreamingConfig",
        "StreamingProtocol",
        "SubscriptionManager",
        "Threshold",
        "ThresholdAlert",
        "ThresholdAlertManager",
    ]

    _loaded = False
    for _n in _names:
        try:
            _val = getattr(_obs, _n)
        except Exception:
            continue
        globals()[_n] = _val
        _loaded = True

    if _loaded:
        __all__ = [n for n in _names if n in globals()]
    else:
        raise ImportError("no observability stats names available")
except Exception:
    # Observability stats package not available; provide a minimal fallback namespace
    # to avoid import-time failures during test collection. Tests depending on full
    # observability implementations should enable the optional package.
    __all__ = []
