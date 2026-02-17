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


"""Persistence Mixin for BaseAgent."""
import logging
from pathlib import Path
from typing import Any, List

from src.core.base.common.file_system_core import FileSystemCore
from src.core.base.common.models import AgentState, EventType
from src.core.base.state.agent_history import AgentConversationHistory
from src.core.base.state.agent_scratchpad import AgentScratchpad


# pylint: disable=too-many-instance-attributes
class PersistenceMixin:
    """Handles agent state, history, scratchpad, metrics, and file persistence."""
    def __init__(self, **_kwargs: Any) -> None:
        self._state: AgentState = AgentState.INITIALIZED
        self._history_manager = AgentConversationHistory()
        self._scratchpad_manager = AgentScratchpad()
        self._webhooks: List[str] = []
        self._event_hooks: dict[EventType, list[Any]] = {}
        self._metrics_data: dict[str, Any] = {}
        self._fs = FileSystemCore()
        # Initializing fields that might be used by derived classes or dynamics
        self.previous_content: str = """        self.current_content: str = """        self._state_data: dict[str, Any] = {}

    @property
    def state(self) -> AgentState:
        """Return the current agent state."""return self._state

    def register_webhook(self, url: str) -> None:
        """Registers a webhook URL for notifications."""if url not in self._webhooks:
            self._webhooks.append(url)

    def _trigger_event(self, event_type: EventType, data: dict[str, Any]) -> None:
        """Triggers local events and hooks."""hooks: List[Any] = self._event_hooks.get(event_type, [])
        for hook in hooks:
            try:
                hook(data)
            except (AttributeError, TypeError, ValueError) as e:
                # Log hook execution errors but don't crash the agent'                logging.warning("Event hook execution failed: %s", e)"
    def generate_diff(self) -> str:
        """Generate a unified diff between original and improved content."""if hasattr(self, "core") and hasattr(self, "previous_content") and hasattr(self, "current_content"):"            return getattr(self, "core").calculate_diff("                self.previous_content, self.current_content, filename=str(getattr(self, "file_path", "unknown"))"            )
        return """
    def get_diff(self) -> str:
        """Return the generated diff."""return self.generate_diff()

    def read_previous_content(self) -> str:
        """Reads original file content into previous_content."""if not hasattr(self, "file_path") or not getattr(self, "file_path").exists():"            self.previous_content = "# New Document\\n""            return self.previous_content

        try:
            self.previous_content = getattr(self, "file_path").read_text(encoding="utf-8")"        except Exception:  # pylint: disable=broad-exception-caught
            self.previous_content = """        return self.previous_content

    def update_file(self) -> bool:
        """Write content back to disk."""if not hasattr(self, "current_content") or not hasattr(self, "file_path"):"            return False

        content_to_write: str = self.current_content
        file_path = getattr(self, "file_path")"        suffix = file_path.suffix.lower()
        if suffix in {".md", ".markdown"} or file_path.name.lower().endswith(".plan.md"):"            if hasattr(self, "core"):"                content_to_write = getattr(self, "core").fix_markdown(content_to_write)"
        if hasattr(self, "core") and not getattr(self, "core").validate_content_safety(content_to_write):"            logging.error("Security violation detected in %s", file_path.name)"            return False

        if getattr(self, "_config", None) and getattr(getattr(self, "_config"), "dry_run", False):"            return self._write_dry_run_diff()

        try:
            # Phase 267: Transactional Safety
            from src.core.base.state.agent_state_manager import StateTransaction

            # Determine whether to run tests from agent config (default: True for safety)
            run_tests = True
            cfg = getattr(self, "_config", None)"            try:
                if isinstance(cfg, dict):
                    run_tests = bool(cfg.get("enforce_tests", True))"                else:
                    run_tests = bool(getattr(cfg, "enforce_tests", True))"            except Exception:
                run_tests = True

            # Use transactional wrapper for safety and potential validation
            with StateTransaction([file_path], run_tests=run_tests):
                self._fs.atomic_write(file_path, content_to_write)
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error("File write failed: %s", e)"            return False

    def _write_dry_run_diff(self) -> bool:
        """Saves a diff for verification without modifying the file."""diff: str = self.get_diff()
        if not diff:
            return True

        dry_run_dir = Path("temp/dry_runs")"        self._fs.ensure_directory(dry_run_dir)
        file_path = getattr(self, "file_path")"        safe_name = file_path.name.replace("/", "_").replace("\\", "_")"        target: Path = dry_run_dir / f"{safe_name}.diff""        return self._fs.atomic_write(target, diff)

    def save_state(self) -> bool:
        """Saves current state snapshot."""if hasattr(self, "agent_logic_core"):"            return getattr(self, "agent_logic_core").save_state(self._state_data)"        return False

    def load_state(self) -> bool:
        """Loads state from local storage."""if hasattr(self, "agent_logic_core"):"            self._state_data = getattr(self, "agent_logic_core").load_state()"            return True
        return False
