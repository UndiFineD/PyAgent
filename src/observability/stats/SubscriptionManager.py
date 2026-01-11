#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .MetricSubscription import MetricSubscription

from datetime import datetime
from typing import Any, Dict, List, Optional
import hashlib
import logging


































from src.core.base.version import VERSION
__version__ = VERSION

class SubscriptionManager:
    """Manage metric subscriptions and change notifications.

    Provides subscription management for receiving notifications
    when metrics change or breach thresholds.

    Attributes:
        subscriptions: Active subscriptions.
        last_notification: Timestamp of last notification per subscription.
    """

    def __init__(self) -> None:
        """Initialize subscription manager."""
        self.subscriptions: Dict[str, MetricSubscription] = {}
        self.last_notification: Dict[str, datetime] = {}
        self._notification_count: Dict[str, int] = {}

    def subscribe(
        self,
        metric_pattern: str,
        callback_url: str = "",
        notify_on: Optional[List[str]] = None,
        min_interval_seconds: int = 60
    ) -> MetricSubscription:
        """Create a new subscription.

        Args:
            metric_pattern: Glob pattern for metrics.
            callback_url: URL to call on notification.
            notify_on: Events to notify on.
            min_interval_seconds: Minimum interval between notifications.

        Returns:
            The created subscription.
        """
        sub_id = hashlib.md5(
            f"{metric_pattern}:{callback_url}".encode()
        ).hexdigest()[:8]

        subscription = MetricSubscription(
            id=sub_id,
            metric_pattern=metric_pattern,
            callback_url=callback_url,
            notify_on=notify_on or ["threshold", "anomaly"],
            min_interval_seconds=min_interval_seconds
        )
        self.subscriptions[sub_id] = subscription
        self._notification_count[sub_id] = 0
        return subscription

    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove a subscription.

        Args:
            subscription_id: The subscription to remove.

        Returns:
            True if subscription was removed.
        """
        if subscription_id in self.subscriptions:
            del self.subscriptions[subscription_id]
            return True
        return False

    def _matches_pattern(self, metric_name: str, pattern: str) -> bool:
        """Check if metric name matches pattern.

        Args:
            metric_name: The metric name.
            pattern: The glob pattern.

        Returns:
            True if matches.
        """
        import fnmatch
        return fnmatch.fnmatch(metric_name, pattern)

    def notify(
        self,
        metric_name: str,
        event_type: str,
        value: float
    ) -> List[str]:
        """Send notifications for a metric event.

        Args:
            metric_name: The metric name.
            event_type: Type of event (threshold, anomaly).
            value: The metric value.

        Returns:
            List of subscription IDs that were notified.
        """
        notified: List[str] = []
        now = datetime.now()
        for sub_id, sub in self.subscriptions.items():
            if event_type not in sub.notify_on:
                continue
            if not self._matches_pattern(metric_name, sub.metric_pattern):
                continue
            # Check minimum interval
            last = self.last_notification.get(sub_id)
            if last:
                elapsed = (now - last).total_seconds()
                if elapsed < sub.min_interval_seconds:
                    continue
            # Send notification (simulated)
            self.last_notification[sub_id] = now
            self._notification_count[sub_id] += 1
            notified.append(sub_id)
            logging.info(f"Notified {sub_id}: {metric_name}={value} ({event_type})")
        return notified

    def get_stats(self) -> Dict[str, Any]:
        """Get subscription statistics.

        Returns:
            Statistics about subscriptions.
        """
        return {
            "total_subscriptions": len(self.subscriptions),
            "notification_counts": dict(self._notification_count)
        }
