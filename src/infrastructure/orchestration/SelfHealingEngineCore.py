from __future__ import annotations

import traceback
from typing import Dict, List, Any

class SelfHealingEngineCore:
    """
    Pure logic for self-healing analysis.
    Decides what kind of fix is needed based on the traceback.
    """
    
    def analyze_failure(self, agent_name: str, tool_name: str, error_msg: str, tb: str) -> Dict[str, Any]:
        """Analyzes a failure and suggests a strategy."""
        strategy = "manual_review"
        
        if "SyntaxError" in tb:
            strategy = "fix_syntax"
        elif "ImportError" in tb:
            strategy = "install_dependency"
        elif "KeyError" in tb:
            strategy = "check_config"
        elif "AttributeError" in tb:
            strategy = "verify_api_compatibility"
            
        return {
            "agent": agent_name,
            "tool": tool_name,
            "error": error_msg,
            "strategy": strategy,
            "is_critical": "Registry" in agent_name or "Fleet" in agent_name
        }

    def format_healing_report(self, history: List[Dict[str, Any]]) -> str:
        """Standardized reporting logic."""
        return f"Self-Healing Engine: {len(history)} failures detected and queued for repair."
