"""
Delegation management for agent cascading.
Enables agents to launch sub-tasks by spawning other specialized agents.
"""

from __future__ import annotations
import os
import sys
import logging
from pathlib import Path
from typing import Optional, Any

class AgentDelegator:
    """Handles cascading sub-tasks to other agents."""

    @staticmethod
    def delegate(agent_type: str, prompt: str, current_agent_name: str, current_file_path: Path, 
                 current_model: Optional[str] = None, target_file: Optional[str] = None) -> str:
        """Launches another agent to perform a sub-task."""
        if os.environ.get("DV_AGENT_PARENT"):
             # Already in a cascade, limit depth
             logging.warning(f"Delegation to {agent_type} blocked: depth limit.")
             return "Error: Delegation depth limit reached."

        logging.info(f"Delegating task to {agent_type} for {target_file or current_file_path}")
        
        target_path: Path = Path(target_file) if target_file else current_file_path
        
        try:
            type_clean: str = agent_type.replace("Agent", "").lower()
            
            # Simple heuristic for discovery
            if type_clean == "coder" or os.path.exists(os.path.join("src", "coder", "agents", f"{agent_type}.py")):
                module_name = f"src.logic.agents.development.{agent_type}"
            else:
                module_name = f"src.{type_clean}.{agent_type}"
            
            import importlib
            module = importlib.import_module(module_name)
            agent_class = getattr(module, agent_type)
            
            os.environ["DV_AGENT_PARENT"] = current_agent_name
            
            try:
                with agent_class(str(target_path)) as sub_agent:
                    if current_model:
                        sub_agent.set_model(current_model)
                    
                    result = sub_agent.improve_content(prompt)
                    sub_agent.update_file()
                    
                    logging.info(f"Delegation to {agent_type} completed.")
                    return result
            finally:
                if os.environ.get("DV_AGENT_PARENT") == current_agent_name:
                    del os.environ["DV_AGENT_PARENT"]
                
        except Exception as e:
            logging.error(f"Delegation to {agent_type} failed: {e}")
            return f"Error: Delegation failed - {str(e)}"
