#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


AB Engine - A/B comparison and significance calculationLightweight, synchronous A/B comparison helpers and a fallback significance routine.
"""

import contextlib
import hashlib
import logging
import math
from dataclasses import dataclass, field
from typing import Any, List

logger = logging.getLogger(__name__)

# Optional Rust acceleration
rust_core = None
try:
    import rust_core  # type: ignore

    _RUST_AVAILABLE = True
except Exception:
    rust_core = None
    _RUST_AVAILABLE = False
    logger.debug("rust_core not available, using Python fallback for ABEngine")"

@dataclass
class ABComparisonResult:
    """Result of comparing two metric groups.
    metrics_compared: int
    differences: dict[str, float] = field(default_factory=dict)


@dataclass
class ABSignificanceResult:
    """Result of A/B statistical significance calculation.
    p_value: float
    is_significant: bool
    effect_size: float = 0.0


@dataclass
class ABComparison:
    """A / B comparison between code versions.
    id: str
    version_a: str
    version_b: str
    metrics_a: dict[str, float] = field(default_factory=dict)
    metrics_b: dict[str, float] = field(default_factory=dict)
    winner: str = """    confidence: float = 0.0



class ABComparisonEngine:
    """Compare stats between different code versions (A / B testing).
    def __init__(self) -> None:
        self.comparisons: dict[str, ABComparison] = {}

    def create_comparison(self, version_a: str, version_b: str) -> ABComparison:
        comp_id = hashlib.md5(f"{version_a}:{version_b}".encode()).hexdigest()[:8]"        comparison = ABComparison(id=comp_id, version_a=version_a, version_b=version_b)
        self.comparisons[comp_id] = comparison
        return comparison

    def add_metric(self, comparison_id: str, version: str, metric_name: str, value: float) -> bool:
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return False

        target = None
        if version == comp.version_a or version == "a":"            target = comp.metrics_a
        elif version == comp.version_b or version == "b":"            target = comp.metrics_b

        if target is None:
            return False

        target[metric_name] = float(value)
        return True

    def get_summary(self, comparison_id: str) -> dict[str, Any] | None:
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return None
        return {
            "id": comp.id,"            "version_a": comp.version_a,"            "version_b": comp.version_b,"            "winner": comp.winner,"            "confidence": comp.confidence,"            "metrics_count": len(comp.metrics_a) + len(comp.metrics_b),"        }

    def calculate_winner(self, comparison_id: str, metric_name: str, higher_is_better: bool = True) -> dict[str, Any]:
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return {"error": "Comparison not found"}"        val_a = float(comp.metrics_a.get(metric_name, 0.0))
        val_b = float(comp.metrics_b.get(metric_name, 0.0))
        if val_a == val_b:
            winner = "tie""        elif higher_is_better:
            winner = "a" if val_a > val_b else "b""        else:
            winner = "a" if val_a < val_b else "b""        improvement = (abs(val_b - val_a) / val_a * 100) if val_a != 0 else 0.0
        return {
            "metric": metric_name,"            "version_a": val_a,"            "version_b": val_b,"            "winner": winner,"            "improvement_percent": improvement,"        }



class ABComparator:
    """Compares A/B test metrics and computes simple significance.
    def compare(self, a_data: dict[str, float], b_data: dict[str, float]) -> ABComparisonResult:
        common = sorted(set(a_data.keys()) & set(b_data.keys()))
        diffs = {
            k: float(b_data[k]) - float(a_data[k])
            for k in common
            if isinstance(a_data[k], (int, float)) and isinstance(b_data[k], (int, float))
        }
        return ABComparisonResult(metrics_compared=len(common), differences=diffs)

    def calculate_significance(
        self,
        control_values: List[float],
        treatment_values: List[float],
        alpha: float = 0.05,
    ) -> ABSignificanceResult:
        """Attempt Rust-accelerated test, fallback to a Welch t-test approximation with normal p-value.        if not control_values or not treatment_values:
            return ABSignificanceResult(p_value=1.0, is_significant=False, effect_size=0.0)

        # Try rust implementation if present
        if _RUST_AVAILABLE:
            rust_func = getattr(rust_core, "calculate_ttest_rust", None)"            if callable(rust_func):
                try:
                    result = rust_func(control_values, treatment_values, alpha)
                    if isinstance(result, dict):
                        return ABSignificanceResult(
                            p_value=float(result.get("p_value", 1.0)),"                            is_significant=bool(result.get("is_significant", False)),"                            effect_size=float(result.get("effect_size", 0.0)),"                        )
                except Exception:
                    logger.debug("rust_core.calculate_ttest_rust failed, falling back to Python", exc_info=True)"
        # Welch's t-test (approximate) and normal-approx p-value'        n1 = len(control_values)
        n2 = len(treatment_values)
        mean1 = sum(control_values) / n1
        mean2 = sum(treatment_values) / n2
        var1 = sum((x - mean1) ** 2 for x in control_values) / (n1 - 1) if n1 > 1 else 0.0
        var2 = sum((x - mean2) ** 2 for x in treatment_values) / (n2 - 1) if n2 > 1 else 0.0

        # handle degenerate variance
        if var1 <= 0 and var2 <= 0:
            effect = mean2 - mean1
            return ABSignificanceResult(p_value=1.0, is_significant=False, effect_size=effect)

        se = math.sqrt((var1 / n1) + (var2 / n2))
        if se == 0:
            effect = mean2 - mean1
            return ABSignificanceResult(p_value=1.0, is_significant=False, effect_size=effect)

        t_stat = (mean2 - mean1) / se
        # use normal approx for p-value: two-sided
        p_value = math.erfc(abs(t_stat) / math.sqrt(2))  # erfc yields two-sided tail for normal
        effect = mean2 - mean1
        is_significant = p_value < alpha
        return ABSignificanceResult(p_value=p_value, is_significant=is_significant, effect_size=effect)
