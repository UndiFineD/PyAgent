#!/usr/bin/env python3

"""Engine for dynamic task decomposition.
Breaks complex user requests into granular sub-tasks for the agent fleet.
"""

from __future__ import annotations

import logging
import json
from typing import List, Dict, Any

from .TaskDecomposerCore import TaskDecomposerCore

class TaskDecomposer:
    """
    Analyzes high-level requests and generates a multi-step plan.
    Shell for TaskDecomposerCore.
    """

    def __init__(self, fleet_manager: Any) -> None:
        self.fleet = fleet_manager
        self.core = TaskDecomposerCore()

    def decompose(self, request: str) -> List[Dict[str, Any]]:
        """Splits a request into a sequence of agent steps."""
        logging.info(f"Decomposing task: {request}")
        steps = self.core.generate_plan(request)
        logging.info(f"Generated {len(steps)} steps for task.")
        return steps

    def get_plan_summary(self, steps: List[Dict[str, Any]]) -> str:
        return self.core.summarize_plan(steps)
