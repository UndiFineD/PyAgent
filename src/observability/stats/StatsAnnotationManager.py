#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .MetricAnnotation import MetricAnnotation

from datetime import datetime
from typing import Any, Dict, List, Optional


































from src.core.base.version import VERSION
__version__ = VERSION

class StatsAnnotationManager:
    """Manages annotations on metrics."""

    def __init__(self) -> None:
        self.annotations: Dict[str, List[MetricAnnotation]] = {}

    def add_annotation(
        self,
        metric: str,
        annotation: Optional[MetricAnnotation] = None,
        **kwargs: Any,
    ) -> MetricAnnotation:
        """Add annotation to metric.

        Compatibility:
        - Some tests call `add_annotation(metric=..., timestamp=..., text=..., author=...)`.
        - Older code may pass a `MetricAnnotation` directly.
        """
        if annotation is None:
            timestamp = kwargs.get("timestamp")
            text = str(kwargs.get("text", ""))
            author = str(kwargs.get("author", ""))
            annotation_type = str(kwargs.get("annotation_type", kwargs.get("type", "info")))
            annotation = MetricAnnotation(
                metric_name=metric,
                timestamp=str(timestamp) if timestamp is not None else datetime.now().isoformat(),
                text=text,
                author=author,
                annotation_type=annotation_type,
            )

        if metric not in self.annotations:
            self.annotations[metric] = []
        self.annotations[metric].append(annotation)
        return annotation

    def get_annotations(self, metric: str) -> List[MetricAnnotation]:
        """Get annotations for metric."""
        return self.annotations.get(metric, [])
