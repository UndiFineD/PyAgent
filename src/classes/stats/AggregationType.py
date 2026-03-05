#!/usr/bin/env python3
try:
    from src.observability.stats import AggregationType as _AggregationType
except Exception:
    try:
        from src.observability.stats.ab_engine import AggregationType as _AggregationType
    except Exception:
    from src.observability.stats.analysis import AggregationType as _AggregationType

AggregationType = _AggregationType

__all__ = ["AggregationType"]
