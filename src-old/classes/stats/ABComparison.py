#!/usr/bin/env python3
try:
    from src.observability.stats.ab_engine import ABComparison as _ABComparison
except Exception:
    from src.observability.stats.analysis import ABComparison as _ABComparison

ABComparison = _ABComparison

__all__ = ["ABComparison"]
