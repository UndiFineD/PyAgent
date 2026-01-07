#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .DerivedMetric import DerivedMetric

from typing import Dict, List, Optional
import logging
import math

class DerivedMetricCalculator:
    """Calculate derived metrics from dependencies.

    Supports creating calculated metrics based on formulas
    that reference other metrics.

    Attributes:
        derived_metrics: Registered derived metrics.
    """

    def __init__(self) -> None:
        """Initialize derived metric calculator."""
        self.derived_metrics: Dict[str, DerivedMetric] = {}
        self._cache: Dict[str, float] = {}

    def register_derived(
        self,
        name: str,
        dependencies: List[str],
        formula: str,
        description: str = ""
    ) -> DerivedMetric:
        """Register a derived metric.

        Args:
            name: Name for the derived metric.
            dependencies: List of metric names this depends on.
            formula: Formula string using {metric_name} placeholders.
            description: Description of the metric.

        Returns:
            The registered derived metric.
        """
        derived = DerivedMetric(
            name=name,
            dependencies=dependencies,
            formula=formula,
            description=description
        )
        self.derived_metrics[name] = derived
        return derived

    def calculate(
        self,
        name: str,
        metric_values: Dict[str, float]
    ) -> Optional[float]:
        """Calculate a derived metric value.

        Args:
            name: The derived metric name.
            metric_values: Current values of all metrics.

        Returns:
            Calculated value or None if missing dependencies.
        """
        derived = self.derived_metrics.get(name)
        if not derived:
            return None

        # Check all dependencies are available
        for dep in derived.dependencies:
            if dep not in metric_values:
                return None

        # Replace placeholders and evaluate
        formula = derived.formula
        for dep in derived.dependencies:
            formula = formula.replace(f"{{{dep}}}", str(metric_values[dep]))

        try:
            # Safe eval with only math operations
            result = eval(formula, {"__builtins__": {}}, {
                "abs": abs, "min": min, "max": max,
                "sum": sum, "pow": pow, "sqrt": math.sqrt
            })
            self._cache[name] = result
            return result
        except Exception as e:
            logging.error(f"Failed to calculate {name}: {e}")
            return None

    def get_all_derived(
        self,
        metric_values: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate all derived metrics.

        Args:
            metric_values: Current values of all metrics.

        Returns:
            Dictionary of all calculated derived metrics.
        """
        results: Dict[str, float] = {}
        for name in self.derived_metrics:
            value = self.calculate(name, metric_values)
            if value is not None:
                results[name] = value
        return results
