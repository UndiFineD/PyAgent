#!/usr/bin/env python3

"""Engine for automated self-repair of agent tools and modules.
Detects runtime errors and orchestrates CoderAgents to apply fixes.
"""

from __future__ import annotations

import logging
import traceback
from typing import Dict, List, Any, Optional, Type
from src.core.base.BaseAgent import BaseAgent

from .SelfHealingEngineCore import SelfHealingEngineCore

class SelfHealingEngine:
    """
    Monitors tool execution and attempts automatic fixes for crashes.
    Shell for SelfHealingEngineCore.
    """
    
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = workspace_root
        self.failure_history: List[Dict[str, Any]] = []
        self.core = SelfHealingEngineCore()

    def handle_failure(self, agent: BaseAgent, tool_name: str, error: Exception, context: Dict[str, Any]) -> str:
        """Analyzes a failure and attempts to generate a fix."""
        tb = traceback.format_exc()
        agent_name = agent.__class__.__name__
        logging.error(f"SELF-HEAL: Failure in {agent_name}.{tool_name}: {error}\n{tb}")
        
        analysis = self.core.analyze_failure(agent_name, tool_name, str(error), tb)
        analysis["context"] = context
        self.failure_history.append(analysis)
        
        # Fixed logic: communicate strategy
        return f"Self-Healing initiated: Strategy '{analysis['strategy']}' assigned to {tool_name}."

    def get_healing_stats(self) -> str:
        """Returns a summary of healing attempts."""
        return self.core.format_healing_report(self.failure_history)
