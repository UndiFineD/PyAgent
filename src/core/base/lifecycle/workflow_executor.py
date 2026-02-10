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
Module: workflow_executor
Implements Pillar 4: Industrial Factory Integration (DAG-based Workflows).
"""

from __future__ import annotations
import asyncio
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    """
    Executes complex multi-agent workflows defined in LogicManifest snippets.
    Allows branching nodes and conditional execution logic (Pillar 4).
    """

    def __init__(self, agent_instance: Any):
        self.agent = agent_instance
        self.results: Dict[str, Any] = {}

    async def execute(self, flow_nodes: List[Dict[str, Any]], connectors: List[Dict[str, Any]]) -> Any:
        """Executes the workflow graph (Synchronous top-sort for now)."""
        logger.info("WorkflowExecutor: Executing DAG with %d nodes", len(flow_nodes))
        
        # Simple execution loop
        for node in flow_nodes:
            node_id = node.get("id")
            if not node_id:
                logger.warning("WorkflowExecutor: Skipping node without ID")
                continue
            
            node_type = node.get("type", "task")
            prompt_template = node.get("prompt", "")
            
            # Resolve dependencies (Variables from previous nodes)
            prompt = self._resolve_variables(prompt_template)
            
            logger.info("WorkflowExecutor: Executing node [%s] type [%s]", node_id, node_type)
            
            if node_type == "task":
                result = await self.agent.run_task({"context": prompt})
                self.results[node_id] = result
            elif node_type == "condition":
                # Basic branch logic
                condition = str(node.get("logic", "True"))
                self.results[node_id] = eval(condition, {"results": self.results})
                
        # Final node result
        if flow_nodes:
            return self.results.get(flow_nodes[-1]["id"], "Workflow complete")
        return "Empty workflow"

    def _resolve_variables(self, template: str) -> str:
        """Hydrates {{node_id}} placeholders with results."""
        import re
        def replace_match(match):
            key = match.group(1)
            return str(self.results.get(key, f"{{MISSING:{key}}}"))
        
        return re.sub(r"\{\{(.*?)\}\}", replace_match, template)

