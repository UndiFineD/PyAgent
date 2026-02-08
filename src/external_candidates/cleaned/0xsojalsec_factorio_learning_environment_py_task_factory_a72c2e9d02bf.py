# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\fle.py\eval.py\tasks.py\task_factory_a72c2e9d02bf.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\eval\tasks\task_factory.py

from fle.eval.tasks import TaskABC


class TaskFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_task(task_path) -> TaskABC:
        """Create a task from a Python-based definition.

        Args:

            task_path: Task key (e.g., "iron_plate_throughput")

        Returns:

            TaskABC instance

        """

        from fle.eval.tasks.task_definitions.task_registry import create_task

        return create_task(task_path)
