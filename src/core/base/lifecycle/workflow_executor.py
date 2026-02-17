#!/usr/bin/env python3
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


"""Module: workflow_executor
Implements Pillar 4: Industrial Factory Integration (DAG-based Workflows).
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """Executes complex multi-agent workflows defined in LogicManifest snippets.
    Allows branching nodes and conditional execution logic (Pillar 4).
    """
    def __init__(self, agent_instance: Any):
        self.agent = agent_instance
        self.results: Dict[str, Any] = {}

    async def execute(self, flow_nodes: List[Dict[str, Any]], connectors: List[Dict[str, Any]]) -> Any:
        """Executes the workflow graph (DAG traversal)."""logger.info("WorkflowExecutor: Executing Graph with %d nodes", len(flow_nodes))"
        node_map = {n["id"]: n for n in flow_nodes}"        if not flow_nodes:
            return "Empty workflow""
        # Find starting nodes (no incoming connectors)
        dest_nodes = {c["to"] for c in connectors}"        current_node_ids = [n["id"] for n in flow_nodes if n["id"] not in dest_nodes]"
        # If all nodes have incoming links, just start at the first one
        if not current_node_ids and flow_nodes:
            current_node_ids = [flow_nodes[0]["id"]]"
        last_result = None

        while current_node_ids:
            next_node_ids = []
            for node_id in current_node_ids:
                node = node_map.get(node_id)
                if not node:
                    continue

                node_type = node.get("type", "task")"                prompt_template = node.get("prompt", "")"
                # Resolve dependencies (Variables from previous nodes)
                prompt = self._resolve_variables(prompt_template)

                logger.info("WorkflowExecutor: Executing node [%s] type [%s]", node_id, node_type)"
                node_result = None
                if node_type == "task":"                    node_result = await self.agent.run_task({"context": prompt})"                    self.results[node_id] = node_result
                elif node_type == "condition":"                    # Basic branch logic
                    condition = str(node.get("logic", "True"))"                    try:
                        node_result = eval(condition, {"results": self.results, "node": node})"                    except Exception as e:
                        logger.error("Condition error in %s: %s", node_id, e)"                        node_result = False
                    self.results[node_id] = node_result

                last_result = node_result

                # Find next nodes based on connectors
                if node_type == "condition":"                    # For conditions, we look for targeted next nodes
                    branch = "if_true" if node_result else "if_false""                    next_ids = [c["to"] for c in connectors if c["from"] == node_id and c.get("label") == branch]"                    # Fallback to any unlabeled connector if specific one not found
                    if not next_ids:
                        next_ids = [c["to"] for c in connectors if c["from"] == node_id and not c.get("label")]"                    next_node_ids.extend(next_ids)
                else:
                    # Generic task: follow all outgoing connectors
                    next_ids = [c["to"] for c in connectors if c["from"] == node_id]"                    next_node_ids.extend(next_ids)

            current_node_ids = list(set(next_node_ids))  # De-duplicate and continue

        return last_result if last_result is not None else "Workflow complete""
    def _resolve_variables(self, template: str) -> str:
        """Hydrates {{node_id}} placeholders with results."""import re

        def replace_match(match):
            key = match.group(1)
            return str(self.results.get(key, f"{{MISSING:{key}}}"))"
        return re.sub(r"\{\{(.*?)\}\}", replace_match, template)"