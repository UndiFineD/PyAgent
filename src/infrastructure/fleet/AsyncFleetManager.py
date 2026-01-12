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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""An enhanced FleetManager that supports parallel execution of agent workflows."""




import logging
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Type

from .FleetManager import FleetManager

class AsyncFleetManager(FleetManager):
    """Executes agent workflows in parallel using native asyncio."""
    
    def __init__(self, workspace_root: str, max_workers: int = 4) -> None:
        super().__init__(workspace_root)
        self.max_workers = max_workers

    async def execute_workflow_async(self, task: str, workflow_steps: List[Dict[str, Any]]) -> str:
        """Runs multiple agent steps in parallel using native asyncio orchestration."""
        logging.info(f"Starting parallel workflow: {task} with {len(workflow_steps)} steps.")
        
        workflow_id = f"async_wf_{int(time.time())}"
        
        # Schedule all steps as concurrent coroutines
        tasks = [
            self._run_single_step(step, workflow_id) 
            for step in workflow_steps
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        results = []
        for i, res in enumerate(responses):
            step = workflow_steps[i]
            agent_name = step.get("agent")
            action_name = step.get("action")
            
            if isinstance(res, Exception):
                logging.error(f"Async failed for {agent_name}: {res}")
                results.append(f"### Error from {agent_name}\n{str(res)}\n")
            else:
                results.append(f"### Results from {agent_name} ({action_name})\n{res}\n")
                    
        return f"# Parallel Workflow Summary: {task}\n\n" + "\n".join(results)

    async def _run_single_step(self, step: Dict[str, Any], workflow_id: str) -> str:
        """Internal helper to execute a single agent step within the asyncio event loop."""
        agent_name = step.get("agent")
        action_name = step.get("action")
        args = step.get("args", [])
        
        if agent_name not in self.agents:
            return f"Error: Agent '{agent_name}' not found."
            
        agent = self.agents[agent_name]
        if not hasattr(agent, action_name):
            return f"Error: Action '{action_name}' not supported."
            
        action_fn = getattr(agent, action_name)
        trace_id = f"{workflow_id}_{agent_name}_{action_name}"
        self.telemetry.start_trace(trace_id)
        
        try:
            # Phase 152: Intelligent execution based on function type
            if asyncio.iscoroutinefunction(action_fn):
                res = await action_fn(*args)
            else:
                # Offload blocking synchronous actions to the default executor
                loop = asyncio.get_running_loop()
                res = await loop.run_in_executor(None, action_fn, *args)
                
            self.telemetry.end_trace(trace_id, agent_name, action_name, status="success")
            return res
        except Exception as e:
            self.telemetry.end_trace(trace_id, agent_name, action_name, status="error", metadata={"error": str(e)})
            raise e

if __name__ == "__main__":
    # Test script
    import asyncio
    from src.logic.agents.cognitive.KnowledgeAgent import KnowledgeAgent
    from src.logic.agents.security.SecurityGuardAgent import SecurityGuardAgent
    
    root = "."
    afleet = AsyncFleetManager(root)
    afleet.register_agent("K1", KnowledgeAgent)
    afleet.register_agent("S1", SecurityGuardAgent)
    
    wf = [
        {"agent": "K1", "action": "improve_content", "args": ["agent"]},
        {"agent": "S1", "action": "improve_content", "args": ["clean code"]}
    ]
    
    async def run_test():
        report = await afleet.execute_workflow_async("Parallel Test", wf)
        print(report)

    asyncio.run(run_test())
