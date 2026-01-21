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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from .report_subscription import ReportSubscription
from .report_type import ReportType
from typing import Any
import logging
import time

__version__ = VERSION


class SubscriptionManager:
    """Manager for report subscriptions and scheduled delivery.
    Handles subscriber management, delivery scheduling, and
    notification triggering.
    Attributes:
        subscriptions: Active subscriptions.
        delivery_queue: Pending deliveries.
    Example:
        manager=SubscriptionManager()
        manager.add_subscription(ReportSubscription("user1", "user@example.com"))
        manager.process_deliveries()
    """

    def __init__(self) -> None:
        """Initialize subscription manager."""

        self.subscriptions: dict[str, ReportSubscription] = {}
        self.delivery_queue: list[dict[str, Any]] = []
        logging.debug("SubscriptionManager initialized")

    def add_subscription(self, subscription: ReportSubscription) -> None:
        """Add a subscription.
        Args:
            subscription: Subscription to add.
        """

        self.subscriptions[subscription.subscriber_id] = subscription
        logging.debug(f"Added subscription for {subscription.subscriber_id}")

    def remove_subscription(self, subscriber_id: str) -> bool:
        """Remove a subscription.
        Args:
            subscriber_id: Subscriber to remove.
        Returns:
            True if removed.
        """

        if subscriber_id in self.subscriptions:
            del self.subscriptions[subscriber_id]
            return True
        return False

    def get_due_subscriptions(self) -> list[ReportSubscription]:
        """Get subscriptions due for delivery.
        Returns:
            List of due subscriptions.
        """

        return [s for s in self.subscriptions.values() if s.enabled]

    def queue_delivery(
        self, subscriber_id: str, report_content: str, report_type: ReportType
    ) -> None:
        """Queue a report delivery.
        Args:
            subscriber_id: Target subscriber.
            report_content: Report content.
            report_type: Type of report.
        """

        self.delivery_queue.append(
            {
                "subscriber_id": subscriber_id,
                "content": report_content,
                "type": report_type,
                "queued_at": time.time(),
            }
        )

    def process_deliveries(self) -> int:
        """Process pending deliveries.
        Returns:
            Number of deliveries processed.
        """

        processed = len(self.delivery_queue)
        self.delivery_queue.clear()
        return processed
