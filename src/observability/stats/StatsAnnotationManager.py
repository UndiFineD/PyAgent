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
from typing import Any, Dict, List, Optional



































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
