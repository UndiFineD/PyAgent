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
Delegation management for agent cascading.
Enables agents to launch sub-tasks by spawning other specialized agents.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import os
import logging
from pathlib import Path
from typing import Optional, Any
from src.core.base.registry import AgentRegistry
from src.core.base.models import CascadeContext, AgentPriority

__version__ = VERSION

class AgentDelegator:
    """Handles cascading sub-tasks to other agents."""

    @staticmethod
    def delegate(agent_type: str, 
                 prompt: str, 
                 current_agent_name: str, 
                 current_file_path: Path, 
                 current_model: str | None = None, 
                 target_file: str | None = None,
                 context: CascadeContext | None = None,
                 priority: AgentPriority = AgentPriority.NORMAL) -> str:
        """Launches another agent to perform a sub-task."""
        
        # Initialize or update context
        if context is None:
            context = CascadeContext()
        else:
            context.cascade_depth += 1
            context.parent_id = context.task_id
            
        # Check registry for existing instance of this type to avoid redundant spawns
        registry = AgentRegistry()
        type_clean = agent_type.replace("Agent", "").lower()
        
        if context.cascade_depth > 5:
             logging.warning(f"Delegation to {agent_type} blocked: depth limit ({context.cascade_depth}).")
             return "Error: Delegation depth limit reached."

        logging.info(f"Delegating task to {agent_type} [Priority: {priority.name}] for {target_file or current_file_path}")
        
        target_path: Path = Path(target_file) if target_file else current_file_path
        
        try:
            # Simple heuristic for discovery
            # TODO: Move to centralized ModuleLoader
            if type_clean == "coder" or os.path.exists(os.path.join("src", "coder", "agents", f"{agent_type}.py")):
                module_name = f"src.logic.agents.development.{agent_type}"
            else:
                module_name = f"src.{type_clean}.{agent_type}"
            
            import importlib
            module = importlib.import_module(module_name)
            agent_class = getattr(module, agent_type)
            
            try:
                with agent_class(str(target_path)) as sub_agent:
                    if current_model:
                        sub_agent.set_model(current_model)
                    
                    # Store context and priority in agent if supported
                    if hasattr(sub_agent, 'context'):
                        sub_agent.context = context
                    if hasattr(sub_agent, 'priority'):
                        sub_agent.priority = priority
                    
                    result = sub_agent.improve_content(prompt)
                    sub_agent.update_file()
                    
                    logging.info(f"Delegation to {agent_type} completed (Task: {context.task_id}).")
                    return result
            finally:
                pass
                
        except Exception as e:
            logging.error(f"Delegation to {agent_type} failed: {e}")
            return f"Error: Delegation failed - {str(e)}"
                
        except Exception as e:
            logging.error(f"Delegation to {agent_type} failed: {e}")
            return f"Error: Delegation failed - {str(e)}"