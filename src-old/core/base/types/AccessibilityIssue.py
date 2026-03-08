#!/usr/bin/env python3
try:
    from src.core.base.common.types.accessibility_issue import (
        AccessibilityIssue as _AccessibilityIssue,
    )
except Exception:

    class _AccessibilityIssue:  # fallback placeholder
        pass


AccessibilityIssue = _AccessibilityIssue

__all__ = ["AccessibilityIssue"]
