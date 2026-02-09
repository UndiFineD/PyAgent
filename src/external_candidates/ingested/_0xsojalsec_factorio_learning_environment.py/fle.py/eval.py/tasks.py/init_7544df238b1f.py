# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\fle\eval\tasks\__init__.py
"""
Task definitions and evaluation framework for the Factorio Learning Environment.

This module contains the task system used for evaluating agent performance in Factorio.
Tasks define objectives, success conditions, and provide standardized evaluation metrics.

The task system supports various types of challenges including:
- Throughput-based tasks (achieve specific production rates)
- Unbounded optimization tasks (maximize production)
- Custom task definitions loaded from JSON files

Example usage:
    from fle.eval.tasks import TaskFactory, ThroughputTask

    # Create task from JSON definition
    task = TaskFactory.create_task("iron_plate_throughput_16.json")

    # Or create task directly
    task = ThroughputTask(
        trajectory_length=100,
        goal_description="Build an iron plate factory",
        task_key="iron_plate_task",
        throughput_entity="iron-plate",
        quota=50,
        holdout_wait_period=60
    )
"""

from .default_task import DefaultTask

# Core task classes
from .task_abc import TaskABC

# Task creation utilities
from .task_factory import TaskFactory
from .throughput_task import LAB_PLAY_POPULATED_STARTING_INVENTORY, ThroughputTask
from .unbounded_throughput_task import UnboundedThroughputTask

__all__ = [
    # Abstract base and core classes
    "TaskABC",
    "DefaultTask",
    # Throughput-based tasks
    "ThroughputTask",
    "UnboundedThroughputTask",
    # Task creation utilities
    "TaskFactory",
    # Useful constants
    "LAB_PLAY_POPULATED_STARTING_INVENTORY",
]
