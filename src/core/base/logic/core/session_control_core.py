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

import enum
import json
from pathlib import Path


class SessionSignal(enum.Enum):
    """Signals for agent session lifecycle control."""
    RUNNING = "running"
    PAUSE = "pause"
    STOP = "stop"
    RESUME = "resume"


class SessionControlCore:
    """
    Manages session interrupt signals and shared state flags for long-running agent tasks.
    Enables orchestration layers to pause or stop agents mid-loop via filesystem or shared memory flags.
    Lesson harvested from .external/agentcloud pattern.
    """

    def __init__(self, storage_dir: str = "data/agent_cache/sessions") -> None:
        self.storage_path = Path(storage_dir)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_signal_file(self, session_id: str) -> Path:
        return self.storage_path / f"{session_id}_signal.json"

    def set_signal(self, session_id: str, signal: SessionSignal) -> None:
        """Sets a control signal for a specific session."""
        file_path = self._get_signal_file(session_id)
        data = {"signal": signal.value, "session_id": session_id}

        # In a real system, this would be an atomic write or a Redis call.
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def get_signal(self, session_id: str) -> SessionSignal:
        """Retrieves the current signal for a session."""
        file_path = self._get_signal_file(session_id)
        if not file_path.exists():
            return SessionSignal.RUNNING

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return SessionSignal(data.get("signal", "running"))
        except (json.JSONDecodeError, ValueError):
            return SessionSignal.RUNNING

    def check_interrupt(self, session_id: str) -> bool:
        """Returns True if the session should stop immediately."""
        return self.get_signal(session_id) == SessionSignal.STOP

    def check_pause(self, session_id: str) -> bool:
        """Returns True if the session should pause."""
        return self.get_signal(session_id) == SessionSignal.PAUSE
