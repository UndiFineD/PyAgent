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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""FleetDeployerAgent for PyAgent.
Specializes in autonomous containerization, Dockerfile generation, 
and managing node spawning across environments.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION

class FleetDeployerAgent(BaseAgent):
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
            "timestamp": time.time() if 'time' in globals() else 0
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
                    except: continue
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
