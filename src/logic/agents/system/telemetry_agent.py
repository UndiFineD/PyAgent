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

# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
TelemetryAgent: System agent for collecting, aggregating, and reporting telemetry data across the PyAgent swarm.
Supports observability, monitoring, and health diagnostics.
"""


from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.connectivity_manager import ConnectivityManager
from src.infrastructure.compute.backend.local_context_recorder import \
    LocalContextRecorder
from src.observability.structured_logger import StructuredLogger

__version__ = VERSION


class TelemetryAgent(BaseAgent):
    """
    Tier 5 (Maintenance) - Telemetry Agent: Responsible for broadcasting fleet
    telemetry and archiving interactions for swarm intelligence harvesting.
    """

    def __init__(self, api_url: str = "http://localhost:8000", workspace_root: str | None = None) -> None:
        super().__init__(workspace_root or ".")
        self.api_url = api_url
        self.log_buffer: list[Any] = []

        # Phase 108: Robustness and Intelligence Harvesting
        self.connectivity = ConnectivityManager(workspace_root)
        self.recorder = LocalContextRecorder(Path(workspace_root)) if workspace_root else None
        self.logger = StructuredLogger(agent_id="TelemetryAgent")

    def _archive_telemetry_event(self, event_type: str, data: dict[str, Any]) -> None:
        """Harvest telemetry logic for future self-improvement."""
        if self.recorder:
            try:
                meta = {"phase": 108, "type": "telemetry", "timestamp": time.time()}
                self.recorder.record_interaction("telemetry", "broadcast", event_type, json.dumps(data), meta=meta)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass

    def log_event(self, event_type: str, source: str, data: dict[str, Any]) -> None:
        event = {
            "type": event_type,
            "source": source,
            "data": data,
            "timestamp": time.time(),
        }
        self.logger.info(f"Telemetry event: {event_type}", source=source, type=event_type)

        # Phase 108: TTL-based connectivity check
        if self.connectivity.is_endpoint_available("telemetry_server"):
            try:
                # requests.post(f"{self.api_url}/telemetry/log", json=event, timeout=0.1)
                # self.connectivity.update_status("telemetry_server", True)
                pass
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                # self.connectivity.update_status("telemetry_server", False)
                pass

        self._archive_telemetry_event(event_type, data)
        self.log_buffer.append(event)
        if len(self.log_buffer) > 100:
            self.log_buffer.pop(0)

    def get_recent_logs(self) -> list[dict[str, Any]]:
        return self.log_buffer
