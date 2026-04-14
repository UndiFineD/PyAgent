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

"""Agent-facing mixin that delegates n8n bridge calls to core orchestration."""

from __future__ import annotations

from typing import Any


class N8nBridgeMixin:
    """Expose convenient async helpers for n8n bridge operations."""

    _n8n_bridge_core: Any

    async def n8n_trigger(
        self,
        workflow_id: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        """Delegate outbound trigger requests to the configured bridge core.

        Args:
            workflow_id: Target workflow ID.
            event_type: Event type name.
            payload: Event payload body.
            correlation_id: Optional request correlation ID.

        Returns:
            Canonical bridge result from core orchestration.

        """
        return await self._n8n_bridge_core.trigger_workflow(
            workflow_id=workflow_id,
            event_type=event_type,
            payload=payload,
            correlation_id=correlation_id,
        )

    async def n8n_handle_callback(self, raw_payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
        """Delegate inbound callback handling to the configured bridge core.

        Args:
            raw_payload: Raw callback payload.
            headers: Request headers.

        Returns:
            Canonical bridge result from core orchestration.

        """
        return await self._n8n_bridge_core.handle_inbound_event(raw_payload, headers)
