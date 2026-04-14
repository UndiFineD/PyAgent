"""FleetManager plugin — orchestrates specialized agent fleet.

This plugin provides tools for managing and coordinating the Hermes agent fleet,
including task distribution, agent spawning, and fleet health monitoring.
"""

from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING, cast

from hermes_constants import get_hermes_home  # type: ignore[reportMissingImports]

logger = logging.getLogger(__name__)

# Try to import the fleetmanager components
try:
    # Add the orchestration and code directories to path for imports
    import sys

    GITHUB_AGENTS_ROOT = Path.home() / ".github" / "agents"
    GITHUB_AGENTS_ORCHESTRATION = str(GITHUB_AGENTS_ROOT / "orchestration")
    GITHUB_AGENTS_CODE = str(GITHUB_AGENTS_ROOT / "code")
    for path in (GITHUB_AGENTS_ORCHESTRATION, GITHUB_AGENTS_CODE):
        if path not in sys.path:
            sys.path.insert(0, path)

    from backend import PostgresBackend  # type: ignore[reportMissingModuleSource]

    # Availability flag - lowercase to avoid constant redeclaration warnings
    fleetmanager_available = True
except ImportError as e:
    logger.warning(f"FleetManager components not available: {e}")
    fleetmanager_available = False
    PostgresBackend = None  # type: ignore

if TYPE_CHECKING:
    # For static type checkers import the real type when available
    from backend import PostgresBackend  # type: ignore


class FleetManagerPlugin:
    """FleetManager plugin for agent fleet orchestration."""

    def __init__(self) -> None:
        self.name = "fleetmanager"
        self._backend: Optional[Any] = None
        self._hermes_home: Optional[str] = None
        self._initialized = False

    def is_available(self) -> bool:
        """Check if FleetManager plugin is available and configured."""
        if not fleetmanager_available:
            return False

        # Check for required environment variables
        required_vars = ["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
        return all(os.getenv(var) for var in required_vars)

    def initialize(self, session_id: str, **kwargs: Any) -> None:
        """Initialize the FleetManager plugin for a session."""
        if not self.is_available():
            logger.warning("FleetManager plugin not available - missing dependencies or config")
            return

        self._hermes_home = kwargs.get("hermes_home", get_hermes_home())
        logger.info(f"Initializing FleetManager plugin for session {session_id}")

        # Initialize the backend
        if PostgresBackend is None:
            logger.error("PostgresBackend class not available despite FLEETMANAGER_AVAILABLE")
            self._backend = None
            self._initialized = False
            return

        try:
            self._backend = PostgresBackend()
            self._initialized = True
            logger.info("FleetManager backend initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize FleetManager backend: {e}")
            self._backend = None
            self._initialized = False

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return tool schemas exposed by this plugin."""
        if not self._initialized or not self._backend:
            return []

        return [
            {
                "name": "fleetmanager_status",
                "description": "Get status of the agent fleet including pending tasks and agent health",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of tasks to return (default: 10)",
                            "default": 10,
                        }
                    },
                    "additionalProperties": False,
                },
            },
            {
                "name": "fleetmanager_run",
                "description": "Execute the fleet manager to process pending tasks",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of tasks to process (default: 10)",
                            "default": 10,
                        }
                    },
                    "additionalProperties": False,
                },
            },
            {
                "name": "fleetmanager_agents",
                "description": "List all available agents in the fleet",
                "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
            },
        ]

    def handle_tool_call(self, tool_name: str, args: Dict[str, Any], **kwargs: Any) -> str:
        """Handle tool calls for FleetManager plugin tools."""
        if not self._initialized:
            return json.dumps({"error": "FleetManager plugin not initialized"})

        try:
            if tool_name == "fleetmanager_status":
                return self._handle_fleetmanager_status(args)
            elif tool_name == "fleetmanager_run":
                return self._handle_fleetmanager_run(args)
            elif tool_name == "fleetmanager_agents":
                return self._handle_fleetmanager_agents(args)
            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})
        except Exception as e:
            logger.error(f"Error handling tool call {tool_name}: {e}")
            return json.dumps({"error": str(e)})

    def _handle_fleetmanager_status(self, args: Dict[str, Any]) -> str:
        """Handle fleetmanager_status tool call."""
        limit: int = int(args.get("limit", 10))

        if not self._backend:
            return json.dumps({"error": "Backend not initialized"})

        try:
            tasks: List[Dict[str, Any]] = cast(List[Dict[str, Any]], self._backend.get_pending_tasks())

            # Get agent information
            agents_dir = Path.home() / ".github" / "agents" / "code"
            agent_files = list(agents_dir.glob("*.py")) if agents_dir.exists() else []
            agent_names = [f.stem for f in agent_files if not f.name.startswith("_") and f.name != "__init__.py"]

            status: Dict[str, Any] = {
                "fleet_status": "operational" if self._backend else "unavailable",
                "pending_tasks": len(tasks),
                "tasks": tasks[:limit] if tasks else [],
                "available_agents": agent_names,
                "agent_count": len(agent_names),
                "timestamp": time.time(),
            }

            return json.dumps(status, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to get fleet status: {e}"})

    def _handle_fleetmanager_run(self, args: Dict[str, Any]) -> str:
        """Handle fleetmanager_run tool call."""
        limit: int = int(args.get("limit", 10))

        if not self._backend:
            return json.dumps({"error": "Backend not initialized"})

        # Import subprocess/sys at function scope so exception handlers can reference them
        import subprocess
        import sys

        try:
            # Set up the environment
            env = os.environ.copy()
            github_root = Path.home() / ".github"
            github_agents_orchestration = str(github_root / "agents" / "orchestration")
            github_agents_code = str(github_root / "agents" / "code")
            env["PYTHONPATH"] = ":".join(
                [
                    github_agents_orchestration,
                    github_agents_code,
                    env.get("PYTHONPATH", ""),
                ]
            ).strip(":")

            # Run fleetmanager
            cmd = [
                sys.executable,
                str(github_root / "agents" / "orchestration" / "fleetmanager.py"),
                "--limit",
                str(limit),
            ]
            result = subprocess.run(cmd, cwd=str(github_root), capture_output=True, text=True, timeout=30, env=env)

            output: Dict[str, Any] = {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "limit": limit,
                "timestamp": time.time(),
            }

            return json.dumps(output, indent=2)
        except subprocess.TimeoutExpired:
            return json.dumps({"error": "FleetManager execution timed out"})
        except Exception as e:
            return json.dumps({"error": f"Failed to run FleetManager: {e}"})

    def _handle_fleetmanager_agents(self, args: Dict[str, Any]) -> str:
        """Handle fleetmanager_agents tool call."""
        try:
            agents_dir = Path.home() / ".github" / "agents" / "code"
            if not agents_dir.exists():
                return json.dumps({"error": "Agents directory not found"})

            agent_files = list(agents_dir.glob("*.py"))
            agents: List[Dict[str, Any]] = []

            for f in agent_files:
                if f.name.startswith("_") or f.name == "__init__.py":
                    continue

                # Try to extract agent name and description
                agent_name = f.stem
                description = "No description available"

                try:
                    content = f.read_text()
                    # Look for docstring or comment at top
                    lines = content.split("\n")
                    for line in lines[:10]:  # Check first 10 lines
                        stripped = line.strip()
                        if stripped.startswith('"""') or stripped.startswith("'''"):
                            description = stripped.strip("\"'")
                            break
                        elif stripped.startswith("#") and len(stripped) > 10:
                            description = stripped[1:].strip()
                            break
                except Exception:
                    pass  # Keep default description

                agents.append({"name": agent_name, "description": description, "file": f.name})

            return json.dumps({"agents": agents, "count": len(agents), "timestamp": time.time()}, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to list agents: {e}"})

    def shutdown(self) -> None:
        """Clean shutdown of the plugin."""
        logger.info("Shutting down FleetManager plugin")
        self._backend = None
        self._initialized = False

    def on_session_end(self, messages: List[Dict[str, Any]]) -> None:
        """Called when a session ends."""
        logger.debug(f"FleetManager plugin: session end with {len(messages)} messages")
        # Could analyze session for fleet-related patterns here

    def on_turn_start(self, turn_number: int, message: str, **_kwargs: Any) -> None:
        """Called at the start of each turn."""
        logger.debug(f"FleetManager plugin: turn {turn_number} started")
        # Could prefetch fleet status or do periodic checks here
