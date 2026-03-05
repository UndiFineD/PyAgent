#!/usr/bin/env python3
try:
    from src.observability.stats.ab_engine import ABSignificanceResult as _ABSignificanceResult
except Exception:
    from src.observability.stats.analysis import ABSignificanceResult as _ABSignificanceResult

ABSignificanceResult = _ABSignificanceResult

__all__ = ["ABSignificanceResult"]
