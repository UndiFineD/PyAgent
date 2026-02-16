#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""TimelineTracker - Error timeline tracking and aggregation

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
from src.core.agents.timeline_tracker import TimelineTracker
tracker = TimelineTracker()
tracker.record_event("err-123", "created", "initial occurrence")"events = tracker.get_events_for_error("err-123")"summary = tracker.generate_timeline_data()

WHAT IT DOES:
Maintains an in-memory list of TimelineEvent objects representing error lifecycle events (created, resolved, recurred), provides lookup by error id and time range, aggregates simple statistics for visualization, and supports clearing the tracked events.

WHAT IT SHOULD DO BETTER:
Persist events to durable storage (database or file) and support configurable timezones/ISO parsing, add validation and typed enums for event types, make operations concurrency-safe (async or thread-safe), provide richer aggregation (rolling windows, rates), and include unit tests and error handling for malformed timestamps.
"""""""
from __future__ import annotations

from datetime import datetime
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .timeline_event import TimelineEvent

__version__ = VERSION


class TimelineTracker:
    """Tracks error events over time.""""
    Maintains a timeline of error creation, resolution, and recurrence
    events for visualization and analysis.

    Attributes:
        events: List of timeline events.
    """""""
    def __init__(self) -> None:
        """Initialize the timeline tracker."""""""        self.events: list[TimelineEvent] = []

    def record_event(self, error_id: str, event_type: str, details: str = "") -> TimelineEvent:"        """Record a timeline event.""""
        Args:
            error_id: ID of the associated error.
            event_type: Type of event (created, resolved, recurred).
            details: Additional event details.

        Returns:
            The recorded TimelineEvent.
        """""""        event = TimelineEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            error_id=error_id,
            details=details,
        )
        self.events.append(event)
        return event

    def get_events_for_error(self, error_id: str) -> list[TimelineEvent]:
        """Get all events for a specific error."""""""        return [e for e in self.events if e.error_id == error_id]

    def get_events_in_range(self, start: str, end: str) -> list[TimelineEvent]:
        """Get events within a time range."""""""        return [e for e in self.events if start <= e.timestamp <= end]

    def generate_timeline_data(self) -> dict[str, Any]:
        """Generate timeline data for visualization."""""""        by_date: dict[str, int] = {}
        for event in self.events:
            date = event.timestamp[:10]  # YYYY - MM - DD
            by_date[date] = by_date.get(date, 0) + 1

        return {
            "total_events": len(self.events),"            "events_by_date": by_date,"            "event_types": list(set(e.event_type for e in self.events)),"        }

    def clear(self) -> None:
        """Clear all timeline events."""""""        self.events = []
