#!/usr/bin/env python3

"""Agent specializing in proactive task management and recurring workflows (Sentient pattern)."""

from src.core.base.BaseAgent import BaseAgent
import logging
import json
import time
from typing import Dict, List, Any, Optional

class ProactiveAgent(BaseAgent):
    """Manages recurring, triggered, and scheduled tasks proactively."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Proactive Agent. "
            "Your role is to monitor the environment and execute tasks based on triggers, "
            "schedules, or detected patterns. You don't just wait for prompts; you anticipate needs."
        )
        self.scheduled_tasks: List[Dict[str, Any]] = []

    def observe_environment(self) -> Dict[str, Any]:
        """
        Observes the local system environment for triggers.
        Hooked into ResourceMonitor (Phase 125).
        """
        try:
            from src.observability.stats.ResourceMonitor import ResourceMonitor
            monitor = ResourceMonitor(self._workspace_root)
            return monitor.get_current_stats()
        except (ImportError, AttributeError):
            return {"status": "UNAVAILABLE", "cpu_usage_pct": 0, "disk_free_gb": 100}

    def schedule_task(self, task: str, cron_or_delay: str) -> str:
        """Schedules a task for future execution."""
        task_entry = {
            "id": f"task_{int(time.time())}",
            "task": task,
            "trigger": cron_or_delay,
            "status": "scheduled"
        }
        self.scheduled_tasks.append(task_entry)
        logging.info(f"ProactiveAgent: Scheduled task '{task}' with trigger '{cron_or_delay}'")
        return json.dumps(task_entry)

    def scan_for_triggers(self, environment_state: Optional[Dict[str, Any]] = None) -> List[str]:
        """Checks if any environmental triggers should fire a proactive task."""
        state = environment_state or self.observe_environment()
        triggered_tasks = []
        
        # CPU/Memory Triggers
        if state.get("status") == "CRITICAL":
            triggered_tasks.append(f"Resource Alert: System status is {state['status']}. Optimizing processes.")
            
        # Disk Triggers
        if state.get("disk_free_gb", 100) < 5:
            triggered_tasks.append("Cleanup workspace: Disk space is critically low (less than 5GB free)")
            
        # Original placeholders
        if state.get("error_count", 0) > 5:
            triggered_tasks.append("Diagnostic: High error rate detected")
            
        return triggered_tasks

    def get_habit_recommendation(self, user_history: List[str]) -> str:
        """Uses LLM to detect user behavior patterns and recommend proactive habits."""
        if not user_history:
            return "Not enough data yet to establish habits."
            
        logging.info(f"ProactiveAgent: Analyzing history of {len(user_history)} interactions.")
        prompt = (
            f"Analyze the following user interaction history: {json.dumps(user_history)}\n"
            "Identify recurring patterns (e.g., 'always runs tests after editing models') "
            "and suggest one proactive automation or habit that would save time. "
            "Be concise and helpful."
        )
        
        return self.think(prompt)

    def improve_content(self, input_text: str) -> str:
        """Returns proactive suggestions based on current context."""
        return self.get_habit_recommendation([input_text])

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(ProactiveAgent)
    main()
