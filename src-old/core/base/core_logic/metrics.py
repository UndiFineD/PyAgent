# Copyright 2026 PyAgent Authors
"""
LLM_CONTEXT_START

## Source: src-old/core/base/core_logic/metrics.description.md

# metrics

**File**: `src\core\base\core_logic\metrics.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 72  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for metrics.

## Classes (1)

### `MetricsCore`

Class MetricsCore implementation.

**Methods** (6):
- `calculate_anchoring_strength(self, result, context_pool)`
- `verify_self(self, result, anchoring_score)`
- `assess_response_quality(self, response, metadata)`
- `_assess_quality_python(self, response, metadata)`
- `calculate_priority_score(self, priority, urgency)`
- `calculate_token_estimate(self, text, chars_per_token)`

## Dependencies

**Imports** (10):
- `logging`
- `rust_core`
- `src.core.base.AgentVerification.AgentVerifier`
- `src.core.base.models.AgentPriority`
- `src.core.base.models.ResponseQuality`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/core/base/core_logic/metrics.improvements.md

# Improvements for metrics

**File**: `src\core\base\core_logic\metrics.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 72 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: MetricsCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `metrics_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import logging
from typing import Any, Dict, Optional, List, Tuple
from src.core.base.models import ResponseQuality, AgentPriority
from src.core.base.AgentVerification import AgentVerifier

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)


class MetricsCore:
    def calculate_anchoring_strength(
        self, result: str, context_pool: Optional[Dict[str, Any]] = None
    ) -> float:
        """Calculate the 'Anchoring Strength' metric (Stanford Research 2025)."""
        return AgentVerifier.calculate_anchoring_strength(result, context_pool or {})

    def verify_self(self, result: str, anchoring_score: float) -> Tuple[bool, str]:
        """Self-verification layer."""
        return AgentVerifier.verify_self(result, anchoring_score)

    def assess_response_quality(
        self, response: str, metadata: Optional[Dict[str, Any]] = None
    ) -> ResponseQuality:
        """Assess the quality of a response."""
        if rc:
            try:
                final_score = rc.assess_response_quality(response, metadata)
            except Exception:
                final_score = self._assess_quality_python(response, metadata)
        else:
            final_score = self._assess_quality_python(response, metadata)

        if final_score >= 0.9:
            return ResponseQuality.EXCELLENT
        elif final_score >= 0.7:
            return ResponseQuality.GOOD
        elif final_score >= 0.5:
            return ResponseQuality.ACCEPTABLE
        elif final_score >= 0.3:
            return ResponseQuality.POOR
        else:
            return ResponseQuality.INVALID

    def _assess_quality_python(
        self, response: str, metadata: Optional[Dict[str, Any]] = None
    ) -> float:
        """Fallback Python implementation of quality assessment."""
        if metadata is None:
            metadata = {}
        score = 0.5
        if len(response) > 100:
            score += 0.1
        if "error" not in response.lower() and "fail" not in response.lower():
            score += 0.1
        if metadata.get("has_references"):
            score += 0.1
        if metadata.get("is_complete"):
            score += 0.1
        return min(1.0, score)

    def calculate_priority_score(
        self, priority: AgentPriority, urgency: float
    ) -> float:
        """Calculate effective priority score."""
        priority_base = {
            AgentPriority.LOW: 0.2,
            AgentPriority.NORMAL: 0.5,
            AgentPriority.HIGH: 0.8,
            AgentPriority.CRITICAL: 1.0,
        }.get(priority, 0.5)

        if rc:
            try:
                return rc.calculate_priority_score(priority_base, urgency)
            except Exception:
                pass
        return (priority_base * 0.7) + (urgency * 0.3)

    def calculate_token_estimate(self, text: str, chars_per_token: float = 4.0) -> int:
        """Estimate token count."""
        if rc:
            try:
                return rc.calculate_token_estimate(text, chars_per_token)
            except Exception:
                pass
        return max(1, int(len(text) / chars_per_token))
