#!/usr/bin/env python3
from __future__ import annotations

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
"""
Lightweight WorkflowExecutor for test collection.

"""
This simplified executor provides a minimal implementation that
supports basic task execution and variable substitution for tests.
"""
import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    def __init__(self, agent_instance: Any):
        self.agent = agent_instance
        self.results: Dict[str, Any] = {}

        async def execute(self, flow_nodes: List[Dict[str, Any]], connectors: List[Dict[str, Any]]) -> Any:
        if not flow_nodes:
        return "Empty workflow"

        # Execute nodes sequentially for simplicity
        for node in flow_nodes:
        node_id = node.get("id")
        node_type = node.get("type", "task")
        prompt = self._resolve_variables(node.get("prompt", ""))

        logger.info("WorkflowExecutor: Executing node %s of type %s", node_id, node_type)
        if node_type == "task":
        # Delegate to agent if available
        if hasattr(self.agent, "run_task"):
        result = await self.agent.run_task({"context": prompt})
        else:
        result = None
        self.results[node_id] = result
        elif node_type == "condition":
        try:
        cond = str(node.get("logic", "True"))
        res = bool(eval(cond, {"results": self.results, "node": node}))
        except Exception:
        res = False
        self.results[node_id] = res

        return self.results

    def _resolve_variables(self, template: str) -> str:
        def replace_match(match: re.Match) -> str:
            key = match.group(1)
            return str(self.results.get(key, f"{{MISSING:{key}}}"))

        return re.sub(r"\{\{(.*?)\}\}", replace_match, template)