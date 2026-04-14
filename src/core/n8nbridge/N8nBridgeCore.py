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

"""Core orchestration for n8n bridge inbound and outbound flows."""

from __future__ import annotations

import time as _stdlib_time
import uuid
from datetime import datetime, timezone
from typing import Any

from .N8nBridgeConfig import N8nBridgeConfig
from .N8nEventAdapter import N8nEventAdapter
from .N8nHttpClient import N8nHttpClient


class _TimeProxy:
    """Provide patch-friendly monotonic clock access for tests."""

    @staticmethod
    def monotonic() -> float:
        """Return monotonic time from stdlib clock.

        Returns:
            Monotonic timestamp in fractional seconds.

        """
        return _stdlib_time.monotonic()


time = _TimeProxy()


class N8nBridgeCore:
    """Coordinate adapter and transport behavior for bridge workflows."""

    def __init__(self, config: N8nBridgeConfig, adapter: N8nEventAdapter, http_client: N8nHttpClient) -> None:
        """Initialize core dependencies and in-memory idempotency map.

        Args:
            config: Runtime bridge configuration.
            adapter: Event adapter for schema mappings.
            http_client: HTTP transport for outbound requests.

        """
        self._config = config
        self._adapter = adapter
        self._http_client = http_client
        self._seen_event_ids: dict[str, float] = {}

    async def handle_inbound_event(self, raw_payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
        """Normalize and process inbound callback events.

        Args:
            raw_payload: Raw n8n callback payload.
            headers: Incoming callback headers.

        Returns:
            Canonical bridge result dict.

        """
        inbound_event = self._adapter.to_inbound_event(raw_payload, headers)
        event_id = str(inbound_event["event_id"])
        correlation_id = str(inbound_event["correlation_id"])

        if self._is_duplicate_event(event_id):
            return {
                "ok": False,
                "status": "duplicate",
                "http_status": 409,
                "correlation_id": correlation_id,
                "event_id": event_id,
                "attempts": 1,
                "retryable": False,
                "error_code": "duplicate_event",
                "message": "Duplicate inbound event id inside idempotency TTL",
                "data": {},
            }

        return {
            "ok": True,
            "status": "processed",
            "http_status": 200,
            "correlation_id": correlation_id,
            "event_id": event_id,
            "attempts": 1,
            "retryable": False,
            "error_code": None,
            "message": "Inbound event processed",
            "data": inbound_event,
        }

    async def trigger_workflow(
        self,
        *,
        workflow_id: str,
        event_type: str,
        payload: dict[str, Any],
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        """Trigger an outbound n8n workflow execution.

        Args:
            workflow_id: Target workflow identifier.
            event_type: Canonical event type string.
            payload: Event payload to send.
            correlation_id: Optional correlation ID override.

        Returns:
            Canonical bridge result dict.

        """
        corr = correlation_id or str(uuid.uuid4())
        event_id = str(uuid.uuid4())
        outbound_event = {
            "schema_version": "1.0",
            "event_id": event_id,
            "event_type": event_type,
            "target_workflow": workflow_id,
            "triggered_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "correlation_id": corr,
            "payload": payload,
            "metadata": {"source": "pyagent"},
        }
        trigger_payload = self._adapter.to_n8n_trigger_payload(outbound_event)

        try:
            status, body, _headers = await self._http_client.post_json(
                "/hooks/trigger",
                trigger_payload,
                correlation_id=corr,
            )
            return {
                "ok": 200 <= status < 300,
                "status": "accepted" if 200 <= status < 300 else "failed",
                "http_status": status,
                "correlation_id": corr,
                "event_id": event_id,
                "attempts": 1,
                "retryable": False,
                "error_code": None,
                "message": "n8n workflow triggered",
                "data": body,
            }
        except TimeoutError as error:
            return {
                "ok": False,
                "status": "timeout",
                "http_status": 504,
                "correlation_id": corr,
                "event_id": event_id,
                "attempts": 1,
                "retryable": True,
                "error_code": "timeout",
                "message": str(error),
                "data": {},
            }
        except Exception as error:  # pragma: no cover - defensive mapping for contract shape.
            return {
                "ok": False,
                "status": "failed",
                "http_status": 500,
                "correlation_id": corr,
                "event_id": event_id,
                "attempts": 1,
                "retryable": False,
                "error_code": "bridge_error",
                "message": str(error),
                "data": {},
            }

    def _is_duplicate_event(self, event_id: str) -> bool:
        """Check and record event IDs inside the configured idempotency window.

        Args:
            event_id: Inbound event identifier.

        Returns:
            ``True`` when the event is a duplicate inside the TTL window.

        """
        now = time.monotonic()
        self._evict_expired(now)
        expires_at = self._seen_event_ids.get(event_id)
        if expires_at is not None and now <= expires_at:
            return True

        self._seen_event_ids[event_id] = time.monotonic() + float(self._config.idempotency_ttl_seconds)
        return False

    def _evict_expired(self, now: float) -> None:
        """Drop expired idempotency entries.

        Args:
            now: Current monotonic timestamp.

        """
        expired = [event_id for event_id, expires_at in self._seen_event_ids.items() if now > expires_at]
        for event_id in expired:
            del self._seen_event_ids[event_id]
