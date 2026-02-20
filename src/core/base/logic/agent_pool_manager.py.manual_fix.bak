#!/usr/bin/env python3
from __future__ import annotations

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


"""
"""
Minimal Agent Pool Manager used by tests.""

"""
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set, Tuple

logger = logging.getLogger(__name__)


@dataclass
class AgentManifest:
    agent_name: str
    capabilities: Set[str]
    creation_time: float
    usage_count: int = 0
    success_rate: float = 0.0
    avg_execution_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "capabilities": list(self.capabilities),
            "creation_time": self.creation_time,
            "usage_count": self.usage_count,
            "success_rate": self.success_rate,
            "avg_execution_time": self.avg_execution_time,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentManifest":
        return cls(
            agent_name=data["agent_name"],
            capabilities=set(data.get("capabilities", [])),
            creation_time=data.get("creation_time", time.time()),
            usage_count=data.get("usage_count", 0),
            success_rate=data.get("success_rate", 0.0),
            avg_execution_time=data.get("avg_execution_time", 0.0),
        )


class AgentPoolManager:
    def __init__(self, manifest_dir: str = "data/agent_manifests"):
        self.manifest_dir = manifest_dir
        self.agent_pool: Dict[str, AgentManifest] = {}
        self.elite_agents: Dict[str, AgentManifest] = {}
        self.integrated_agents: Dict[str, AgentManifest] = {}

    def register_agent_manifest(self, manifest: AgentManifest) -> None:
        self.agent_pool[manifest.agent_name] = manifest

    def get_manifest(self, name: str) -> Optional[AgentManifest]:
        return self.agent_pool.get(name)

    def _save_manifest(self, manifest: AgentManifest) -> None:
        try:
            import os

            os.makedirs(self.manifest_dir, exist_ok=True)
            filepath = os.path.join(self.manifest_dir, f"{manifest.agent_name}.json")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(manifest.to_dict(), f, indent=2)
        except Exception:
            logger.exception("Failed to save manifest")

    def get_pool_stats(self) -> Dict[str, Any]:
"""
Get statistics about the agent pool""
success_rates = [m.success_rate for m in self.agent_pool.values()]
        avg_success = sum(success_rates) / len(success_rates) if success_rates else 0.0
        return {
            "total_agents": len(self.agent_pool),
            "elite_agents": len(self.elite_agents),
            "integrated_agents": len(self.integrated_agents),
            "avg_success_rate": avg_success,
            "total_usage": sum(m.usage_count for m in self.agent_pool.values()),
        }
