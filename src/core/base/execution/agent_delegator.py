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
import logging
from pathlib import Path

from src.core.base.lifecycle.version import VERSION
from src.core.base.registry.module_loader import ModuleLoader
from src.core.base.common.models import CascadeContext, AgentPriority

__version__ = VERSION


# pylint: disable=too-few-public-methods
class AgentDelegator:
    """Handles cascading sub-tasks to other agents."""

    @staticmethod
    def delegate(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        agent_type: str,
        prompt: str,
        current_agent_name: str,
        current_file_path: Path,
        current_model: str | None = None,
        target_file: str | None = None,
        context: CascadeContext | None = None,
        priority: AgentPriority = AgentPriority.NORMAL,
    ) -> str:
        """Launches another agent to perform a sub-task."""
        _ = current_agent_name

        # Initialize or update context
        if context is None:
            context = CascadeContext()
        else:
            context.cascade_depth += 1
            context.parent_id = context.task_id

        if context.cascade_depth > 5:
            logging.warning(
                "Delegation to %s blocked: depth limit (%s).",
                agent_type, context.cascade_depth
            )
            return "Error: Delegation depth limit reached."

        logging.info(
            "Delegating task to %s [Priority: %s] for %s",
            agent_type, priority.name, target_file or current_file_path
        )

        target_path: Path = Path(target_file) if target_file else current_file_path

        try:
            # Discovery delegated to centralized ModuleLoader
            agent_class = ModuleLoader.load_agent_class(agent_type)

            with agent_class(str(target_path)) as sub_agent:
                if current_model:
                    sub_agent.set_model(current_model)

                # Store context and priority in agent if supported
                if hasattr(sub_agent, "context"):
                    sub_agent.context = context
                if hasattr(sub_agent, "priority"):
                    sub_agent.priority = priority

                result = sub_agent.improve_content(prompt)
                sub_agent.update_file()

                logging.info(
                    "Delegation to %s completed (Task: %s).",
                    agent_type, context.task_id
                )
                return result

        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("Delegation to %s failed: %s", agent_type, e)
            return f"Error: Delegation failed - {str(e)}"
