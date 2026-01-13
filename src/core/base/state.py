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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
State management for swarm agents.
Handles persistence of agent memory, history, and metadata.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

__version__ = VERSION

class AgentStateManager:
    """Manages saving and loading agent state to/from disk."""
    
    @staticmethod
    def save_state(file_path: Path, current_state: str, token_usage: int, state_data: Dict[str, Any], history_len: int, path: Optional[Path] = None) -> None:
        """Save agent state to disk."""
        state_path: Path = path or file_path.with_suffix(".state.json")
        state: Dict[str, Any] = {
            "file_path": str(file_path),
            "state": current_state,
            "token_usage": token_usage,
            "state_data": state_data,
            "history_length": history_len,
        }
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        logging.debug(f"State saved to {state_path}")

    @staticmethod
    def load_state(file_path: Path, path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
        """Load agent state from disk."""
        state_path: Path = path or file_path.with_suffix(".state.json")
        if not state_path.exists():
            return None

        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except Exception as e:
            logging.warning(f"Failed to load state: {e}")
            return None