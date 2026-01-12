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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""
Delegation management for agent cascading.
Enables agents to launch sub-tasks by spawning other specialized agents.
"""



import os
import sys
import logging
from pathlib import Path
from typing import Optional, Any

from src.core.base.registry import AgentRegistry

class AgentDelegator:
    """Handles cascading sub-tasks to other agents."""

    @staticmethod
    def delegate(agent_type: str, prompt: str, current_agent_name: str, current_file_path: Path, 
                 current_model: Optional[str] = None, target_file: Optional[str] = None) -> str:
        """Launches another agent to perform a sub-task."""
        
        # Check registry for existing instance of this type to avoid redundant spawns
        registry = AgentRegistry()
        type_clean = agent_type.replace("Agent", "").lower()
        
        active_agents = registry.list_agents()
        if type_clean in active_agents:
            logging.info(f"Reusing active agent: {type_clean}")
            # In a real system we might pass the task to the existing instance
            # For now, we continue with spawning but acknowledge it.

        if os.environ.get("DV_AGENT_PARENT"):
             # Already in a cascade, limit depth
             logging.warning(f"Delegation to {agent_type} blocked: depth limit.")
             return "Error: Delegation depth limit reached."

        logging.info(f"Delegating task to {agent_type} for {target_file or current_file_path}")
        
        target_path: Path = Path(target_file) if target_file else current_file_path
        
        try:
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
