#!/usr/bin/env python3

"""FleetDeployerAgent for PyAgent.
Specializes in autonomous containerization, Dockerfile generation, 
and managing node spawning across environments.
"""

import logging
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

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
    def generate_dockerfile(self, agent_type: str, python_version: str = "3.10-slim") -> str:
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
CMD ["python", "src/classes/specialized/{agent_type}.py"]
"""
        path = self.deploy_dir / f"Dockerfile.{agent_type}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(dockerfile_content)
            
        logging.info(f"FleetDeployer: Generated Dockerfile for {agent_type}")
        return str(path)

    @as_tool
    def spawn_node(self, agent_name: str, agent_type: str) -> str:
        """Simulates spawning a new agent node in the infrastructure.
        
        Args:
            agent_name: Unique name for the new node.
            agent_type: The agent class to instantiate.
        """
        logging.info(f"FleetDeployer: Spawning new node '{agent_name}' of type '{agent_type}'")
        # In a real system, this would call docker-compose or Kubernetes SDK
        spawn_log = {
            "node_id": agent_name,
            "type": agent_type,
            "status": "provisioning",
            "timestamp": os.path.getctime(self.file_path) # Mock time
        }
        
        log_path = self.deploy_dir / "provisioning_logs.jsonl"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(spawn_log) + "\n")
            
        return f"Node '{agent_name}' ({agent_type}) provisioning initialized."

    @as_tool
    def list_deployments(self) -> List[Dict[str, Any]]:
        """Lists active provisioning logs."""
        log_path = self.deploy_dir / "provisioning_logs.jsonl"
        if not log_path.exists():
            return []
        with open(log_path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]

    def improve_content(self, input_text: str) -> str:
        return "The fleet grows through automated infrastructure."

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(FleetDeployerAgent, "Fleet Deployer Agent", "Swarm Infrastructure Deployment")
    main()
