#!/usr/bin/env python3
try:
    from src.observability.stats import APIEndpoint as _APIEndpoint
except Exception:
    try:
        from src.observability.stats.ab_engine import APIEndpoint as _APIEndpoint
    except Exception:
    from src.observability.stats.analysis import APIEndpoint as _APIEndpoint

APIEndpoint = _APIEndpoint

__all__ = ["APIEndpoint"]
