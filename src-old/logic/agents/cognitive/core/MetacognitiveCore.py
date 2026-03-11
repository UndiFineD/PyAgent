#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/core/MetacognitiveCore.description.md

# MetacognitiveCore

**File**: `src\\logic\agents\\cognitive\\core\\MetacognitiveCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 121  
**Complexity**: 5 (moderate)

## Overview

MetacognitiveCore logic for PyAgent.
Pure logic for evaluating reasoning certainty and consistency.
No I/O or side effects.

## Classes (1)

### `MetacognitiveCore`

Pure logic core for metacognitive evaluation and intention prediction.

Phase 14 Rust Optimizations:
- count_hedge_words_rust: Fast multi-pattern matching for hedge word detection
- predict_intent_rust: Optimized pattern-based intent classification

**Methods** (5):
- `calibrate_confidence_weight(self, reported_conf, actual_correct, current_weight)`
- `predict_next_intent(self, history)`
- `get_prewarm_targets(self, predicted_intent)`
- `calculate_confidence(reasoning_chain)`
- `aggregate_summary(uncertainty_log)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `logging`
- `rust_core`
- `src.core.base.Version.VERSION`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/core/MetacognitiveCore.improvements.md

# Improvements for MetacognitiveCore

**File**: `src\\logic\agents\\cognitive\\core\\MetacognitiveCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 121 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MetacognitiveCore_test.py` with pytest tests

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

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
MetacognitiveCore logic for PyAgent.
Pure logic for evaluating reasoning certainty and consistency.
No I/O or side effects.
"""

import logging
from typing import Any

from src.core.base.Version import VERSION

__version__ = VERSION

logger = logging.getLogger(__name__)

try:
    import rust_core as rc

    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False


class MetacognitiveCore:
    """Pure logic core for metacognitive evaluation and intention prediction.

    Phase 14 Rust Optimizations:
    - count_hedge_words_rust: Fast multi-pattern matching for hedge word detection
    - predict_intent_rust: Optimized pattern-based intent classification
    """

    def calibrate_confidence_weight(
        self, reported_conf: float, actual_correct: bool, current_weight: float
    ) -> float:
        """Adjusts the consensus weight of an agent.
        If an agent is 'overconfident' (high conf, wrong result), penalize heavily.
        """
        if not actual_correct and reported_conf > 0.8:
            return max(0.1, current_weight * 0.8)  # Overconfidence penalty
        elif actual_correct and reported_conf < 0.4:
            return min(2.0, current_weight * 1.05)  # Underconfidence reward
        return current_weight

    def predict_next_intent(self, history: list[dict[str, Any]]) -> str:
        """Heuristic-based intent prediction based on recent sequence.
        """
        if not history:
            return "GENERAL_INQUIRY"
        last_actions = [h.get("action", "").lower() for h in history[-3:]]
        if "edit" in last_actions or "create" in last_actions:
            return "CODE_VALIDATION"
        if "search" in last_actions or "research" in last_actions:
            return "REPORT_GENERATION"
        return "CONTINUATION"

    def get_prewarm_targets(self, predicted_intent: str) -> list[str]:
        """Returns agent types that should be pre-warmed."""
        mapping = {
            "CODE_VALIDATION": ["LintingAgent", "UnitTestingAgent"],
            "REPORT_GENERATION": ["DocGenAgent", "SummarizationAgent"],
        }
        return mapping.get(predicted_intent, [])

    @staticmethod
    def calculate_confidence(reasoning_chain: str) -> dict[str, Any]:
        """Analyzes a reasoning chain for hedge words and length patterns.

        Uses Rust-accelerated multi-pattern matching when available.
        """
        hedge_words = ["maybe", "perhaps", "i think", "not sure", "unclear", "likely"]

        # Rust-accelerated hedge word counting
        if RUST_AVAILABLE and hasattr(rc, "count_hedge_words_rust"):
            try:
                count = rc.count_hedge_words_rust(reasoning_chain.lower(), hedge_words)
            except Exception as e:
                logger.debug(
                    f"Rust count_hedge_words failed: {e}, using Python fallback"
                )
                count = sum(
                    1 for word in hedge_words if word in reasoning_chain.lower()
                )
        else:
            count = sum(1 for word in hedge_words if word in reasoning_chain.lower())

        uncertainty_score = min(1.0, count / 5.0)
        confidence = 1.0 - uncertainty_score

        return {
            "confidence": confidence,
            "uncertainty_score": uncertainty_score,
            "hedges_detected": count,
            "status": "high_confidence" if confidence > 0.7 else "uncertain",
        }

    @staticmethod
    def aggregate_summary(uncertainty_log: list[dict[str, Any]]) -> dict[str, Any]:
        """Calculates average confidence and totals."""
        if not uncertainty_log:
            return {"avg_confidence": 1.0, "total_evaluations": 0}

        avg = sum(e.get("confidence", 0.0) for e in uncertainty_log) / len(
            uncertainty_log
        )
        return {
            "avg_confidence": round(avg, 2),
            "total_evaluations": len(uncertainty_log),
        }
