#!/usr/bin/env python3
"""
Module: knowledge_mixin
Provides knowledge and context management mixin for PyAgent agents.
"""
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

"""Knowledge Mixin for BaseAgent."""

from pathlib import Path
<<<<<<< HEAD
<<<<<<< HEAD
from typing import Any, Dict

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from src.core.base.common.memory_core import MemoryCore
from src.core.base.logic.sharded_knowledge_core import ShardedKnowledgeCore


# pylint: disable=too-many-instance-attributes
class KnowledgeMixin:
    """Handles knowledge engines, memory, sharded storage, and templates."""

<<<<<<< HEAD
    def __init__(self, agent_name: str, workspace_root: Path, **_kwargs: Any) -> None:
        self.agent_name: str = agent_name
        self.memory_core = MemoryCore()

=======
    def __init__(self, agent_name: str, workspace_root: Path, **kwargs: Any) -> None:
        self.agent_name = agent_name
        self.memory_core = MemoryCore()
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Legacy Knowledge Trinity support
        try:
            # pylint: disable=import-outside-toplevel
            from src.core.knowledge.knowledge_engine import KnowledgeEngine

            self.knowledge = KnowledgeEngine(agent_id=agent_name, base_path=workspace_root / "data/agents")
        except (ImportError, ModuleNotFoundError):
            self.knowledge = None

<<<<<<< HEAD
<<<<<<< HEAD
        self.sharded_knowledge: ShardedKnowledgeCore = ShardedKnowledgeCore(base_path=workspace_root / "data/agents")
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.sharded_knowledge = ShardedKnowledgeCore(base_path=Path("data/agents"))
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self._local_global_context: Any = None
        self._workspace_root: Path = workspace_root
        self._notes: list[str] = []
        self._prompt_templates: dict[str, Any] = {}

<<<<<<< HEAD
<<<<<<< HEAD
    def store_episode(
        self, task: str, content: str, success: bool, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Creates and stores an episodic memory via MemoryCore."""
        episode: Dict[str, Any] = self.memory_core.create_episode(
            agent_id=self.agent_name, task=task, content=content, success=success, metadata=metadata
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def store_episode(self, task: str, content: str, success: bool, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        """Creates and stores an episodic memory via MemoryCore."""
        episode = self.memory_core.create_episode(
            agent_id=self.agent_name,
            task=task,
            content=content,
            success=success,
            metadata=metadata
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        )
        self.memory_core.store_knowledge(
            agent_id=self.agent_name,
            key=f"ep_{episode['timestamp'].replace(':', '-')}",
            content=episode,
<<<<<<< HEAD
<<<<<<< HEAD
            mode="structured",
=======
            mode="structured"
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            mode="structured"
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        )
        return episode

    def take_note(self, content: str) -> None:
        """Stores a temporary note in memory."""
        self._notes.append(content)

    def get_notes(self) -> list[str]:
        """Get the notes from memory."""
        return self._notes

    def clear_notes(self) -> None:
        """Clear the notes from memory."""
        self._notes = []

    def register_template(self, name: str, template: Any) -> None:
        """Register a prompt template."""
        self._prompt_templates[name] = template

    def get_template(self, name: str) -> Any:
        """Get a prompt template by name."""
        return self._prompt_templates.get(name)

    def add_to_history(self, role: str, content: str) -> None:
        """Add a message to history if manager exists."""
        if hasattr(self, "_history_manager"):
            getattr(self, "_history_manager").add_message(role, content)

    def clear_history(self) -> None:
        """Clear message history."""
        if hasattr(self, "_history_manager"):
            getattr(self, "_history_manager").clear()

    def get_history(self) -> list[Any]:
        """Get message history."""
        if hasattr(self, "_history_manager"):
            return getattr(self, "_history_manager").get_messages()
        return []

    def _build_prompt_with_history(self, prompt: str) -> str:
        """Build a prompt string including history."""
        history: list[Any] = self.get_history()
        history_text: str = "\n".join([f"{getattr(m, 'role', 'user')}: {getattr(m, 'content', m)}" for m in history])
        return f"{history_text}\nUSER: {prompt}"

    @property
    def global_context(self) -> Any:
        """Access global context engine."""
        if hasattr(self, "fleet") and getattr(self, "fleet") and hasattr(getattr(self, "fleet"), "global_context"):
            return getattr(getattr(self, "fleet"), "global_context")
        if self._local_global_context is None:
            try:
                # pylint: disable=import-outside-toplevel
                from src.logic.agents.cognitive.context.engines.global_context_engine import \
                    GlobalContextEngine

                self._local_global_context = GlobalContextEngine(self._workspace_root)
            except (ImportError, ValueError):
                pass
        return self._local_global_context

    @global_context.setter
    def global_context(self, value: Any) -> None:
        """Set local global context."""
        self._local_global_context = value
