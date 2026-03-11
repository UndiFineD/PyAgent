r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/core/StabilityCore.description.md

# StabilityCore

**File**: `src\observability\stats\core\StabilityCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 3 imports  
**Lines**: 43  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for StabilityCore.

## Classes (2)

### `FleetMetrics`

Class FleetMetrics implementation.

### `StabilityCore`

Pure logic for calculating fleet stability and reasoning coherence.
Integrates SAE activation metrics and error trends into a unified score.

**Methods** (3):
- `calculate_stability_score(self, metrics, sae_anomalies)`
- `is_in_stasis(self, score_history)`
- `get_healing_threshold(self, stability_score)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `dataclasses.dataclass`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/core/StabilityCore.improvements.md

# Improvements for StabilityCore

**File**: `src\observability\stats\core\StabilityCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 43 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: FleetMetrics

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StabilityCore_test.py` with pytest tests

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

from dataclasses import dataclass


@dataclass(frozen=True)
class FleetMetrics:
    avg_error_rate: float
    total_token_out: int
    active_agent_count: int
    latency_p95: float


class StabilityCore:
    """Pure logic for calculating fleet stability and reasoning coherence.
    Integrates SAE activation metrics and error trends into a unified score.
    """

    def calculate_stability_score(
        self, metrics: FleetMetrics, sae_anomalies: int
    ) -> float:
        """Calculates a stability score from 0.0 to 1.0."""
        # Baseline: 1.0
        # Deductions: error_rate * 5.0, sae_anomalies * 0.05, latency_p95 overhead

        score = 1.0
        score -= metrics.avg_error_rate * 5.0
        score -= sae_anomalies * 0.05

        latency_penalty = max(0.0, (metrics.latency_p95 - 2000) / 10000)
        score -= latency_penalty

        return min(max(score, 0.0), 1.0)

    def is_in_stasis(self, score_history: list[float]) -> bool:
        """Determines if the swarm is in 'Digital Stasis' (too rigid)."""
        if len(score_history) < 10:
            return False
        variance = sum(
            (x - sum(score_history) / len(score_history)) ** 2 for x in score_history
        ) / len(score_history)
        return variance < 0.0001  # Minimal change indicates stasis

    def get_healing_threshold(self, stability_score: float) -> float:
        """Returns the threshold for triggering self-healing subroutines."""
        if stability_score < 0.3:
            return 0.9  # Aggressive healing
        return 0.5
