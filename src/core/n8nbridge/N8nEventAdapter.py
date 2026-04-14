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

"""Contract adapter between n8n payloads and bridge canonical events."""

from __future__ import annotations

from typing import Any

from .exceptions import N8nBridgeValidationError


class N8nEventAdapter:
    """Map and validate inbound/outbound n8n bridge events."""

    def to_inbound_event(self, raw_payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
        """Validate and normalize inbound callback payload into canonical shape.

        Args:
            raw_payload: Raw callback payload from n8n.
            headers: Request headers for correlation extraction.

        Returns:
            Canonical inbound event mapping.

        Raises:
            N8nBridgeValidationError: If required fields are missing.

        """
        required = [
            "event_id",
            "event_type",
            "workflow_id",
            "execution_id",
            "occurred_at",
            "source",
            "payload",
            "auth_context",
        ]
        missing = [field for field in required if field not in raw_payload or raw_payload[field] in (None, "")]
        if missing:
            raise N8nBridgeValidationError(f"Missing inbound fields: {', '.join(missing)}")

        correlation_id = _get_header(headers, "X-Correlation-ID") or str(raw_payload.get("event_id", ""))
        if not correlation_id:
            raise N8nBridgeValidationError("Unable to determine correlation_id")

        return {
            "schema_version": "1.0",
            "event_id": str(raw_payload["event_id"]),
            "event_type": str(raw_payload["event_type"]),
            "workflow_id": str(raw_payload["workflow_id"]),
            "execution_id": str(raw_payload["execution_id"]),
            "occurred_at": str(raw_payload["occurred_at"]),
            "source": str(raw_payload["source"]),
            "correlation_id": correlation_id,
            "payload": dict(raw_payload["payload"]),
            "auth_context": dict(raw_payload["auth_context"]),
        }

    def to_n8n_trigger_payload(self, outbound_event: dict[str, Any]) -> dict[str, Any]:
        """Validate and map canonical outbound event into n8n trigger payload.

        Args:
            outbound_event: Canonical outbound event produced by the bridge core.

        Returns:
            n8n-ready trigger payload.

        Raises:
            N8nBridgeValidationError: If required fields are missing.

        """
        required = [
            "schema_version",
            "event_id",
            "event_type",
            "target_workflow",
            "triggered_at",
            "correlation_id",
            "payload",
            "metadata",
        ]
        missing = [field for field in required if field not in outbound_event or outbound_event[field] in (None, "")]
        if missing:
            raise N8nBridgeValidationError(f"Missing outbound fields: {', '.join(missing)}")

        return {
            "schema_version": str(outbound_event["schema_version"]),
            "event_id": str(outbound_event["event_id"]),
            "event_type": str(outbound_event["event_type"]),
            "workflow_id": str(outbound_event["target_workflow"]),
            "triggered_at": str(outbound_event["triggered_at"]),
            "correlation_id": str(outbound_event["correlation_id"]),
            "payload": dict(outbound_event["payload"]),
            "metadata": dict(outbound_event["metadata"]),
        }


def _get_header(headers: dict[str, str], name: str) -> str | None:
    """Read headers in a case-insensitive way.

    Args:
        headers: Incoming header mapping.
        name: Header key to read.

    Returns:
        Header value when available, else ``None``.

    """
    wanted = name.lower()
    for key, value in headers.items():
        if key.lower() == wanted and value:
            return value
    return None
