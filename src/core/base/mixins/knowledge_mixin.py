#!/usr/bin/env python3
# Knowledge Mixin for BaseAgent
from typing import Any
from pathlib import Path
from src.core.base.common.memory_core import MemoryCore
from src.core.base.logic.sharded_knowledge_core import ShardedKnowledgeCore

class KnowledgeMixin:
    """Handles knowledge engines, memory, sharded storage, and templates."""

    def __init__(self, agent_name: str, workspace_root: Path, **kwargs: Any) -> None:
        self.agent_name = agent_name
        self.memory_core = MemoryCore()
        
        # Legacy Knowledge Trinity support
        try:
            from src.core.knowledge.knowledge_engine import KnowledgeEngine
            self.knowledge = KnowledgeEngine(
                agent_id=agent_name, base_path=Path("data/agents")
            )
        except (ImportError, ModuleNotFoundError):
            self.knowledge = None

        self.sharded_knowledge = ShardedKnowledgeCore(base_path=Path("data/agents"))
        self._local_global_context: Any = None
        self._workspace_root = workspace_root
        self._notes: list[str] = []
        self._prompt_templates: dict[str, Any] = {}

    def store_episode(self, task: str, content: str, success: bool, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        """Creates and stores an episodic memory via MemoryCore."""
        episode = self.memory_core.create_episode(
            agent_id=self.agent_name,
            task=task,
            content=content,
            success=success,
            metadata=metadata
        )
        self.memory_core.store_knowledge(
            agent_id=self.agent_name,
            key=f"ep_{episode['timestamp'].replace(':', '-')}",
            content=episode,
            mode="structured"
        )
        return episode

    def take_note(self, content: str) -> None:
        """Stores a temporary note in memory."""
        self._notes.append(content)

    def get_notes(self) -> list[str]:
        return self._notes

    def clear_notes(self) -> None:
        self._notes = []

    def register_template(self, name: str, template: Any) -> None:
        self._prompt_templates[name] = template

    def get_template(self, name: str) -> Any:
        return self._prompt_templates.get(name)

    def add_to_history(self, role: str, content: str) -> None:
        if hasattr(self, "_history_manager"):
            self._history_manager.add_message(role, content)

    def clear_history(self) -> None:
        if hasattr(self, "_history_manager"):
            self._history_manager.clear()

    def get_history(self) -> list[Any]:
        if hasattr(self, "_history_manager"):
            return self._history_manager.get_messages()
        return []

    def _build_prompt_with_history(self, prompt: str) -> str:
        history = self.get_history()
        history_text = "\n".join([f"{getattr(m, 'role', 'user')}: {getattr(m, 'content', m)}" for m in history])
        return f"{history_text}\nUSER: {prompt}"

    @property
    def global_context(self) -> Any:
        if (
            hasattr(self, "fleet")
            and self.fleet
            and hasattr(self.fleet, "global_context")
        ):
            return self.fleet.global_context
        if self._local_global_context is None:
            try:
                from src.logic.agents.cognitive.context.engines.global_context_engine import (
                    GlobalContextEngine,
                )
                self._local_global_context = GlobalContextEngine(self._workspace_root)
            except (ImportError, ValueError):
                pass
        return self._local_global_context

    @global_context.setter
    def global_context(self, value: Any) -> None:
        self._local_global_context = value
