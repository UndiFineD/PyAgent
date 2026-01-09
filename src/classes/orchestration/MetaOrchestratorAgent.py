#!/usr/bin/env python3

"""High-level goal manager and recursive orchestrator.
Manages complex objectives by breaking them down into sub-goals and delegating to specialized agents.
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.fleet.FleetManager import FleetManager
from src.classes.orchestration.ToolRegistry import ToolRegistry
from src.classes.context.GlobalContextEngine import GlobalContextEngine

class MetaOrchestratorAgent(BaseAgent):
    """The 'Brain' of the Agent OS. Manages goals, resources, and fleet coordination."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.fleet = FleetManager(str(self.workspace_root))
        self.registry = ToolRegistry()
        self.global_context = GlobalContextEngine(str(self.workspace_root))
        
        self._system_prompt = (
            "You are the Meta-Orchestrator Agent. "
            "Your goal is to manage the entire lifecycle of a project request. "
            "1. Decompose high-level goals into atomic tasks. "
            "2. Assign tasks to agents based on their registered capabilities. "
            "3. Monitor progress and resolve conflicts or failures. "
            "4. Maintain a consistent project context via Long-Term Memory."
        )

    def _get_default_content(self) -> str:
        return "# Meta-Orchestration Log\n\n## Current Goal\nNone.\n"

    def execute_by_goal(self, goal: str) -> str:
        """Determines which tool to use for a specific goal and executes it."""
        tools = self.registry.list_tools()
        # In a real scenario, we'd use semantic search / LLM to match goal to tool
        # For now, simple keyword matching for demo
        for tool_meta in tools:
            if tool_meta.name.lower() in goal.lower() or any(k in goal.lower() for k in tool_meta.description.lower().split()):
                logging.info(f"Orchestrator matched goal '{goal}' to tool '{tool_meta.name}'")
                return self.registry.call_tool(tool_meta.name, query=goal)
        
        return f"No direct tool found for goal: {goal}. Falling back to standard objective solver."

    def solve_complex_objective(self, objective: str, depth: int = 0) -> str:
        """Solves a large objective by orchestrating multiple agent workflows with recursion support."""
        if depth > 3:
            return "Recursion limit reached for objective decomposition."
            
        logging.info(f"Orchestrator tackling objective (Depth {depth}): {objective}")
        
        # Intelligence Harvesting (Phase 108)
        self.recorder.record_lesson("meta_planning_init", {"objective": objective, "depth": depth})
        
        # 1. Update Global Context with the new objective
        self.global_context.add_insight(f"Objective depth {depth}: {objective}", "MetaOrchestrator")
        
        # 2. Planning Phase
        planner = self.fleet.agents.get("Planner")
        if not planner:
            return "Error: TaskPlannerAgent not registered in fleet."
            
        plan_report = planner.improve_content(objective)
        
        # Handle recursive sub-objectives if found in plan
        try:
            plan_json_start = plan_report.find("```json") + 7
            plan_json_end = plan_report.rfind("```")
            plan_data = json.loads(plan_report[plan_json_start:plan_json_end].strip())
            
            # Record successful planning logic
            self.recorder.record_lesson("meta_plan_received", {"plan": plan_data, "objective": objective})
        except Exception as e:
            self.recorder.record_lesson("meta_plan_parsing_error", {"error": str(e), "report_preview": plan_report[:500]})
            return f"Error: Failed to parse plan from TaskPlanner: {e}"
            
        # 3. Execution Phase
        results = []
        for step in plan_data:
            if step.get("type") == "complex_goal":
                # RECURSIVE CALL
                logging.info(f"Decomposing complex sub-goal: {step.get('goal')}")
                res = self.solve_complex_objective(step.get("goal"), depth + 1)
                results.append(res)
                continue

            agent_name = step.get("agent")
            action = step.get("action")
            args = step.get("args", [])
            
            # Execute via FleetManager
            res = self.fleet.execute_workflow(objective, [{"agent": agent_name, "action": action, "args": args}])
            results.append(res)
            
        return f"# Objective Resolution Report (Depth {depth})\n\n" + "\n".join(results)

    def _enrich_args(self, args: List[Any]) -> List[Any]:
        """Injects global context into agent arguments."""
        enriched = []
        context_brief = self.global_context.get_summary()
        
        for arg in args:
            if isinstance(arg, str):
                # If arg is a string, we might append context if it seems broadly descriptive
                if len(arg) > 50: 
                    arg += f"\n\n[GLOBAL CONTEXT]\n{context_brief}"
            enriched.append(arg)
        return enriched

    def recursive_solve(self, objective: str, depth: int = 0) -> str:
        """Recursively solves an objective by breaking it down further if needed."""
        if depth > 3: # Prevention of infinite loops
            return "Error: Maximum recursion depth reached for task decomposition."
            
        logging.info(f"Recursive check for: {objective} (Depth: {depth})")
        
        # Simple heuristic: if objective contains "and", "then", or is very long, decompose it.
        if " and " in objective or " then " in objective or len(objective) > 100:
            logging.info("Objective identified as complex. Spawning sub-planner.")
            return self.solve_complex_objective(objective)
        else:
            return self.execute_by_goal(objective)

    def improve_content(self, prompt: str) -> str:
        """Entry point for fulfilling complex user requests."""
        return self.recursive_solve(prompt)
