#!/usr/bin/env python3
try:
    from src.observability.stats import AnnotationManager as _AnnotationManager
except Exception:
    try:
        from src.observability.stats.ab_engine import AnnotationManager as _AnnotationManager
    except Exception:
    from src.observability.stats.analysis import AnnotationManager as _AnnotationManager

AnnotationManager = _AnnotationManager

__all__ = ["AnnotationManager"]
