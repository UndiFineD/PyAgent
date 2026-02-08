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
Agent Pool Manager - Self-evolving agent pool with task-driven creation and evolution
Based on the Autonomous Orchestration Ecosystem from agent-orchestrator-self-evolving-subagent
"""

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set, Tuple
from enum import Enum
import statistics

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.models.communication_models import CascadeContext

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent lifecycle status"""
    ACTIVE = "active"
    ELITE = "elite"
    DEPRECATED = "deprecated"
    INTEGRATED = "integrated"


@dataclass
class AgentManifest:
    """Metadata and metrics for an agent"""
    agent_name: str
    capabilities: Set[str]
    creation_time: float
    usage_count: int = 0
    success_rate: float = 0.0
    avg_execution_time: float = 0.0
    synergy_hints: List[Dict[str, Any]] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    status: AgentStatus = AgentStatus.ACTIVE
    lineage: List[str] = field(default_factory=list)  # Parent agents for integrated agents

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "capabilities": list(self.capabilities),
            "creation_time": self.creation_time,
            "usage_count": self.usage_count,
            "success_rate": self.success_rate,
            "avg_execution_time": self.avg_execution_time,
            "synergy_hints": self.synergy_hints,
            "constraints": self.constraints,
            "status": self.status.value,
            "lineage": self.lineage
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentManifest':
        return cls(
            agent_name=data["agent_name"],
            capabilities=set(data["capabilities"]),
            creation_time=data["creation_time"],
            usage_count=data.get("usage_count", 0),
            success_rate=data.get("success_rate", 0.0),
            avg_execution_time=data.get("avg_execution_time", 0.0),
            synergy_hints=data.get("synergy_hints", []),
            constraints=data.get("constraints", []),
            status=AgentStatus(data.get("status", "active")),
            lineage=data.get("lineage", [])
        )


@dataclass
class TaskRequirements:
    """Requirements analysis for a task"""
    required_capabilities: Set[str]
    complexity_score: float  # 0.0 to 1.0
    estimated_duration: float  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentPoolManager:
    """
    Self-evolving agent pool manager
    Implements the Autonomous Orchestration Ecosystem pattern
    """

    def __init__(self, manifest_dir: str = "data/agent_manifests"):
        self.manifest_dir = manifest_dir
        self.agent_pool: Dict[str, AgentManifest] = {}
        self.elite_agents: Dict[str, AgentManifest] = {}
        self.integrated_agents: Dict[str, AgentManifest] = {}
        self._ensure_manifest_dir()

    def _ensure_manifest_dir(self):
        """Ensure manifest directory exists"""
        import os
        os.makedirs(self.manifest_dir, exist_ok=True)

    def register_agent(self, agent: BaseAgent, capabilities: Set[str]):
        """Register a new agent in the pool"""
        manifest = AgentManifest(
            agent_name=agent.name,
            capabilities=capabilities,
            creation_time=time.time()
        )

        self.agent_pool[agent.name] = manifest
        self._save_manifest(manifest)
        logger.info(f"Registered agent: {agent.name} with capabilities: {capabilities}")

    def update_agent_metrics(self, agent_name: str, success: bool, execution_time: float):
        """Update performance metrics for an agent"""
        if agent_name in self.agent_pool:
            manifest = self.agent_pool[agent_name]
            manifest.usage_count += 1

            # Update success rate
            total_successes = int(manifest.success_rate * (manifest.usage_count - 1))
            if success:
                total_successes += 1
            manifest.success_rate = total_successes / manifest.usage_count

            # Update average execution time
            if manifest.usage_count == 1:
                manifest.avg_execution_time = execution_time
            else:
                manifest.avg_execution_time = (
                    (manifest.avg_execution_time * (manifest.usage_count - 1)) + execution_time
                ) / manifest.usage_count

            self._save_manifest(manifest)

            # Check for elite promotion
            self._check_elite_promotion(manifest)

    def analyze_task_requirements(self, task_description: str, context: CascadeContext) -> TaskRequirements:
        """Analyze task requirements and extract needed capabilities"""
        # This is a simplified implementation - in practice, this would use LLM analysis
        capabilities = set()

        # Extract keywords that indicate capabilities
        task_lower = task_description.lower()

        capability_keywords = {
            "code": ["coding", "programming", "development", "refactor"],
            "research": ["research", "analyze", "investigate", "study"],
            "writing": ["write", "document", "create", "generate"],
            "testing": ["test", "validate", "verify", "check"],
            "security": ["security", "vulnerability", "exploit", "penetration"],
            "database": ["database", "query", "sql", "data"],
            "api": ["api", "rest", "endpoint", "integration"],
            "frontend": ["frontend", "ui", "interface", "component"],
            "backend": ["backend", "server", "infrastructure", "deployment"]
        }

        for capability, keywords in capability_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                capabilities.add(capability)

        # Estimate complexity (simplified)
        complexity_score = min(1.0, len(capabilities) * 0.2 + len(task_description.split()) * 0.001)

        # Estimate duration (simplified)
        estimated_duration = 60 + (complexity_score * 240)  # 1-5 minutes

        return TaskRequirements(
            required_capabilities=capabilities,
            complexity_score=complexity_score,
            estimated_duration=estimated_duration
        )

    def find_optimal_agent(self, requirements: TaskRequirements) -> Tuple[Optional[str], float]:
        """
        Find the optimal agent for a task based on coverage rate
        Returns (agent_name, coverage_rate)
        """
        best_agent = None
        best_coverage = 0.0
        best_capability_count = 0

        # Check elite agents first
        for agent_name, manifest in self.elite_agents.items():
            coverage = self._calculate_coverage(requirements, manifest)
            capability_count = len(manifest.capabilities)

            if (coverage > best_coverage or
                (coverage == best_coverage and capability_count > best_capability_count)):
                best_coverage = coverage
                best_agent = agent_name
                best_capability_count = capability_count

        # Check regular pool
        for agent_name, manifest in self.agent_pool.items():
            if manifest.status != AgentStatus.ACTIVE:
                continue

            coverage = self._calculate_coverage(requirements, manifest)
            capability_count = len(manifest.capabilities)

            if (coverage > best_coverage or
                (coverage == best_coverage and capability_count > best_capability_count)):
                best_coverage = coverage
                best_agent = agent_name
                best_capability_count = capability_count

        return best_agent, best_coverage

    def decide_agent_action(self, coverage_rate: float, requirements: TaskRequirements) -> str:
        """
        Decide what action to take based on coverage rate
        Based on the decision matrix from the autonomous orchestration ecosystem
        """
        if coverage_rate >= 0.9:
            return "use_existing"
        elif coverage_rate >= 0.6:
            return "integrate_agents"
        else:
            return "create_new"

    def create_integrated_agent(self, requirements: TaskRequirements, candidate_agents: List[str]) -> str:
        """Create an integrated agent from multiple candidates"""
        # Find best combination of agents
        best_combination = self._find_best_integration(requirements, candidate_agents)

        if not best_combination:
            return self.create_specialized_agent(requirements)

        # Create integrated agent name
        integrated_name = f"integrated_{'_'.join(sorted(best_combination))}_{int(time.time())}"

        # Combine capabilities
        combined_capabilities = set()
        lineage = []

        for agent_name in best_combination:
            if agent_name in self.agent_pool:
                manifest = self.agent_pool[agent_name]
                combined_capabilities.update(manifest.capabilities)
                lineage.append(agent_name)

        # Create manifest for integrated agent
        manifest = AgentManifest(
            agent_name=integrated_name,
            capabilities=combined_capabilities,
            creation_time=time.time(),
            lineage=lineage,
            status=AgentStatus.INTEGRATED
        )

        self.integrated_agents[integrated_name] = manifest
        self._save_manifest(manifest)

        logger.info(f"Created integrated agent: {integrated_name} from {best_combination}")
        return integrated_name

    def create_specialized_agent(self, requirements: TaskRequirements) -> str:
        """Create a new specialized agent for specific requirements"""
        agent_name = f"specialized_{'_'.join(sorted(requirements.required_capabilities))}_{int(time.time())}"

        manifest = AgentManifest(
            agent_name=agent_name,
            capabilities=requirements.required_capabilities.copy(),
            creation_time=time.time()
        )

        self.agent_pool[agent_name] = manifest
        self._save_manifest(manifest)

        logger.info(f"Created specialized agent: {agent_name} for capabilities: {requirements.required_capabilities}")
        return agent_name

    def _calculate_coverage(self, requirements: TaskRequirements, manifest: AgentManifest) -> float:
        """Calculate how well an agent covers the task requirements"""
        if not requirements.required_capabilities:
            return 1.0

        matching_capabilities = requirements.required_capabilities.intersection(manifest.capabilities)
        coverage = len(matching_capabilities) / len(requirements.required_capabilities)

        # Boost score for elite agents
        if manifest.status == AgentStatus.ELITE:
            coverage *= 1.2

        return min(1.0, coverage)

    def _find_best_integration(self, requirements: TaskRequirements, candidates: List[str]) -> Optional[List[str]]:
        """Find the best combination of agents for integration"""
        # Simplified: just return top 2 candidates if they together provide good coverage
        if len(candidates) < 2:
            return None

        # Sort by individual coverage
        candidate_scores = []
        for agent_name in candidates:
            if agent_name in self.agent_pool:
                manifest = self.agent_pool[agent_name]
                coverage = self._calculate_coverage(requirements, manifest)
                candidate_scores.append((agent_name, coverage))

        candidate_scores.sort(key=lambda x: x[1], reverse=True)

        # Try combinations of top candidates
        for i in range(min(3, len(candidate_scores))):
            for j in range(i + 1, min(4, len(candidate_scores))):
                combo = [candidate_scores[i][0], candidate_scores[j][0]]
                combined_capabilities = set()

                for agent_name in combo:
                    if agent_name in self.agent_pool:
                        combined_capabilities.update(self.agent_pool[agent_name].capabilities)

                combo_coverage = len(requirements.required_capabilities.intersection(combined_capabilities)) / len(requirements.required_capabilities)

                if combo_coverage >= 0.8:  # Good combined coverage
                    return combo

        return None

    def _check_elite_promotion(self, manifest: AgentManifest):
        """Check if an agent should be promoted to elite status"""
        if (manifest.usage_count >= 10 and
            manifest.success_rate >= 0.8 and
            manifest.status == AgentStatus.ACTIVE):

            manifest.status = AgentStatus.ELITE
            self.elite_agents[manifest.agent_name] = manifest
            self._save_manifest(manifest)
            logger.info(f"Promoted agent to elite: {manifest.agent_name}")

    def _save_manifest(self, manifest: AgentManifest):
        """Save agent manifest to disk"""
        import os
        filepath = os.path.join(self.manifest_dir, f"{manifest.agent_name}.json")

        try:
            with open(filepath, 'w') as f:
                json.dump(manifest.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save manifest for {manifest.agent_name}: {e}")

    def load_manifests(self):
        """Load all agent manifests from disk"""
        import os
        import glob

        pattern = os.path.join(self.manifest_dir, "*.json")
        for filepath in glob.glob(pattern):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    manifest = AgentManifest.from_dict(data)

                    if manifest.status == AgentStatus.ELITE:
                        self.elite_agents[manifest.agent_name] = manifest
                    elif manifest.status == AgentStatus.INTEGRATED:
                        self.integrated_agents[manifest.agent_name] = manifest
                    else:
                        self.agent_pool[manifest.agent_name] = manifest

            except Exception as e:
                logger.error(f"Failed to load manifest {filepath}: {e}")

    def get_pool_stats(self) -> Dict[str, Any]:
        """Get statistics about the agent pool"""
        return {
            "total_agents": len(self.agent_pool),
            "elite_agents": len(self.elite_agents),
            "integrated_agents": len(self.integrated_agents),
            "avg_success_rate": statistics.mean([m.success_rate for m in self.agent_pool.values()]) if self.agent_pool else 0.0,
            "total_usage": sum(m.usage_count for m in self.agent_pool.values())
        }
