#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .MetricCorrelation import MetricCorrelation

from typing import Dict, List, Optional
import math


































from src.core.base.version import VERSION
__version__ = VERSION

class CorrelationAnalyzer:
    """Analyze correlations between metrics.

    Provides correlation analysis to identify relationships
    between different metrics.

    Attributes:
        correlations: Computed correlations.
    """

    def __init__(self) -> None:
        """Initialize correlation analyzer."""
        self.correlations: List[MetricCorrelation] = []
        self._metric_history: Dict[str, List[float]] = {}

    def record_value(self, metric_name: str, value: float) -> None:
        """Record a metric value for correlation analysis.

        Args:
            metric_name: The metric name.
            value: The value to record.
        """
        if metric_name not in self._metric_history:
            self._metric_history[metric_name] = []
        self._metric_history[metric_name].append(value)

    def compute_correlation(
        self,
        metric_a: str,
        metric_b: str
    ) -> Optional[MetricCorrelation]:
        """Compute correlation between two metrics.

        Args:
            metric_a: First metric name.
            metric_b: Second metric name.

        Returns:
            Correlation result or None if insufficient data.
        """
        values_a = self._metric_history.get(metric_a, [])
        values_b = self._metric_history.get(metric_b, [])

        # Need same number of samples
        n = min(len(values_a), len(values_b))
        if n < 3:
            return None

        values_a = values_a[-n:]
        values_b = values_b[-n:]

        # Calculate Pearson correlation
        mean_a = sum(values_a) / n
        mean_b = sum(values_b) / n

        numerator = sum((values_a[i] - mean_a) * (values_b[i] - mean_b) for i in range(n))
        denom_a = math.sqrt(sum((x - mean_a) ** 2 for x in values_a))
        denom_b = math.sqrt(sum((x - mean_b) ** 2 for x in values_b))

        if denom_a == 0 or denom_b == 0:
            return None

        correlation = numerator / (denom_a * denom_b)

        result = MetricCorrelation(
            metric_a=metric_a,
            metric_b=metric_b,
            correlation_coefficient=correlation,
            sample_size=n
        )
        self.correlations.append(result)
        return result

    def find_strong_correlations(
        self,
        threshold: float = 0.7
    ) -> List[MetricCorrelation]:
        """Find strongly correlated metric pairs.

        Args:
            threshold: Minimum absolute correlation coefficient.

        Returns:
            List of strong correlations.
        """
        return [c for c in self.correlations
                if abs(c.correlation_coefficient) >= threshold]

    def get_correlation_matrix(self) -> Dict[str, Dict[str, float]]:
        """Get correlation matrix for all metrics.

        Returns:
            Matrix of correlations.
        """
        metrics = list(self._metric_history.keys())
        matrix: Dict[str, Dict[str, float]] = {}

        for m1 in metrics:
            matrix[m1] = {}
            for m2 in metrics:
                if m1 == m2:
                    matrix[m1][m2] = 1.0
                else:
                    corr = self.compute_correlation(m1, m2)
                    matrix[m1][m2] = corr.correlation_coefficient if corr else 0.0

        return matrix
