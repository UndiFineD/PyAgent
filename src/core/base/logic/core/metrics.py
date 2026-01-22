"""
Core logic for metrics.
(Facade for src.core.base.common.metrics_core)
"""

from src.core.base.common.metrics_core import MetricsCore as StandardMetricsCore

class MetricsCore(StandardMetricsCore):
    """Facade for MetricsCore."""
    pass
