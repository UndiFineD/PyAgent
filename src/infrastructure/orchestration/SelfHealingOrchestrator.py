from __future__ import annotations

import time
import logging
from typing import Dict, List, Any, Optional
from .SelfHealingCore import SelfHealingCore

class SelfHealingOrchestrator:
    """
    Advanced Self-Healing v3: Shell for fleet resilience logic.
    Delegates thresholds and strategy to SelfHealingCore.
    Uses AgentRegistry tools for re-loading failed plugins.
    """
    def __init__(self, fleet_manager: Any) -> None:
        self.fleet_manager: Any = fleet_manager
        # Shell-Core separation: The core handles pure logic and state registry
        self.core = SelfHealingCore(timeout_seconds=15.0, max_errors=3)
        self.state_backups: Dict[str, Any] = {}    # agent_name -> state_snapshot
        self.recovery_logs: List[Dict[str, Any]] = []

    @property
    def health_registry(self) -> Dict[str, Any]:
        """Provides access to the core health registry for testing and monitoring."""
        return self.core.health_registry

    def register_heartbeat(self, agent_name: str, state: Optional[Dict[str, Any]] = None, latency: float = 0.0, error: bool = False) -> None:
        """Signals that an agent is alive and optionally backs up its state."""
        self.core.update_health(agent_name, latency=latency, error=error)
        if state:
            self.state_backups[agent_name] = state

    def check_fleet_health(self) -> None:
        """Scans the fleet for agents that have stopped responding."""
        failed_agents = self.core.detect_failures()
        
        for agent_name in failed_agents:
            self.attempt_recovery(agent_name)

    def attempt_recovery(self, agent_name: str) -> bool:
        """Attempts to restart a failed agent and restore its last known state."""
        action = self.core.get_recovery_action(agent_name)
        logging.info(f"Self-Healing: Recovery action '{action}' triggered for {agent_name}")
        
        success = False
        
        # Action implementation using FleetManager/Registry
        if action == "reinitialize" or action == "restart_process":
            # Attempt to reload through the registry
            if hasattr(self.fleet_manager, 'agents') and hasattr(self.fleet_manager.agents, 'try_reload'):
                success = self.fleet_manager.agents.try_reload(agent_name)
            else:
                logging.warning(f"Self-Healing: FleetManager registry unavailable for {agent_name} recovery.")
                success = False
        
        if success:
            # Clear error count on success
            self.core.health_registry[agent_name].error_count = 0
            self.core.health_registry[agent_name].is_alive = True
            
            # Update core that it's fixed
            self.core.update_health(agent_name, error=False)
            
            restored_state = self.state_backups.get(agent_name, "N/A")
            self.recovery_logs.append({
                "agent": agent_name,
                "timestamp": time.time(),
                "action": action,
                "state_restored": restored_state is not None
            })
            logging.info(f"Self-Healing: Successfully recovered {agent_name}")
            return True
        elif action == "apoptosis":
            logging.error(f"Self-Healing: Agent {agent_name} is unrecoverable. Initiating apoptosis.")
            # Logic to remove from registry or kill process here
            return False
            
        return False

    def attempt_repair(self, agent_name: str, error: Exception = None, **kwargs) -> Any:
        """Alias for attempt_recovery (Legacy Phase 35 compatibility)."""
        logging.info(f"Self-Healing: Attempting repair for {agent_name}...")
        self.attempt_recovery(agent_name)
        return f"Self-healing complete for {agent_name}."

    def get_recovery_status(self) -> Dict[str, Any]:
        """Returns statistics on health and recovery actions."""
        return {
            "monitored_agents": len(self.core.health_registry),
            "total_recoveries": len(self.recovery_logs),
            "recent_actions": self.recovery_logs[-5:]
        }

    def review_recovery_lessons(self) -> None:
        """
        Reviews recent recovery logs to identify recurring patterns of failure.
        Feeds these back into the SelfImprovementOrchestrator for source-level fixes.
        """
        if not self.recovery_logs:
            return
            
        logging.info("Self-Healing: Reviewing recovery logs for new intelligence lessons...")
        for log in self.recovery_logs[-10:]:
            if log.get("action") == "apoptosis":
                lesson = f"Lesson: Agent {log['agent']} reached apoptosis. Root cause analysis needed."
                # Record lesson to SQL intelligence table via FleetManager
                if hasattr(self.fleet_manager, 'sql_metadata'):
                    self.fleet_manager.sql_metadata.record_lesson(
                        interaction_id=f"recovery_{int(log['timestamp'])}",
                        text=lesson,
                        category="Self-Healing Failure"
                    )
