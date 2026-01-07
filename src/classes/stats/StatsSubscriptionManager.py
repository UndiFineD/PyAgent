#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .StatsSubscription import StatsSubscription

from datetime import datetime
from typing import Any, Callable, Dict, List
import hashlib

class StatsSubscriptionManager:
    """Manages metric subscriptions."""
    def __init__(self) -> None:
        # Legacy exact-metric subscriptions: metric -> callbacks(value)
        self.subscribers: Dict[str, List[Callable[[float], None]]] = {}

        # New-style subscriptions used by tests: (subscriber_id, metric_pattern, delivery_method)
        self._subscriptions: List[StatsSubscription] = []
        self._delivery_handlers: Dict[str, Callable[[str], None]] = {}

    def subscribe(self, *args: Any, **kwargs: Any) -> Any:
        """Subscribe to updates.

        Supported forms:
        - Legacy: subscribe(metric: str, callback: Callable[[float], None]) -> None
        - New: subscribe(subscriber_id: str, metric_pattern: str, delivery_method: str) -> StatsSubscription
        - New (kwargs): subscribe(subscriber_id=..., metric_pattern=..., delivery_method=...)
        """
        if kwargs and "subscriber_id" in kwargs:
            subscriber_id = str(kwargs.get("subscriber_id"))
            metric_pattern = str(kwargs.get("metric_pattern"))
            delivery_method = str(kwargs.get("delivery_method"))
            return self._subscribe_delivery(subscriber_id, metric_pattern, delivery_method)

        if len(args) == 2 and callable(args[1]):
            metric, callback = args
            metric = str(metric)
            if metric not in self.subscribers:
                self.subscribers[metric] = []
            self.subscribers[metric].append(callback)
            return None

        if len(args) == 3:
            subscriber_id, metric_pattern, delivery_method = args
            return self._subscribe_delivery(str(subscriber_id), str(metric_pattern), str(delivery_method))

        raise TypeError("subscribe() expects (metric, callback) or (subscriber_id, metric_pattern, delivery_method)")

    def _subscribe_delivery(self, subscriber_id: str, metric_pattern: str, delivery_method: str) -> "StatsSubscription":
        sub_id = hashlib.md5(f"{subscriber_id}:{metric_pattern}:{delivery_method}".encode()).hexdigest()[:8]
        sub = StatsSubscription(
            id=sub_id,
            subscriber_id=subscriber_id,
            metric_pattern=metric_pattern,
            delivery_method=delivery_method,
            created_at=datetime.now().isoformat(),
        )
        self._subscriptions.append(sub)
        return sub

    def set_delivery_handler(self, delivery_method: str, handler: Callable[[str], None]) -> None:
        """Set a handler for a delivery method (e.g. webhook/email)."""
        self._delivery_handlers[delivery_method] = handler

    def notify(self, metric: str, value: Any) -> None:
        """Notify subscribers.

        - If `value` is a float/int, deliver to legacy metric callbacks.
        - If `value` is a str, treat it as a message and deliver via delivery handlers.
        """
        if isinstance(value, (int, float)):
            if metric in self.subscribers:
                for callback in self.subscribers[metric]:
                    try:
                        callback(float(value))
                    except Exception:
                        pass
            return

        # Message delivery mode
        message = str(value)
        import fnmatch

        for sub in self._subscriptions:
            if fnmatch.fnmatch(metric, sub.metric_pattern):
                handler = self._delivery_handlers.get(sub.delivery_method)
                if handler is None:
                    continue
                try:
                    handler(message)
                except Exception:
                    pass
