#!/usr/bin/env python3

"""Agent specializing in proactive task management and recurring workflows (Sentient pattern)."""

from src.classes.base_agent import BaseAgent
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

    def scan_for_triggers(self, environment_state: Dict[str, Any]) -> List[str]:
        """Checks if any environmental triggers should fire a proactive task."""
        triggered_tasks = []
        # Example triggers
        if environment_state.get("disk_usage", 0) > 90:
            triggered_tasks.append("Cleanup workspace: Disk usage high")
        if environment_state.get("error_count", 0) > 5:
            triggered_tasks.append("Diagnostic: High error rate detected")
            
        return triggered_tasks

    def get_habit_recommendation(self, user_history: List[str]) -> str:
        """Learns habits from user history and suggests optimizations."""
        if len(user_history) > 10:
            return "Observation: You frequently run tests after editing 'fleet' files. Should I automate this?"
        return "Not enough data yet to establish habits."

    def improve_content(self, input_text: str) -> str:
        """Returns proactive suggestions based on current context."""
        return self.get_habit_recommendation([]) # Placeholder

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(ProactiveAgent)
    main()
