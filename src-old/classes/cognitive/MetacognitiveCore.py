#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/cognitive/MetacognitiveCore.description.md

# MetacognitiveCore

**File**: `src\classes\cognitive\MetacognitiveCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 72  
**Complexity**: 5 (moderate)

## Overview

MetacognitiveCore logic for PyAgent.
Pure logic for evaluating reasoning certainty and consistency.
No I/O or side effects.

## Classes (1)

### `MetacognitiveCore`

Pure logic core for metacognitive evaluation and intention prediction.

**Methods** (5):
- `calibrate_confidence_weight(self, reported_conf, actual_correct, current_weight)`
- `predict_next_intent(self, history)`
- `get_prewarm_targets(self, predicted_intent)`
- `calculate_confidence(reasoning_chain)`
- `aggregate_summary(uncertainty_log)`

## Dependencies

**Imports** (3):
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/cognitive/MetacognitiveCore.improvements.md

# Improvements for MetacognitiveCore

**File**: `src\classes\cognitive\MetacognitiveCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 72 lines (small)  
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

"""
MetacognitiveCore logic for PyAgent.
Pure logic for evaluating reasoning certainty and consistency.
No I/O or side effects.
"""

from typing import Any, Dict, List


class MetacognitiveCore:
    """Pure logic core for metacognitive evaluation and intention prediction."""

    def calibrate_confidence_weight(self, reported_conf: float, actual_correct: bool, current_weight: float) -> float:
        """Adjusts the consensus weight of an agent.
        If an agent is 'overconfident' (high conf, wrong result), penalize heavily.
        """
        if not actual_correct and reported_conf > 0.8:
            return max(0.1, current_weight * 0.8) # Overconfidence penalty
        elif actual_correct and reported_conf < 0.4:
            return min(2.0, current_weight * 1.05) # Underconfidence reward
        return current_weight

    def predict_next_intent(self, history: List[Dict[str, Any]]) -> str:
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

    def get_prewarm_targets(self, predicted_intent: str) -> List[str]:
        """Returns agent types that should be pre-warmed."""
        mapping = {
            "CODE_VALIDATION": ["LintingAgent", "UnitTestingAgent"],
            "REPORT_GENERATION": ["DocGenAgent", "SummarizationAgent"]
        }
        return mapping.get(predicted_intent, [])

    @staticmethod
    def calculate_confidence(reasoning_chain: str) -> Dict[str, Any]:
        """Analyzes a reasoning chain for hedge words and length patterns."""
        hedge_words = ["maybe", "perhaps", "i think", "not sure", "unclear", "likely"]
        count = sum(1 for word in hedge_words if word in reasoning_chain.lower())

        uncertainty_score = min(1.0, count / 5.0)
        confidence = 1.0 - uncertainty_score

        return {
            "confidence": confidence,
            "uncertainty_score": uncertainty_score,
            "hedges_detected": count,
            "status": "high_confidence" if confidence > 0.7 else "uncertain"
        }

    @staticmethod
    def aggregate_summary(uncertainty_log: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates average confidence and totals."""
        if not uncertainty_log:
            return {"avg_confidence": 1.0, "total_evaluations": 0}

        avg = sum(e.get("confidence", 0.0) for e in uncertainty_log) / len(uncertainty_log)
        return {
            "avg_confidence": round(avg, 2),
            "total_evaluations": len(uncertainty_log)
        }
