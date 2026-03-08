#!/usr/bin/env python3
try:
    from src.observability.stats.ab_engine import ABComparator as _ABComparator
except Exception:
    from src.observability.stats.analysis import ABComparator as _ABComparator

ABComparator = _ABComparator

__all__ = ["ABComparator"]
