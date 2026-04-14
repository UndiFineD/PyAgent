"""Cron Scheduler for Phase 8.2 Reasoning Tasks

Schedule reasoning tasks to run periodically.

Examples:
  reasoning_cron_job("Daily market analysis", "0 9 * * *", "/reason hybrid Analyze market trends")
  reasoning_cron_job("Weekly planning", "0 10 * * 1", "/plan Week planning")
  reasoning_cron_job("Hourly monitoring", "0 * * * *", "/reason math Check KPI calculations")

"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Callable, Dict, Optional

from hermes_integration import CronScheduledReasoning, HermesReasoningEngine, ReasoningCommandType


@dataclass
class ReasoningCronTask:
    """A reasoning task scheduled with cron"""

    task_id: str
    name: str
    command: str  # /reason, /math, /debate, etc.
    args: str    # Arguments to command
    schedule: str  # Cron format: "0 9 * * *"
    user_id: str
    created_at: str
    enabled: bool = True
    last_run: Optional[str] = None
    last_result: Optional[str] = None
    next_run: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)


class ReasoningCronScheduler:
    """Manage cron-scheduled reasoning tasks"""

    def __init__(self):
        """Initialize cron scheduler"""
        self.tasks: Dict[str, ReasoningCronTask] = {}
        self.reasoning_engine = HermesReasoningEngine()
        self.cron_manager = CronScheduledReasoning(self.reasoning_engine)

    def schedule_task(
        self,
        name: str,
        command: str,
        args: str,
        schedule: str,
        user_id: str
    ) -> str:
        """Schedule a reasoning task.
        
        Args:
            name: Task name (e.g., "Daily math checks")
            command: Command type (math, debate, plan, etc.)
            args: Command arguments
            schedule: Cron schedule (e.g., "0 9 * * *" for 9 AM daily)
            user_id: User ID
        
        Returns:
            Task ID
        
        Example:
            scheduler.schedule_task(
                name="Daily market analysis",
                command="hybrid",
                args="Analyze stock market trends today",
                schedule="0 9 * * *",  # Every day at 9 AM
                user_id="user123"
            )

        """
        import uuid
        task_id = f"reasoning_cron_{uuid.uuid4().hex[:8]}"

        # Map command to reasoning type
        command_map = {
            'math': ReasoningCommandType.SYMBOLIC_MATH,
            'debate': ReasoningCommandType.MULTI_AGENT_DEBATE,
            'plan': ReasoningCommandType.HIERARCHICAL_PLAN,
            'hybrid': ReasoningCommandType.HYBRID_REASON,
            'pattern': ReasoningCommandType.REASONING_PATTERN,
        }

        reasoning_command = command_map.get(command.lower())
        if not reasoning_command:
            raise ValueError(f"Unknown command: {command}")

        # Create task
        task = ReasoningCronTask(
            task_id=task_id,
            name=name,
            command=command,
            args=args,
            schedule=schedule,
            user_id=user_id,
            created_at=datetime.now().isoformat(),
            enabled=True
        )

        self.tasks[task_id] = task

        # Register with cron manager
        # Note: In production, this would integrate with actual cron scheduler
        # For now, we store the task definition

        return task_id

    def list_tasks(self, user_id: str) -> list:
        """List all tasks for a user"""
        return [
            task for task in self.tasks.values()
            if task.user_id == user_id
        ]

    def get_task(self, task_id: str) -> Optional[ReasoningCronTask]:
        """Get a specific task"""
        return self.tasks.get(task_id)

    def enable_task(self, task_id: str) -> bool:
        """Enable a task"""
        task = self.tasks.get(task_id)
        if task:
            task.enabled = True
            return True
        return False

    def disable_task(self, task_id: str) -> bool:
        """Disable a task"""
        task = self.tasks.get(task_id)
        if task:
            task.enabled = False
            return True
        return False

    def cancel_task(self, task_id: str) -> bool:
        """Cancel (delete) a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def update_task(
        self,
        task_id: str,
        **kwargs
    ) -> Optional[ReasoningCronTask]:
        """Update task fields"""
        task = self.tasks.get(task_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        return task

    async def execute_task(self, task_id: str) -> Optional[str]:
        """Execute a scheduled task immediately.
        
        Returns:
            Result summary

        """
        task = self.tasks.get(task_id)
        if not task:
            return None

        if not task.enabled:
            return f"Task {task_id} is disabled"

        try:
            # Map command to reasoning type
            command_map = {
                'math': ReasoningCommandType.SYMBOLIC_MATH,
                'debate': ReasoningCommandType.MULTI_AGENT_DEBATE,
                'plan': ReasoningCommandType.HIERARCHICAL_PLAN,
                'hybrid': ReasoningCommandType.HYBRID_REASON,
                'pattern': ReasoningCommandType.REASONING_PATTERN,
            }

            reasoning_command = command_map[task.command.lower()]

            # Execute
            session = await self.reasoning_engine.process_reasoning_command(
                user_id=task.user_id,
                command=reasoning_command,
                query=task.args
            )

            # Update task
            task.last_run = datetime.now().isoformat()
            task.last_result = session.explanation[:200]  # Summary

            return f"Task '{task.name}' executed: {session.explanation[:100]}"

        except Exception as e:
            task.last_result = f"Error: {str(e)}"
            return f"Task failed: {str(e)}"


# Example cron job definitions
EXAMPLE_CRON_JOBS = [
    {
        'name': 'Daily Market Analysis',
        'command': 'hybrid',
        'args': 'What are today\'s market trends?',
        'schedule': '0 9 * * *',  # 9 AM daily
        'description': 'Analyze market trends each morning'
    },
    {
        'name': 'Weekly Planning',
        'command': 'plan',
        'args': 'Plan activities for next week',
        'schedule': '0 10 * * 1',  # 10 AM Monday
        'description': 'Auto-plan the week ahead'
    },
    {
        'name': 'Hourly Monitoring',
        'command': 'math',
        'args': 'Calculate moving average of last hour metrics',
        'schedule': '0 * * * *',  # Every hour
        'description': 'Monitor hourly KPIs'
    },
    {
        'name': 'Daily Debate - Tomorrow\'s Topic',
        'command': 'debate',
        'args': 'Will AI agents become more autonomous?',
        'schedule': '0 20 * * *',  # 8 PM daily
        'description': 'Daily perspective on trending topics'
    },
]


def setup_reasoning_cron_jobs(scheduler: ReasoningCronScheduler, user_id: str) -> list:
    """Setup example cron jobs for a user.
    
    Returns:
        List of created task IDs

    """
    task_ids = []

    for job in EXAMPLE_CRON_JOBS:
        try:
            task_id = scheduler.schedule_task(
                name=job['name'],
                command=job['command'],
                args=job['args'],
                schedule=job['schedule'],
                user_id=user_id
            )
            task_ids.append(task_id)
        except Exception as e:
            print(f"Failed to create job {job['name']}: {e}")

    return task_ids


# Integration with Hermes cron system
def register_reasoning_cron_jobs(cron_registry) -> None:
    """Register reasoning cron job templates with Hermes.
    
    Called during Hermes initialization.
    """
    scheduler = ReasoningCronScheduler()

    for job in EXAMPLE_CRON_JOBS:
        # Register job template with cron registry
        # This would integrate with Hermes' actual cron system
        pass


# Hermes CLI command for managing reasoning cron jobs
REASONING_CRON_COMMANDS = {
    'reasoning_cron_list': {
        'description': 'List scheduled reasoning tasks',
        'usage': '/reasoning_cron list [user_id]'
    },
    'reasoning_cron_add': {
        'description': 'Schedule a new reasoning task',
        'usage': '/reasoning_cron add <name> <command> <schedule> <args>'
    },
    'reasoning_cron_run': {
        'description': 'Run a scheduled reasoning task now',
        'usage': '/reasoning_cron run <task_id>'
    },
    'reasoning_cron_enable': {
        'description': 'Enable a disabled task',
        'usage': '/reasoning_cron enable <task_id>'
    },
    'reasoning_cron_disable': {
        'description': 'Disable a task',
        'usage': '/reasoning_cron disable <task_id>'
    },
    'reasoning_cron_cancel': {
        'description': 'Delete a task',
        'usage': '/reasoning_cron cancel <task_id>'
    },
}
