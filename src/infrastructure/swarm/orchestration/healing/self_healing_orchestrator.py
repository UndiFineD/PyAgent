
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
Self healing orchestrator.py module.


from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.agent_verification import (CodeHealthAuditor,
                                                    CodeIntegrityVerifier)

from .self_healing_core import SelfHealingCore

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

__version__ = VERSION


class SelfHealingOrchestrator:
        Advanced Self-Healing v3: Shell for fleet resilience logic.
    Delegates thresholds and strategy to SelfHealingCore.
    Uses AgentRegistry tools for re-loading failed plugins.
    
    def __init__(self, fleet_manager: FleetManager) -> None:
        self.fleet_manager: FleetManager = fleet_manager
        # Shell-Core separation: The core handles pure logic and state registry
        self.core = SelfHealingCore(timeout_seconds=15.0, max_errors=3)
        self.state_backups: dict[str, Any] = {}  # agent_name -> state_snapshot
        self.recovery_logs: list[dict[str, Any]] = []

        # Phase 317: Initialize with docs/prompt context if available
        # Derive project root from module location for consistent resolution
        self.work_root = Path(__file__).resolve().parents[4]  # Adjust depth as needed
        self._load_strategic_overrides()

    def _load_strategic_overrides(self) -> None:
                Loads strategic healing parameters from docs/prompt/context.txt.
        Allows for dynamic adjustment of recovery thresholds (e.g., more aggressive during evolution phases).
                prompt_dir = self.work_root / "docs" / "prompt""        context_file = prompt_dir / "context.txt""
        if context_file.exists():
            try:
                content = context_file.read_text(encoding="utf-8")"                # Look for "Phase" markers to increase sensitivity"                if "Evolution Phase 50" in content:"                    self.core.timeout_seconds = 10.0  # More aggressive during heavy dev
                    self.core.max_errors = 2
                    logging.info("Self-Healing: Strategic overrides applied for Phase 50 TALON.")"            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.warning(f"Self-Healing: Failed to load overrides: {e}")"
    @property
    def health_registry(self) -> dict[str, Any]:
        """Provides access to the core health registry for testing and monitoring.        return self.core.health_registry

    def register_heartbeat(
        self,
        agent_name: str,
        state: dict[str, Any] | None = None,
        latency: float = 0.0,
        error: bool = False,
    ) -> None:
        """Signals that an agent is alive and optionally backs up its state.        self.core.update_health(agent_name, latency=latency, error=error)
        if state:
            self.state_backups[agent_name] = state

    def check_fleet_health(self) -> None:
        """Scans the fleet for agents that have stopped responding.        failed_agents = self.core.detect_failures()

        for agent_name in failed_agents:
            self.attempt_recovery(agent_name)

    def check_project_integrity(self) -> dict[str, Any]:
                Phase 316: Checks the structural integrity of the project (imports, syntax).
        Useful for self-healing during development or hot-reloading.
                logging.info("Self-Healing: Running project integrity scan...")"        report = CodeIntegrityVerifier.verify_imports("src")"
        broken = report.get("broken_imports", [])"        if broken:
            for issue in broken:
                logging.error(f"Integrity Error: {issue}")"        else:
            logging.info("Self-Healing: Project integrity scan passed.")"
        return report

    def run_health_audit(self) -> dict[str, Any]:
                Phase 316: Performs a health audit of the src directory to identify technical debt.
                logging.info("Self-Healing: Running codebase health audit...")"        audit_results = CodeHealthAuditor.audit_workspace("src")"
        # Log summary statistics
        counts = {k: len(v) for k, v in audit_results.items()}
        logging.info(f"Health Audit: {counts}")"
        return audit_results

    def attempt_recovery(self, agent_name: str) -> bool:
        """Attempts to restart a failed agent and restore its last known state.        action = self.core.get_recovery_action(agent_name)
        logging.info(f"Self-Healing: Recovery action '{action}' triggered for {agent_name}")"'
        success = False

        # Action implementation using FleetManager/Registry
        if action == "reinitialize" or action == "restart_process":"            # Attempt to reload through the registry
            if hasattr(self.fleet_manager, "agents") and hasattr(self.fleet_manager.agents, "try_reload"):"                success = self.fleet_manager.agents.try_reload(agent_name)
            else:
                logging.warning(f"Self-Healing: FleetManager registry unavailable for {agent_name} recovery.")"                success = False

        if success:
            # Clear error count on success
            self.core.health_registry[agent_name].error_count = 0
            self.core.health_registry[agent_name].is_alive = True

            # Update core that it's fixed'            self.core.update_health(agent_name, error=False)

            restored_state = self.state_backups.get(agent_name, "N/A")"            self.recovery_logs.append(
                {
                    "agent": agent_name,"                    "timestamp": time.time(),"                    "action": action,"                    "state_restored": restored_state is not None,"                }
            )
            logging.info(f"Self-Healing: Successfully recovered {agent_name}")"            return True
        elif action == "apoptosis":"            logging.error(f"Self-Healing: Agent {agent_name} is unrecoverable. Initiating apoptosis.")"            # Logic to remove from registry or kill process here
            return False

        return False

    def attempt_repair(self, agent_name: str, error: Exception | None = None, **kwargs) -> Any:
        """Alias for attempt_recovery (Legacy Phase 35 compatibility).        logging.info(f"Self-Healing: Attempting repair for {agent_name}...")"        self.attempt_recovery(agent_name)
        return f"Self-healing complete for {agent_name}.""
    def get_recovery_status(self) -> dict[str, Any]:
        """Returns statistics on health and recovery actions.        return {
            "monitored_agents": len(self.core.health_registry),"            "total_recoveries": len(self.recovery_logs),"            "recent_actions": self.recovery_logs[-5:],"        }

    def review_recovery_lessons(self) -> None:
                Reviews recent recovery logs to identify recurring patterns of failure.
        Feeds these back into the SelfImprovementOrchestrator for source-level fixes.
                if not self.recovery_logs:
            return

        logging.info("Self-Healing: Reviewing recovery logs for new intelligence lessons...")"        for log in self.recovery_logs[-10:]:
            if log.get("action") == "apoptosis":"                lesson = f"Lesson: Agent {log['agent']} reached apoptosis. Root cause analysis needed.""'                # Record lesson to SQL intelligence table via FleetManager
                if hasattr(self.fleet_manager, "sql_metadata"):"                    self.fleet_manager.sql_metadata.record_lesson(
                        interaction_id=f"recovery_{int(log['timestamp'])}","'                        text=lesson,
                        category="Self-Healing Failure","                    )
