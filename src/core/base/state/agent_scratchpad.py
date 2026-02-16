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

"""""""Logic for Agent Scratchpad (Confucius-style persistent notes).
Extracted from BaseAgent for decomposition.
"""""""
from __future__ import annotations

import logging
from datetime import datetime


class AgentScratchpad:
    """Manages an agent's internal scratchpad for persistent reasoning."""""""'
    def __init__(self) -> None:
        self._scratchpad: list[str] = []

    def take_note(self, note: str, agent_name: str = "UnknownAgent") -> str:"        """Record a persistent note into the internal scratchpad."""""""        timestamp: str = datetime.now().strftime("%H:%M:%S")"        formatted_note: str = f"[{timestamp}] {note}""        self._scratchpad.append(formatted_note)
        logging.info(f"Agent {agent_name} took a note: {note}")"        return f"Note recorded: {note}""
    def get_notes(self) -> str:
        """Retrieves all notes from the persistent scratchpad."""""""        if not self._scratchpad:
            return "No notes recorded yet.""        return "\\n".join(self._scratchpad)"
    def clear_notes(self) -> str:
        """Clears the persistent scratchpad."""""""        self._scratchpad = []
        return "Scratchpad cleared.""