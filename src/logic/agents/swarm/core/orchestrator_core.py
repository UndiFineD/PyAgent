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
OrchestratorCore: Pure logic for swarm coordination.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Set
from src.core.base.lifecycle.agent_core import AgentCore

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]


class OrchestratorCore(AgentCore):
    """
    Pure logic core for the OrchestratorAgent.
    Handles decision making, consensus logic, and scoring.
    """

    def __init__(self, workspace_root: str) -> None:
        super().__init__(workspace_root=workspace_root)
        self.workspace_root_path = Path(workspace_root)

    def should_execute_agent(self, agent_name: str, selective_agents: Set[str]) -> bool:
        """Determines if an agent should run."""
        if not selective_agents:
            return True
        return agent_name.lower() in [s.lower() for s in selective_agents]

    def get_timeout_for_agent(
        self, agent_name: str, timeout_map: Dict[str, int], default: int = 120
    ) -> int:
        """Calculates timeout for a specific agent."""
        return timeout_map.get(agent_name.lower(), default)

    def check_files_ready(self, code_file: Path) -> bool:
        """Check if all supporting files exist and have content."""
        base = code_file.stem
        dir_path = code_file.parent
        required = [
            dir_path / f"{base}.description.md",
            dir_path / f"{base}.changes.md",
            dir_path / f"{base}.errors.md",
            dir_path / f"{base}.improvements.md",
        ]

        for req in required:
            if not req.exists():
                return False
            # Optimization: Rust could eventually handle high-speed content validation
            content = req.read_text(encoding="utf-8").strip()
            if len(content) < 100:
                return False
        return True

    def calculate_improvement_score(
        self, files_processed: int, files_modified: int
    ) -> float:
        """
        Calculates a global improvement score.
        Rust hook candidate for phase 132.
        """
        if rc and hasattr(rc, "calculate_efficiency_score"):
            # Mocking usage of a rust function if it existed or using a generic one
            try:
                return rc.score_efficiency(float(files_modified), files_processed)  # type: ignore[attr-defined]
            except Exception:
                pass

        if files_processed == 0:
            return 0.0
        return (files_modified / files_processed) * 100.0

    async def validate_with_consensus(
        self, task: str, proposals: Dict[str, str], log_path: Path
    ) -> Dict[str, Any]:
        """
        Validates proposals using the ByzantineConsensusAgent via logical delegation.
        """
        from src.logic.agents.security.byzantine_consensus_agent import (
            ByzantineConsensusAgent,
        )

        consensus_agent = ByzantineConsensusAgent(str(log_path))
        return await consensus_agent.run_committee_vote(task, proposals)
