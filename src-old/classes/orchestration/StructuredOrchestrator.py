#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/orchestration/StructuredOrchestrator.description.md

# StructuredOrchestrator

**File**: `src\classes\orchestration\StructuredOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 110  
**Complexity**: 9 (moderate)

## Overview

Orchestrator implementing the 7-phase Inner Loop from Personal AI Infrastructure (PAI).
Phases: Observe, Think, Plan, Build, Execute, Verify, Learn.

## Classes (1)

### `StructuredOrchestrator`

High-reliability task orchestrator using a 7-phase scientific method loop.

**Methods** (9):
- `__init__(self, fleet)`
- `execute_task(self, task)`
- `_phase_observe(self, task)`
- `_phase_think(self, task, observation)`
- `_phase_plan(self, task, thoughts)`
- `_phase_build(self, task, plan)`
- `_phase_execute(self, plan)`
- `_phase_verify(self, execution_result, criteria)`
- `_phase_learn(self, task, verification)`

## Dependencies

**Imports** (7):
- `json`
- `logging`
- `src.classes.fleet.FleetManager.FleetManager`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/StructuredOrchestrator.improvements.md

# Improvements for StructuredOrchestrator

**File**: `src\classes\orchestration\StructuredOrchestrator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 110 lines (medium)  
**Complexity**: 9 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StructuredOrchestrator_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""Orchestrator implementing the 7-phase Inner Loop from Personal AI Infrastructure (PAI).
Phases: Observe, Think, Plan, Build, Execute, Verify, Learn.
"""

import logging
import json
from typing import Dict, List, Any, Optional
from src.classes.fleet.FleetManager import FleetManager


class StructuredOrchestrator:
    """High-reliability task orchestrator using a 7-phase scientific method loop."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.current_context: Dict[str, Any] = {}

    def execute_task(self, task: str) -> str:
        """Runs the 7-phase cycle for a given task."""
        logging.info(f"StructuredOrchestrator: Starting 7-phase cycle for task: {task}")

        report = [f"# Structured Execution Report: {task}\n"]

        # Phase 1: OBSERVE
        observe_res = self._phase_observe(task)
        report.append(f"## Phase 1: OBSERVE\n{observe_res}\n")

        # Phase 2: THINK
        think_res = self._phase_think(task, observe_res)
        report.append(f"## Phase 2: THINK\n{think_res}\n")

        # Phase 3: PLAN
        plan_res = self._phase_plan(task, think_res)
        report.append(f"## Phase 3: PLAN\n{plan_res}\n")

        # Phase 4: BUILD (Define Verification Criteria)
        build_res = self._phase_build(task, plan_res)
        report.append(f"## Phase 4: BUILD (Verification Specs)\n{build_res}\n")

        # Phase 5: EXECUTE
        exec_res = self._phase_execute(plan_res)
        report.append(f"## Phase 5: EXECUTE\n{exec_res}\n")

        # Phase 6: VERIFY
        verify_res = self._phase_verify(exec_res, build_res)
        report.append(f"## Phase 6: VERIFY\n{verify_res}\n")

        # Phase 7: LEARN
        learn_res = self._phase_learn(task, verify_res)
        report.append(f"## Phase 7: LEARN\n{learn_res}\n")

        return "\n".join(report)

    def _phase_observe(self, task: str) -> str:
        """Gather initial context and state using MemoRAG and Self-Search."""
        # Step 1: MemoRAG Clue Generation
        clues = self.fleet.call_by_capability("MemoRAG.generate_clues", context=task)

        # Step 2: Self-Search (Internal Knowledge Retrieval - SSRL Pattern)
        self_search = self.fleet.call_by_capability(
            "SelfSearch.perform_internal_search", query=task
        )

        # Step 3: Global Context Retrieval
        global_ctx = self.fleet.global_context.get_context_for_task(task)

        return f"Clues: {clues}\n\nInternal Search: {self_search}\n\nGlobal Knowledge: {global_ctx}"

    def _phase_think(self, task: str, observation: str) -> str:
        """Reason about the problem, generate hypotheses, and optimize model strategy."""
        # Step 1: Optimize Model Strategy (AirLLM Pattern)
        optimization = self.fleet.call_by_capability(
            "ModelOptimizer.improve_content", task_description=task
        )

        # Step 2: Complex Reasoning
        reasoning = self.fleet.call_by_capability(
            "Reasoner.analyze", input=f"Task: {task}\nObservation: {observation}"
        )

        return f"Optimization Strategy: {optimization}\n\nReasoning: {reasoning}"

    def _phase_plan(self, task: str, thoughts: str) -> List[Dict[str, Any]]:
        """Create a step-by-step execution plan."""
        # This returns JSON steps for the FleetManager to execute
        planner_res = self.fleet.call_by_capability(
            "TaskPlannerAgent.create_plan", user_request=task
        )
        # Note: In real life we'd parse this, but for the demo we assume it's a list
        if isinstance(planner_res, str):
            try:
                return json.loads(planner_res)
            except Exception:
                return []
        return planner_res

    def _phase_build(self, task: str, plan: Any) -> str:
        """Define what success looks like."""
        return self.fleet.call_by_capability(
            "Security.improve_content",
            prompt=f"Define verification criteria for: {task}",
        )

    def _phase_execute(self, plan: List[Dict[str, Any]]) -> str:
        """Run the planned steps."""
        if not plan:
            return "Error: No plan generated in Phase 3."
        return self.fleet.execute_workflow("7-Phase Execution", plan)

    def _phase_verify(self, execution_result: str, criteria: str) -> str:
        """Compare execution results against build criteria."""
        return self.fleet.call_by_capability(
            "Security.improve_content",
            prompt=f"Verify if the result matches criteria.\nResult: {execution_result}\nCriteria: {criteria}",
        )

    def _phase_learn(self, task: str, verification: str) -> str:
        """Extract insights and update global context."""
        return self.fleet.global_context.record_lesson(
            failure_context=task,
            correction=verification,
            agent="StructuredOrchestrator",
        )
