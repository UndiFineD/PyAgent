#!/usr/bin/env python3

"""An enhanced FleetManager that supports parallel execution of agent workflows."""

import logging
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Any, Optional, Type
from src.classes.fleet.FleetManager import FleetManager
from src.classes.base_agent import BaseAgent

class AsyncFleetManager(FleetManager):
    """Executes agent workflows in parallel using a thread pool."""
    
    def __init__(self, workspace_root: str, max_workers: int = 4) -> None:
        super().__init__(workspace_root)
        self.max_workers = max_workers

    def execute_workflow_async(self, task: str, workflow_steps: List[Dict[str, Any]]) -> str:
        """Runs multiple agent steps in parallel if they don't have inter-dependencies."""
        logging.info(f"Starting parallel workflow: {task} with {len(workflow_steps)} steps.")
        
        results = []
        workflow_id = f"async_wf_{int(logging.time.time())}"
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Map steps to future objects
            future_to_step = {
                executor.submit(self._run_single_step, step, workflow_id): step 
                for step in workflow_steps
            }
            
            for future in concurrent.futures.as_completed(future_to_step):
                step = future_to_step[future]
                agent_name = step.get("agent")
                action_name = step.get("action")
                
                try:
                    res = future.result()
                    results.append(f"### Results from {agent_name} ({action_name})\n{res}\n")
                except Exception as e:
                    logging.error(f"Async failed for {agent_name}: {e}")
                    results.append(f"### Error from {agent_name}\n{str(e)}\n")
                    
        return f"# Parallel Workflow Summary: {task}\n\n" + "\n".join(results)

    def _run_single_step(self, step: Dict[str, Any], workflow_id: str) -> str:
        """Internal helper to execute a single agent step within a thread."""
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
            res = action_fn(*args)
            self.telemetry.end_trace(trace_id, agent_name, action_name, status="success")
            return res
        except Exception as e:
            self.telemetry.end_trace(trace_id, agent_name, action_name, status="error", metadata={"error": str(e)})
            raise e

if __name__ == "__main__":
    # Test script
    from src.classes.context.KnowledgeAgent import KnowledgeAgent
    from src.classes.coder.SecurityGuardAgent import SecurityGuardAgent
    
    root = "c:/DEV/PyAgent"
    afleet = AsyncFleetManager(root)
    afleet.register_agent("K1", KnowledgeAgent, root + "/src/classes/context/KnowledgeAgent.py")
    afleet.register_agent("S1", SecurityGuardAgent, root + "/src/classes/coder/SecurityGuardAgent.py")
    
    wf = [
        {"agent": "K1", "action": "scan_workspace", "args": ["agent"]},
        {"agent": "S1", "action": "improve_content", "args": ["rm -rf /"]}
    ]
    
    report = afleet.execute_workflow_async("Parallel Test", wf)
    print(report)
