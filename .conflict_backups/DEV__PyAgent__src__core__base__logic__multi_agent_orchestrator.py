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


"""
Multi-Agent Orchestrator Core - Unified Agent Management System
=================================================================

Inspired by big-3-super-agent's orchestration patterns, this core provides:
- Unified interface for managing multiple agent types (voice, coding, browser)
- Agent registry with persistent session management
- Tool-based dispatch system for agent orchestration
- Background task processing with status tracking
- Working directory management per agent type

Key Patterns Extracted from big-3-super-agent:
- Agent registry system with session persistence
- Tool-based orchestration via function calls
- Background processing with operator logs
- Multi-agent coordination and lifecycle management
"""

import json
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field

from src.core.base.common.models.communication_models import CascadeContext
from src.core.base.state.agent_state_manager import StateTransaction


@dataclass
class AgentMetadata:
    """Metadata for registered agents."""
    name: str
    agent_type: str
    session_id: str
    created_at: str
    working_dir: str
    status: str = "active"
    last_active: Optional[str] = None
    task_history: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)


@dataclass
class TaskResult:
    """Result of an agent task execution."""
    task_id: str
    agent_name: str
    status: str  # "pending", "running", "completed", "failed"
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    operator_log: Optional[str] = None




class MultiAgentOrchestratorCore:
    """
    Unified orchestrator for managing multiple agent types.

    Provides a centralized system for:
    - Agent registration and lifecycle management
    - Task dispatch and execution tracking
    - Working directory management
    - Tool-based orchestration interface
    """

    def __init__(self, base_working_dir: Optional[Path] = None):
        """Initialize the multi-agent orchestrator."""
        self.base_working_dir = base_working_dir or Path.cwd() / "agent_workspace"
        self.base_working_dir.mkdir(parents=True, exist_ok=True)

        # Agent registry storage
        self.registry_path = self.base_working_dir / "agent_registry.json"
        self.agent_registry: Dict[str, AgentMetadata] = {}
        self.registry_lock = threading.Lock()

        # Task tracking
        self.tasks: Dict[str, TaskResult] = {}
        self.task_lock = threading.Lock()

        # Background processing
        self.background_threads: List[threading.Thread] = []
        self.running = True

        # Agent type handlers
        self.agent_handlers: Dict[str, Callable] = {}

        # Load existing registry
        self._load_registry()

    def _load_registry(self):
        """Load agent registry from disk."""
        if not self.registry_path.exists():
            return

        try:
            with self.registry_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                for name, metadata in data.get("agents", {}).items():
                    self.agent_registry[name] = AgentMetadata(**metadata)
        except Exception as e:
            print(f"Warning: Failed to load agent registry: {e}")

    def _save_registry(self):
        """Save agent registry to disk."""
        data = {
            "agents": {
                name: {
                    "name": agent.name,
                    "agent_type": agent.agent_type,
                    "session_id": agent.session_id,
                    "created_at": agent.created_at,
                    "working_dir": agent.working_dir,
                    "status": agent.status,
                    "last_active": agent.last_active,
                    "task_history": agent.task_history,
                    "capabilities": agent.capabilities,
                }
                for name, agent in self.agent_registry.items()
            }
        }

        with StateTransaction([self.registry_path]) as _:
            self.registry_path.write_text(json.dumps(data, indent=2))

    def register_agent_type(self, agent_type: str, handler: Callable):
        """
        Register a handler for a specific agent type.

        Args:
            agent_type: Type of agent (e.g., "voice", "coding", "browser")
            handler: Function that creates and manages agents of this type
        """
        self.agent_handlers[agent_type] = handler

    def create_agent(
        self,
        agent_type: str,
        agent_name: Optional[str] = None,
        capabilities: Optional[List[str]] = None,
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """
        Create and register a new agent.

        Args:
            agent_type: Type of agent to create
            agent_name: Optional name for the agent
            capabilities: List of agent capabilities
            context: Cascade context for lineage tracking

        Returns:
            Dictionary with agent creation result
        """
        if agent_type not in self.agent_handlers:
            return {
                "ok": False,
                "error": f"Unsupported agent type: {agent_type}. Available: {list(self.agent_handlers.keys())}"
            }

        # Generate unique name if not provided
        if not agent_name:
            agent_name = self._generate_agent_name(agent_type)

        # Check for name conflicts
        if agent_name in self.agent_registry:
            return {
                "ok": False,
                "error": f"Agent '{agent_name}' already exists"
            }

        try:
            # Create agent working directory
            agent_dir = self.base_working_dir / agent_type / agent_name
            agent_dir.mkdir(parents=True, exist_ok=True)

            # Generate session ID
            session_id = str(uuid.uuid4())

            # Create agent metadata
            metadata = AgentMetadata(
                name=agent_name,
                agent_type=agent_type,
                session_id=session_id,
                created_at=datetime.now(timezone.utc).isoformat(),
                working_dir=str(agent_dir),
                capabilities=capabilities or [],
            )

            # Register agent
            with self.registry_lock:
                self.agent_registry[agent_name] = metadata
                self._save_registry()

            # Initialize agent with handler
            handler = self.agent_handlers[agent_type]
            init_result = handler("create", agent_name, metadata)

            if not init_result.get("ok", False):
                # Cleanup on failure
                with self.registry_lock:
                    del self.agent_registry[agent_name]
                    self._save_registry()
                return init_result

            return {
                "ok": True,
                "agent_name": agent_name,
                "session_id": session_id,
                "working_dir": str(agent_dir),
                "capabilities": capabilities,
            }

        except Exception as e:
            return {
                "ok": False,
                "error": f"Failed to create agent: {e}"
            }

    def dispatch_task(
        self,
        agent_name: str,
        task_description: str,
        parameters: Optional[Dict[str, Any]] = None,
        context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """
        Dispatch a task to an agent for execution.

        Args:
            agent_name: Name of the agent to dispatch to
            task_description: Description of the task
            parameters: Additional task parameters
            context: Cascade context for lineage tracking

        Returns:
            Dictionary with task dispatch result
        """
        agent = self.agent_registry.get(agent_name)
        if not agent:
            return {
                "ok": False,
                "error": f"Agent '{agent_name}' not found"
            }

        if agent.status != "active":
            return {
                "ok": False,
                "error": f"Agent '{agent_name}' is not active (status: {agent.status})"
            }

        # Create task record
        task_id = str(uuid.uuid4())
        task_result = TaskResult(
            task_id=task_id,
            agent_name=agent_name,
            status="pending",
            started_at=datetime.now(timezone.utc).isoformat(),
        )

        with self.task_lock:
            self.tasks[task_id] = task_result

        # Update agent last active time
        agent.last_active = datetime.now(timezone.utc).isoformat()
        agent.task_history.append(task_id)
        self._save_registry()

        # Dispatch task in background
        thread = threading.Thread(
            target=self._execute_task_background,
            args=(task_id, agent, task_description, parameters or {}),
            daemon=True
        )
        thread.start()
        self.background_threads.append(thread)

        return {
            "ok": True,
            "task_id": task_id,
            "agent_name": agent_name,
            "status": "dispatched"
        }

    def get_task_status(self, task_id: str) -> Optional[TaskResult]:
        """Get the status of a task."""
        with self.task_lock:
            return self.tasks.get(task_id)

    def list_agents(self, agent_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all registered agents, optionally filtered by type."""
        agents = []
        for name, metadata in self.agent_registry.items():
            if agent_type and metadata.agent_type != agent_type:
                continue

            agents.append({
                "name": metadata.name,
                "type": metadata.agent_type,
                "session_id": metadata.session_id,
                "status": metadata.status,
                "created_at": metadata.created_at,
                "last_active": metadata.last_active,
                "capabilities": metadata.capabilities,
                "task_count": len(metadata.task_history),
            })

        return sorted(agents, key=lambda x: x["created_at"], reverse=True)

    def delete_agent(self, agent_name: str) -> Dict[str, Any]:
        """Delete an agent and clean up its resources."""
        agent = self.agent_registry.get(agent_name)
        if not agent:
            return {
                "ok": False,
                "error": f"Agent '{agent_name}' not found"
            }

        try:
            # Notify handler of deletion
            if agent.agent_type in self.agent_handlers:
                handler = self.agent_handlers[agent.agent_type]
                handler("delete", agent_name, agent)

            # Remove from registry
            with self.registry_lock:
                del self.agent_registry[agent_name]
                self._save_registry()

            # Clean up working directory
            agent_dir = Path(agent.working_dir)
            if agent_dir.exists():
                import shutil
                shutil.rmtree(agent_dir)

            return {"ok": True, "agent_name": agent_name}

        except Exception as e:
            return {
                "ok": False,
                "error": f"Failed to delete agent: {e}"
            }

    def get_agent_tools(self, agent_name: str) -> List[Dict[str, Any]]:
        """Get available tools for an agent."""
        agent = self.agent_registry.get(agent_name)
        if not agent or agent.agent_type not in self.agent_handlers:
            return []

        handler = self.agent_handlers[agent.agent_type]
        return handler("tools", agent_name, agent)

    def shutdown(self):
        """Shutdown the orchestrator and cleanup resources."""
        self.running = False

        # Wait for background threads
        for thread in self.background_threads:
            if thread.is_alive():
                thread.join(timeout=5.0)

        # Save final registry state
        self._save_registry()

    def _execute_task_background(
        self,
        task_id: str,
        agent: AgentMetadata,
        task_description: str,
        parameters: Dict[str, Any]
    ):
        """Execute a task in the background."""
        try:
            # Update task status
            with self.task_lock:
                self.tasks[task_id].status = "running"

            # Get agent handler
            if agent.agent_type not in self.agent_handlers:
                raise ValueError(f"No handler for agent type: {agent.agent_type}")

            handler = self.agent_handlers[agent.agent_type]

            # Execute task
            result = handler("execute", agent.name, {
                "task_description": task_description,
                "parameters": parameters,
                "agent_metadata": agent,
            })

            # Update task result
            with self.task_lock:
                task = self.tasks[task_id]
                task.status = "completed" if result.get("ok") else "failed"
                task.result = result
                task.completed_at = datetime.now(timezone.utc).isoformat()
                if not result.get("ok"):
                    task.error = result.get("error", "Unknown error")

        except Exception as e:
            # Update task with error
            with self.task_lock:
                task = self.tasks[task_id]
                task.status = "failed"
                task.error = str(e)
                task.completed_at = datetime.now(timezone.utc).isoformat()

    def _generate_agent_name(self, agent_type: str) -> str:
        """Generate a unique agent name."""
        base_name = f"{agent_type}_{int(time.time())}"
        counter = 1
        name = base_name

        while name in self.agent_registry:
            name = f"{base_name}_{counter}"
            counter += 1

        return name
