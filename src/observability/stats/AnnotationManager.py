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



from .MetricAnnotation import MetricAnnotation

from datetime import datetime
from typing import Dict, List, Optional
import json



































class AnnotationManager:
    """Manage metric annotations and comments.

    Provides capabilities for adding and managing annotations
    on metrics for documentation and context.

    Attributes:
        annotations: All annotations indexed by metric name.
    """

    def __init__(self) -> None:
        """Initialize annotation manager."""
        self.annotations: Dict[str, List[MetricAnnotation]] = {}

    def add_annotation(
        self,
        metric_name: str,
        text: str,
        author: str = "",
        annotation_type: str = "info"
    ) -> MetricAnnotation:
        """Add an annotation to a metric.

        Args:
            metric_name: The metric to annotate.
            text: Annotation text.
            author: Author of the annotation.
            annotation_type: Type of annotation (info, warning, milestone).

        Returns:
            The created annotation.
        """
        annotation = MetricAnnotation(
            metric_name=metric_name,
            timestamp=datetime.now().isoformat(),
            text=text,
            author=author,
            annotation_type=annotation_type
        )

        if metric_name not in self.annotations:
            self.annotations[metric_name] = []
        self.annotations[metric_name].append(annotation)
        return annotation

    def get_annotations(
        self,
        metric_name: str,
        annotation_type: Optional[str] = None
    ) -> List[MetricAnnotation]:
        """Get annotations for a metric.

        Args:
            metric_name: The metric name.
            annotation_type: Optional type filter.

        Returns:
            List of annotations.
        """
        annotations = self.annotations.get(metric_name, [])
        if annotation_type:
            annotations = [a for a in annotations if a.annotation_type == annotation_type]
        return annotations

    def delete_annotation(self, metric_name: str, timestamp: str) -> bool:
        """Delete an annotation by timestamp.

        Args:
            metric_name: The metric name.
            timestamp: The annotation timestamp.

        Returns:
            True if annotation was deleted.
        """
        if metric_name not in self.annotations:
            return False

        original_count = len(self.annotations[metric_name])
        self.annotations[metric_name] = [
            a for a in self.annotations[metric_name]
            if a.timestamp != timestamp
        ]
        return len(self.annotations[metric_name]) < original_count

    def export_annotations(self, metric_name: Optional[str] = None) -> str:
        """Export annotations to JSON.

        Args:
            metric_name: Optional metric to filter by.

        Returns:
            JSON string of annotations.
        """
        if metric_name:
            data: List[MetricAnnotation] = self.annotations.get(metric_name, [])
        else:
            data = []
            for ann_values in self.annotations.values():
                data.extend(ann_values)
        return json.dumps([{
            "metric_name": a.metric_name,
            "timestamp": a.timestamp,
            "text": a.text,
            "author": a.author,
            "type": a.annotation_type
        } for a in data], indent=2)
