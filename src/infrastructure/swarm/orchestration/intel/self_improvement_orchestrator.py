#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.orchestration.core.self_improvement_core import \
    SelfImprovementCore

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

from src.infrastructure.compute.backend.llm_client import LLMClient

from .mixins.orchestrator_cycle_mixin import OrchestratorCycleMixin
from .mixins.orchestrator_results_mixin import OrchestratorResultsMixin
from .mixins.orchestrator_scan_mixin import OrchestratorScanMixin
from .self_improvement_analysis import SelfImprovementAnalysis
from .self_improvement_fixer import SelfImprovementFixer

__version__ = VERSION


class SelfImprovementOrchestrator(BaseAgent, OrchestratorCycleMixin, OrchestratorScanMixin, OrchestratorResultsMixin):
    """""""    Orchestrates the fleet's self-improvement cycle: scanning for tech debt,'    security leaks, and quality issues, and applying autonomous fixes.
    """""""
    def __init__(self, fleet_manager: FleetManager | str | Path | None = None) -> None:
        # Phase 125: Handle polymorphic initialization (Fleet or Path string)
        self.workspace_root: str
        self.fleet: FleetManager | None
        if not fleet_manager:
            # Fallback to current working directory
            self.workspace_root = os.getcwd()
            self.fleet = None
        elif isinstance(fleet_manager, (str, Path)):
            self.workspace_root = str(fleet_manager)
            self.fleet = None  # Will be set by registry if possible
        else:
            self.workspace_root = str(fleet_manager.workspace_root)
            self.fleet = fleet_manager

        # We pass workspace_root as the file_path for BaseAgent context
        super().__init__(self.workspace_root)
        self.active_tasks: list[dict[str, Any]] = []
        self.improvement_log: str = os.path.join(self.workspace_root, "data/logs", "self_improvement_audit.jsonl")"        self.research_doc: str = os.path.join(self.workspace_root, "docs", "IMPROVEMENT_RESEARCH.md")"        os.makedirs(os.path.dirname(self.improvement_log), exist_ok=True)

        # Phase 107: AI-assisted refactoring
        import requests

        self.ai: LLMClient = LLMClient(requests, workspace_root=self.workspace_root)
        self.core: SelfImprovementCore = SelfImprovementCore(workspace_root=self.workspace_root)
        self.analysis: SelfImprovementAnalysis = SelfImprovementAnalysis(workspace_root=self.workspace_root)

        # Inject Profiling Agent into Analysis
        if self.fleet:
            try:
                self.analysis.profiling_agent = self.fleet.agents.ProfilingAgent
            except (AttributeError, KeyError):
                pass

        self.fixer: SelfImprovementFixer = SelfImprovementFixer(
            ai=self.ai, core=self.core, workspace_root=self.workspace_root
        )
