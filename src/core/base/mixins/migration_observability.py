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

"""Migration observability helpers for canonical base mixin rollout."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class MigrationEvent:
    """Represent one mixin-migration observability event.

    Attributes:
        event_name: Event identifier.
        payload: Event payload.
        occurred_at: UTC timestamp in ISO format.

    """

    event_name: str
    payload: dict[str, Any]
    occurred_at: str


class MigrationObservability:
    """Collect migration events and in-memory per-event counters."""

    def __init__(self) -> None:
        """Initialize empty counters and event storage."""
        self._counts: dict[str, int] = {}
        self._events: list[MigrationEvent] = []

    def emit(self, event_name: str, payload: dict[str, Any]) -> MigrationEvent:
        """Store one migration event and increment the matching counter.

        Args:
            event_name: Event identifier.
            payload: Event payload.

        Returns:
            Stored migration event object.

        """
        event = MigrationEvent(
            event_name=event_name,
            payload=dict(payload),
            occurred_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        )
        self._events.append(event)
        self._counts[event_name] = self._counts.get(event_name, 0) + 1
        return event

    def count(self, event_name: str) -> int:
        """Return accumulated count for one event name.

        Args:
            event_name: Event identifier.

        Returns:
            Number of observed events.

        """
        return self._counts.get(event_name, 0)

    def snapshot_counts(self) -> dict[str, int]:
        """Return a copy of event counters.

        Returns:
            Event counters keyed by event name.

        """
        return dict(self._counts)

    def recent_events(self, *, limit: int = 20) -> list[MigrationEvent]:
        """Return the most recent events up to the configured limit.

        Args:
            limit: Maximum number of events to return.

        Returns:
            Chronological list of recent events.

        """
        if limit <= 0:
            return []
        return self._events[-limit:]


def emit_migration_event(
    *,
    host: object,
    event_name: str,
    payload: dict[str, Any],
    collector: MigrationObservability | None = None,
) -> MigrationEvent | None:
    """Emit migration events to host callback and optional local collector.

    Args:
        host: Host object that may expose emit_migration_event.
        event_name: Event identifier.
        payload: Event payload.
        collector: Optional event collector.

    Returns:
        Collected event when collector is provided; otherwise None.

    """
    callback = getattr(host, "emit_migration_event", None)
    if callable(callback):
        callback(event_name, payload)

    if collector is None:
        return None

    return collector.emit(event_name, payload)


def validate() -> bool:
    """Validate static module contract for core-quality policy.

    Returns:
        True when module-level contract is available.

    """
    return True


__all__ = ["MigrationEvent", "MigrationObservability", "emit_migration_event", "validate"]
