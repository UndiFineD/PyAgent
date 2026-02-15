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
FleetDeployerAgent - Fleet lifecycle management and containerization

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Import FleetDeployerAgent from src.core.base.lifecycle and instantiate with a path to the agent file (e.g., FleetDeployerAgent("path/to/file")).
- Use exposed async tools to generate Dockerfiles, spawn nodes, list active nodes, scale up instances, and perform consensus-driven deploy workflows from orchestration code or other agents.
- Intended for automation pipelines or higher-level orchestrators that coordinate agent swarms and deployments.

WHAT IT DOES:
- Provides async tool-wrapped methods to generate simple Dockerfiles for specific agent types, append provisioning logs, and read active nodes from those logs.
- Simulates node provisioning via spawn_node and supports bulk scaling via scale_up by invoking spawn_node repeatedly.
- Persists artifacts and logs under a deploy/ directory created at initialization and exposes operations suitable for integration with higher-level deployment flows.

WHAT IT SHOULD DO BETTER:
- Replace file-based simulation with integration to real orchestration APIs (Docker SDK, Kubernetes API, cloud provider APIs) for idempotent, observable, and secure provisioning.
- Add robust error handling, input validation, transactional semantics (rollback on partial failures), and concurrency controls to avoid race conditions when multiple processes write logs.
- Improve metadata (unique node IDs, timestamps in UTC, lifecycle states), structured logging, metrics, and tests; support secure secrets handling and configurable templates for Dockerfiles (and secure base images).

FILE CONTENT SUMMARY:
FleetDeployerAgent for PyAgent.
Specializes in autonomous containerization, Dockerfile generation,
and managing node spawning across environments.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from pathlib import Path

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class FleetDeployerAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Manages the lifecycle of fleet nodes, including containerization and deployment."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.deploy_dir = Path("deploy")
        self.deploy_dir.mkdir(parents=True, exist_ok=True)
        self._system_prompt = (
            "You are the Fleet Deployer Agent. Your mission is to scale the agent swarm. "
            "You generate Dockerfiles, docker-compose configurations, and deployment logs. "
            "You can spawn new agent nodes autonomously and manage their lifecycle."
        )

    @as_tool
    async def generate_dockerfile(self, agent_type: str, python_version: str = "3.10-slim") -> str:
        """Generates a specialized Dockerfile for an agent type.






        Args:
            agent_type: The type of agent (e.g., 'LinguisticAgent').
            python_version: Base image Python version.





        """
        dockerfile_content = f"""FROM python:{python_version}

WORKDIR /app
COPY requirements.txt .




RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV AGENT_TYPE={agent_type}





CMD ["python", "src/logic/agents/specialized/{agent_type}.py"]
"""
        path = self.deploy_dir / f"Dockerfile.{agent_type}"
        # Phase 287: Use asyncio.to_thread for blocking I/O if needed,
        # but small writes are usually fine. However, we'll be consistent.

        def write_file() -> str:
            with open(path, "w", encoding="utf-8") as f:
                f.write(dockerfile_content)

        await asyncio.to_thread(write_file)

        logging.info(f"FleetDeployer: Generated Dockerfile for {agent_type}")
        return str(path)

    @as_tool
    async def spawn_node(self, agent_name: str, agent_type: str) -> str:
        """Simulates spawning a new agent node in the infrastructure.

        Args:
            agent_name: Unique name for the new node.
            agent_type: The agent class to instantiate.
        """
        logging.info(f"FleetDeployer: Spawning new node '{agent_name}' of type '{agent_type}'")

        spawn_log = {
            "node_id": agent_name,
            "type": agent_type,
            "status": "provisioning",
            "timestamp": time.time() if "time" in globals() else 0,
        }

        log_path = self.deploy_dir / "provisioning_logs.jsonl"

        def append_log() -> str:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(spawn_log) + "\n")

        await asyncio.to_thread(append_log)

        return f"Node '{agent_name}' ({agent_type}) provisioning initialized."

    @as_tool
    async def list_active_nodes(self) -> list[str]:
        """Lists nodes currently marked as active in the provisioning logs."""
        log_path = self.deploy_dir / "provisioning_logs.jsonl"
        if not log_path.exists():
            return []

        def read_logs() -> str:
            nodes = []
            with open(log_path, encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        nodes.append(data.get("node_id", "unknown"))
                    except json.JSONDecodeError:
                        continue
            return nodes

        return await asyncio.to_thread(read_logs)

    @as_tool
    async def scale_up(self, agent_type: str, count: int = 1) -> str:
        """Scales up the number of instances for a specific agent type."""
        results = []
        for i in range(count):
            node_name = f"{agent_type.lower()}-{i}-{os.urandom(2).hex()}"
            res = await self.spawn_node(node_name, agent_type)
            results.append(res)
        return "\n".join(results)

    @as_tool
    async def consensus_driven_deploy(self, agent_type: str, node_name: str) -> str:
        """Depl
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from pathlib import Path

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class FleetDeployerAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Manages the lifecycle of fleet nodes, including containerization and deployment."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.deploy_dir = Path("deploy")
        self.deploy_dir.mkdir(parents=True, exist_ok=True)
        self._system_prompt = (
            "You are the Fleet Deployer Agent. Your mission is to scale the agent swarm. "
            "You generate Dockerfiles, docker-compose configurations, and deployment logs. "
            "You can spawn new agent nodes autonomously and manage their lifecycle."
        )

    @as_tool
    async def generate_dockerfile(self, agent_type: str, python_version: str = "3.10-slim") -> str:
        """Generates a specialized Dockerfile for an agent type.






        Args:
            agent_type: The type of agent (e.g., 'LinguisticAgent').
            python_version: Base image Python version.





        """
        dockerfile_content = f"""FROM python:{python_version}

WORKDIR /app
COPY requirements.txt .




RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV AGENT_TYPE={agent_type}





CMD ["python", "src/logic/agents/specialized/{agent_type}.py"]
"""
        path = self.deploy_dir / f"Dockerfile.{agent_type}"
        # Phase 287: Use asyncio.to_thread for blocking I/O if needed,
        # but small writes are usually fine. However, we'll be consistent.

        def write_file() -> str:
            with open(path, "w", encoding="utf-8") as f:
                f.write(dockerfile_content)

        await asyncio.to_thread(write_file)

        logging.info(f"FleetDeployer: Generated Dockerfile for {agent_type}")
        return str(path)

    @as_tool
    async def spawn_node(self, agent_name: str, agent_type: str) -> str:
        """Simulates spawning a new agent node in the infrastructure.

        Args:
            agent_name: Unique name for the new node.
            agent_type: The agent class to instantiate.
        """
        logging.info(f"FleetDeployer: Spawning new node '{agent_name}' of type '{agent_type}'")

        spawn_log = {
            "node_id": agent_name,
            "type": agent_type,
            "status": "provisioning",
            "timestamp": time.time() if "time" in globals() else 0,
        }

        log_path = self.deploy_dir / "provisioning_logs.jsonl"

        def append_log() -> str:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(spawn_log) + "\n")

        await asyncio.to_thread(append_log)

        return f"Node '{agent_name}' ({agent_type}) provisioning initialized."

    @as_tool
    async def list_active_nodes(self) -> list[str]:
        """Lists nodes currently marked as active in the provisioning logs."""
        log_path = self.deploy_dir / "provisioning_logs.jsonl"
        if not log_path.exists():
            return []

        def read_logs() -> str:
            nodes = []
            with open(log_path, encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        nodes.append(data.get("node_id", "unknown"))
                    except json.JSONDecodeError:
                        continue
            return nodes

        return await asyncio.to_thread(read_logs)

    @as_tool
    async def scale_up(self, agent_type: str, count: int = 1) -> str:
        """Scales up the number of instances for a specific agent type."""
        results = []
        for i in range(count):
            node_name = f"{agent_type.lower()}-{i}-{os.urandom(2).hex()}"
            res = await self.spawn_node(node_name, agent_type)
            results.append(res)
        return "\n".join(results)

    @as_tool
    async def consensus_driven_deploy(self, agent_type: str, node_name: str) -> str:
        """Deploys an agent, but only after reaching consensus (Mock)."""
        logging.info(f"FleetDeployer: Requesting consensus for deployment of {node_name}...")
        # Mock approval
        return await self.spawn_node(node_name, agent_type)
