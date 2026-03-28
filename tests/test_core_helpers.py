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

"""Auxiliary tests exercising small core modules for coverage and meta-tests."""

from __future__ import annotations

import asyncio
import importlib


def test_agent_registry_validate() -> None:
    """Test that the AgentRegistry module can be imported and validated."""
    from src.core import agent_registry

    agent_registry.validate()


def test_memory_validate() -> None:
    """Test that the MemoryStore module can be imported and validated."""
    from src.core import memory

    memory.validate()


def test_observability_validate() -> None:
    """Test that the Observability module can be imported and validated."""
    from src.core import observability

    observability.validate()


def test_base_validate() -> None:
    """Test that the Base module can be imported and validated."""
    from src.core.base import validate as base_validate

    base_validate()


def test_agent_state_manager_validate() -> None:
    """Test that the AgentStateManager module can be imported and validated."""
    from src.core import agent_state_manager

    agent_state_manager.validate()


def test_workflow_components() -> None:
    """Test that basic workflow components can be imported and interact."""
    workflow_queue_module = importlib.import_module("src.core.workflow.queue")
    workflow_engine_module = importlib.import_module("src.core.workflow.engine")
    workflow_task_module = importlib.import_module("src.core.workflow.task")

    task_queue_class = workflow_queue_module.TaskQueue
    workflow_engine_class = workflow_engine_module.WorkflowEngine
    task_class = workflow_task_module.Task

    q = task_queue_class()
    eng = workflow_engine_class(q)
    t = task_class(id="z")
    # queue and engine basic operations
    assert eng.queue is q
    asyncio.run(q.enqueue(t))
    got = asyncio.run(q.dequeue())
    assert got is t
    assert getattr(t, "state", None) is not None


def test_workflow_queue_and_task_validate() -> None:
    """Exercise the workflow queue/task validate helpers."""
    workflow_queue = importlib.import_module("src.core.workflow.queue")
    workflow_task = importlib.import_module("src.core.workflow.task")

    workflow_queue.validate()
    workflow_task.validate()


def test_scaffold_import_and_example() -> None:
    """Import the scaffold module and exercise its example class."""
    from src.core import scaffold

    # instantiate and call the example method
    example = scaffold.ExampleCore(name="xyz")
    out = example.do_work({"a": 1})
    assert out["status"] == "ok"


def test_basic_runtime_modules_validate() -> None:
    """Import lightweight runtime modules and verify their validate hooks."""
    memory = importlib.import_module("src.memory")
    multimodal = importlib.import_module("src.multimodal")
    rl = importlib.import_module("src.rl")

    assert memory.validate()
    assert multimodal.validate()
    assert rl.validate()
