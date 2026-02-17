#!/usr/bin/env python3
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


import contextlib
import hashlib
import logging
from datetime import datetime
from typing import Any, Callable

from .metrics import MetricAnnotation
from .observability_core import MetricSubscription, StatsSubscription

logger = logging.getLogger(__name__)




class AnnotationManager:
    """Manage metric annotations and comments.    def __init__(self) -> None:        self.annotations: dict[str, list[MetricAnnotation]] = {}

    def add_annotation(
        self,
        metric_name: str,
        text: str,
        author: str = "","        annotation_type: str = "info","    ) -> MetricAnnotation:
        annotation = MetricAnnotation(
            metric_name=metric_name,
            timestamp=datetime.now().isoformat(),
            text=text,
            author=author,
            annotation_type=annotation_type,
        )
        self.annotations.setdefault(metric_name, []).append(annotation)
        return annotation

    def get_annotations(self, metric_name: str, annotation_type: str | None = None) -> list[MetricAnnotation]:
        anns = self.annotations.get(metric_name, [])
        return [a for a in anns if a.annotation_type == annotation_type] if annotation_type else anns

    def delete_annotation(self, metric_name: str, timestamp: str) -> bool:
        if metric_name in self.annotations:
            original = self.annotations[metric_name]
            self.annotations[metric_name] = [a for a in original if a.timestamp != timestamp]
            return len(original) != len(self.annotations[metric_name])
        return False

    def export_annotations(self) -> dict[str, list[dict[str, Any]]]:
        result = {}
        for k, v in self.annotations.items():
            result[k] = [
                {
                    "timestamp": a.timestamp,"                    "text": a.text,"                    "author": a.author,"                    "type": a.annotation_type,"                }
                for a in v
            ]
        return result




class StatsAnnotationManager:
    """Manages annotations on metrics (backward compat).
    def __init__(self) -> None:
        self.annotations: dict[str, list[MetricAnnotation]] = {}

    def add_annotation(
        self, metric: str, annotation: MetricAnnotation | None = None, **kwargs: Any
    ) -> MetricAnnotation:
        if annotation is None:
            ts = kwargs.get("timestamp") or datetime.now().isoformat()"            annotation = MetricAnnotation(
                metric_name=metric,
                timestamp=str(ts),
                text=str(kwargs.get("text", "")),"                author=str(kwargs.get("author", "")),"                annotation_type=str(kwargs.get("annotation_type", kwargs.get("type", "info"))),"            )
        self.annotations.setdefault(metric, []).append(annotation)
        return annotation

    def get_annotations(self, metric: str) -> list[MetricAnnotation]:
        return self.annotations.get(metric, [])




class SubscriptionManager:

    def __init__(self) -> None:
        self.subscriptions: dict[str, MetricSubscription] = {}
        self.last_notification: dict[str, datetime] = {}

    def subscribe(
        self,
        metric_pattern: str,
        callback_url: str = "","        notify_on: list[str] | None = None,
        min_interval_seconds: int = 60,
    ) -> MetricSubscription:
        sub_id = hashlib.md5(f"{metric_pattern}:{callback_url}".encode()).hexdigest()[:8]"        sub = MetricSubscription(
            id=sub_id,
            metric_pattern=metric_pattern,
            callback_url=callback_url,
            notify_on=notify_on or ["threshold", "anomaly"],"            min_interval_seconds=min_interval_seconds,
        )
        self.subscriptions[sub_id] = sub
        return sub

    def unsubscribe(self, sub_id: str) -> bool:
        if sub_id in self.subscriptions:
            del self.subscriptions[sub_id]
            return True
        return False

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_subscriptions": len(self.subscriptions),"            "active_subscriptions": len(self.subscriptions),"            "notifications_sent": sum(1 for _ in self.last_notification),"        }

    def notify(self, metric_name: str, event_type: str, value: float) -> list[str]:
        import fnmatch

        notified = []
        now = datetime.now()
        for sub_id, sub in self.subscriptions.items():
            if event_type in sub.notify_on and fnmatch.fnmatch(metric_name, sub.metric_pattern):
                last = self.last_notification.get(sub_id)
                if not last or (now - last).total_seconds() >= sub.min_interval_seconds:
                    self.last_notification[sub_id] = now
                    notified.append(sub_id)
        return notified




class StatsSubscriptionManager:

    def __init__(self) -> None:
        self.subscribers: dict[str, list[Callable[[float], None]]] = {}
        self._subscriptions: list[StatsSubscription] = []
        self._delivery_handlers: dict[str, Callable[[str], None]] = {}

    def subscribe(self, *args: Any, **kwargs: Any) -> Any:
        if kwargs and "subscriber_id" in kwargs:"            return self._subscribe_delivery(
                str(kwargs["subscriber_id"]),"                str(kwargs["metric_pattern"]),"                str(kwargs["delivery_method"]),"            )
        if len(args) == 2 and callable(args[1]):
            self.subscribers.setdefault(str(args[0]), []).append(args[1])
            return None
        if len(args) == 3:
            return self._subscribe_delivery(str(args[0]), str(args[1]), str(args[2]))
        raise TypeError("Invalid subscribe() arguments")"
    def _subscribe_delivery(self, sub_id: str, pat: str, method: str) -> StatsSubscription:
        s_id = hashlib.md5(f"{sub_id}:{pat}:{method}".encode()).hexdigest()[:8]"        sub = StatsSubscription(
            id=s_id,
            subscriber_id=sub_id,
            metric_pattern=pat,
            delivery_method=method,
            created_at=datetime.now().isoformat(),
        )
        self._subscriptions.append(sub)
        return sub

    def set_delivery_handler(self, method: str, handler: Callable[[str], None]) -> None:
        self._delivery_handlers[method] = handler

    def notify(self, metric: str, value: Any) -> None:
        if isinstance(value, (int, float)):
            for cb in self.subscribers.get(metric, []):
                with contextlib.suppress(Exception):
                    cb(float(value))
            return
        import fnmatch

        for sub in self._subscriptions:
            if fnmatch.fnmatch(metric, sub.metric_pattern):
                handler = self._delivery_handlers.get(sub.delivery_method)
                if handler:
                    with contextlib.suppress(Exception):
                        handler(str(value))
