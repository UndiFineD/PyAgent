#!/usr/bin/env python3
try:
    from src.core.base.common.types.accessibility_issue_type import (
        AccessibilityIssueType as _AccessibilityIssueType,
    )
except Exception:

    class _AccessibilityIssueType:  # fallback placeholder
        pass


AccessibilityIssueType = _AccessibilityIssueType

__all__ = ["AccessibilityIssueType"]
