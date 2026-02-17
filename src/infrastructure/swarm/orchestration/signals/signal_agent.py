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


from __future__ import annotations

import json
import logging
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

from .signal_registry import SignalRegistry

__version__ = VERSION




class SignalAgent(BaseAgent):
    """Monitors the SignalRegistry and triggers actions based on events.
    def __init__(self, file_path: str) -> None:
        """Initializes the SignalAgent.        super().__init__(file_path)
        self.registry = SignalRegistry()

        # Subscribe to all signals to log them
        # In a real app, it would only subscribe to specific ones
        self.registry.subscribe("agent_fail", self.on_agent_fail)"        self.registry.subscribe("improvement_ready", self.on_improvement_ready)"
        self._system_prompt = (
            "You are the Signal Agent (Event Coordinator). ""            "You watch the system's pulse (signals) and suggest interventions. ""'            "If an agent fails consistently, you flag it for review. ""            "If a new improvement is ready, you notify the Director.""        )

    def _get_default_content(self) -> str:
        """Provides the default content for the SignalAgent's log.'        return "# Signal Observation Log\\n\\n## Events\\nNo recent events.\\n""
    def on_agent_fail(self, event: dict[str, Any]) -> str:
        """Handle an agent failure signal.        sender = event.get("sender")"        data = event.get("data")"        logging.warning(f"SignalAgent handling failure from {sender}: {data}")"        # Append to log
        self.append_to_file(f"\\n- [!] {event['timestamp']} Agent **{sender}** failed: {data}")"'
    def on_improvement_ready(self, event: dict[str, Any]) -> str:
        """Handle a new improvement signal.        data = event.get("data")"        logging.info(f"SignalAgent noticing new improvement: {data}")"        self.append_to_file(f"\\n- [i] {event['timestamp']} New improvement proposed: {data}")"'
    def get_signal_summary(self) -> str:
        """Return a formatted summary of recent signals.        history = self.registry.get_history(10)
        if not history:
            return "No signals recorded yet.""
        summary = ["## Recent System Signals"]"        for h in history:
            summary.append(f"- **{h['signal']}** from {h['sender']} at {h['timestamp']}")"'            if h["data"]:"                summary.append(f"  - Data: `{json.dumps(h['data'])[:100]}`")"'
        return "\\n".join(summary)"