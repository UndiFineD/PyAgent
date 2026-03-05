#!/usr/bin/env python3
try:
    from src.observability.stats.ab_engine import ABComparisonEngine as _ABComparisonEngine
except Exception:
    from src.observability.stats.analysis import ABComparisonEngine as _ABComparisonEngine

ABComparisonEngine = _ABComparisonEngine

__all__ = ["ABComparisonEngine"]
