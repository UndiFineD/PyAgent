#!/usr/bin/env python3
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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



from .ABComparison import ABComparison

from typing import Any, Dict
import hashlib



































class ABComparisonEngine:
    """Compare stats between different code versions (A / B testing).

    Provides statistical comparison capabilities for A / B testing
    different code versions.

    Attributes:
        comparisons: Active comparisons.
    """

    def __init__(self) -> None:
        """Initialize A / B comparison engine."""
        self.comparisons: Dict[str, ABComparison] = {}

    def create_comparison(
        self,
        version_a: str,
        version_b: str
    ) -> ABComparison:
        """Create a new A / B comparison.

        Args:
            version_a: Version A identifier.
            version_b: Version B identifier.

        Returns:
            The created comparison.
        """
        comp_id = hashlib.md5(
            f"{version_a}:{version_b}".encode()
        ).hexdigest()[:8]

        comparison = ABComparison(
            id=comp_id,
            version_a=version_a,
            version_b=version_b
        )
        self.comparisons[comp_id] = comparison
        return comparison

    def add_metric(
        self,
        comparison_id: str,
        version: str,
        metric_name: str,
        value: float
    ) -> bool:
        """Add a metric measurement to a comparison.

        Args:
            comparison_id: The comparison ID.
            version: Which version (a or b).
            metric_name: The metric name.
            value: The metric value.

        Returns:
            True if added successfully.
        """
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return False

        if version.lower() == "a":
            comp.metrics_a[metric_name] = value
        elif version.lower() == "b":
            comp.metrics_b[metric_name] = value
        else:
            return False
        return True

    def calculate_winner(
        self,
        comparison_id: str,
        metric_name: str,
        higher_is_better: bool = True
    ) -> Dict[str, Any]:
        """Calculate winner for a specific metric.

        Args:
            comparison_id: The comparison ID.
            metric_name: The metric to compare.
            higher_is_better: Whether higher values are better.

        Returns:
            Comparison results.
        """
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return {"error": "Comparison not found"}

        val_a = comp.metrics_a.get(metric_name, 0)
        val_b = comp.metrics_b.get(metric_name, 0)

        if val_a == val_b:
            winner = "tie"
        elif higher_is_better:
            winner = "a" if val_a > val_b else "b"
        else:
            winner = "a" if val_a < val_b else "b"

        improvement = abs(val_b - val_a) / val_a * 100 if val_a != 0 else 0

        return {
            "metric": metric_name,
            "version_a": val_a,
            "version_b": val_b,
            "winner": winner,
            "improvement_percent": improvement
        }

    def get_summary(self, comparison_id: str) -> Dict[str, Any]:
        """Get comparison summary.

        Args:
            comparison_id: The comparison ID.

        Returns:
            Summary of all metrics compared.
        """
        comp = self.comparisons.get(comparison_id)
        if not comp:
            return {}

        all_metrics = set(comp.metrics_a.keys()) | set(comp.metrics_b.keys())
        return {
            "id": comp.id,
            "version_a": comp.version_a,
            "version_b": comp.version_b,
            "metrics_count": len(all_metrics),
            "metrics_a_count": len(comp.metrics_a),
            "metrics_b_count": len(comp.metrics_b)
        }
