# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# PyAgent Implementation Plan

**Goal:**
Build the foundational pieces of the agent task‑workflow system 1 basic task model,
state machine, queue, and a minimal engine so future phases can flesh out 
the rich behaviour described in the design.

**Architecture:**
- Core Python classes under `src/core/workflow/`
- `TaskState` enum drives a lightweight state machine
- `Task` dataclass holds metadata/context and state transition methods
- `TaskQueue` wraps `asyncio.Queue` for enqueue/dequeue behaviour
- `WorkflowEngine` coordinates queue consumption and state updates

**Tech Stack:**
Python 3.11+, `pytest` for tests, `asyncio` for queue/engine.

This plan also leverages the previously created `context_manager` and
`skills_registry` packages (from the future roadmap plan) to handle
large context windows and dynamic tool/skill discovery.  Later tasks will
introduce a minimal Recursive Chain Of Thought (CORT) structure.

---

### Preliminary Task A: Verify context manager package

- File: `tests/test_context_components.py`
- Code:
  ```python
  from context_manager import ContextManager
  from skills_registry import SkillsRegistry
  
  def test_context_components_exist(tmp_path):
      cm = ContextManager(max_tokens=5)
      assert hasattr(cm, "push")
      registry = SkillsRegistry(tmp_path / "skills")
      assert isinstance(registry.list_skills(), list)
  ```
- Command:
  `pytest tests/test_context_components.py -q`
- Expected output:
  ```
  F
  ModuleNotFoundError: No module named 'context_manager'
  ```

### Task 1: Write failing test for `TaskState` enum

- File: `tests/test_task_state.py`
- Code:
  ```python
  import pytest
  from src.core.workflow.task import TaskState

  def test_taskstate_contains_expected_states():
      names = {s.name for s in TaskState}
      assert {"ACTIVE", "PAUSED", "FAILED", "COMPLETED", "RETRYING"} <= names
  ```
- Command:  
  `pytest tests/test_task_state.py -q`
- Expected output:
  ```
  F
  =================================== FAILURES ===================================
  ...
  ModuleNotFoundError: No module named 'src.core.workflow.task'
  ```

### Task 2: Implement `TaskState` enum

- File: `src/core/workflow/task.py`
- Code:
  ```python
  from enum import Enum

  class TaskState(Enum):
      ACTIVE = "active"
      PAUSED = "paused"
      FAILED = "failed"
      COMPLETED = "completed"
      RETRYING = "retrying"
  ```
- Command:  
  `pytest tests/test_task_state.py -q`
- Expected output:
  ```
  .                                                           [100%]
  ```

### Task 3: Write failing tests for `Task` dataclass

- File: `tests/test_task.py`
- Code:
  ```python
  import pytest
  from src.core.workflow.task import Task, TaskState

  def test_task_initial_state_and_metadata():
      t = Task(id="123", metadata={"foo": "bar"}, context={"a": 1})
      assert t.id == "123"
      assert t.metadata["foo"] == "bar"
      assert t.context["a"] == 1
      assert t.state == TaskState.ACTIVE
  ```
- Command:  
  `pytest tests/test_task.py::test_task_initial_state_and_metadata -q`
- Expected output:
  ```
  F
  NameError: name 'Task' is not defined
  ```

### Task 4: Implement `Task` dataclass with defaults

- File: `src/core/workflow/task.py` (append below enum)
- Code:
  ```python
  from dataclasses import dataclass, field
  from typing import Any, Dict

  @dataclass
  class Task:
      id: str
      metadata: Dict[str, Any] = field(default_factory=dict)
      context: Dict[str, Any] = field(default_factory=dict)
      state: TaskState = TaskState.ACTIVE

      def transition(self, new_state: TaskState):
          self.state = new_state
  ```
- Command:  
  `pytest tests/test_task.py::test_task_initial_state_and_metadata -q`
- Expected output:
  ```
  .                                                           [100%]
  ```

### Task 5: Write failing tests for state transitions on `Task`

- Add to `tests/test_task.py`:
  ```python
  def test_task_state_transitions():
      t = Task(id="x")
      t.transition(TaskState.FAILED)
      assert t.state is TaskState.FAILED
      t.transition(TaskState.RETRYING)
      assert t.state is TaskState.RETRYING
  ```
- Command:  
  `pytest tests/test_task.py -q`
- Expected output:
  ```
  F
  AttributeError: 'Task' object has no attribute 'transition'
  ```

### Task 6: Implement `transition` method (already added); rerun to confirm

- Command:  
  `pytest tests/test_task.py -q`
- Expected output:
  ```
  ..                                                          [100%]
  ```

### Task 7: Write failing tests for `TaskQueue` functionality

- File: `tests/test_task_queue.py`
- Code:
  ```python
  import pytest
  import asyncio
  from src.core.workflow.queue import TaskQueue
  from src.core.workflow.task import Task

  @pytest.mark.asyncio
  async def test_enqueue_dequeue():
      q = TaskQueue()
      t = Task(id="1")
      await q.enqueue(t)
      got = await q.dequeue()
      assert got is t
  ```
- Command:  
  `pytest tests/test_task_queue.py -q`
- Expected output:
  ```
  F
  ModuleNotFoundError: No module named 'src.core.workflow.queue'
  ```

### Task 8: Implement `TaskQueue` wrapper

- File: `src/core/workflow/queue.py`
- Code:
  ```python
  import asyncio
  from typing import Optional
  from .task import Task

  class TaskQueue:
      def __init__(self):
          self._q: asyncio.Queue[Task] = asyncio.Queue()

      async def enqueue(self, task: Task):
          await self._q.put(task)

      async def dequeue(self) -> Task:
          return await self._q.get()
  ```
- Command:  
  `pytest tests/test_task_queue.py -q`
- Expected output:
  ```
  .                                                            [100%]
  ```

### Task 9: Write failing tests for minimal `WorkflowEngine`

*(existing content continues)*

---

### Additional Task B: Chain Of Thought (CORT) structure

- File: `tests/test_cort.py`
- Code:
  ```python
  from context_manager import ContextManager
  from cort import ChainOfThought

  def test_cort_simple_branching():
      cm = ContextManager(max_tokens=10)
      cort = ChainOfThought(cm)
      root = cort.new_node("start")
      child = root.fork("step1")
      child.add("detail")
      assert "detail" in cm.snapshot()
  ```
- Command:
  `pytest tests/test_cort.py -q`
- Expected output:
  ```
  F
  ModuleNotFoundError: No module named 'cort'
  ```

- Implementation hint:
  Create `src/cort/__init__.py` with minimal `ChainOfThought` class that
  uses ContextManager and supports `new_node`, `fork`, and `add` methods.

---

(remaining tasks unchanged)

- File: `tests/test_workflow_engine.py`
- Code:
  ```python
  import pytest
  import asyncio
  from src.core.workflow.engine import WorkflowEngine
  from src.core.workflow.queue import TaskQueue
  from src.core.workflow.task import Task, TaskState

  @pytest.mark.asyncio
  async def test_engine_process_changes_state():
      q = TaskQueue()
      engine = WorkflowEngine(q)
      t = Task(id="z")
      await q.enqueue(t)
      await engine.run_once()  # process single task
      assert t.state == TaskState.COMPLETED
  ```
- Command:  
  `pytest tests/test_workflow_engine.py -q`
- Expected output:
  ```
  F
  ModuleNotFoundError: No module named 'src.core.workflow.engine'
  ```

### Task 10: Implement minimal `WorkflowEngine`

- File: `src/core/workflow/engine.py`
- Code:
  ```python
  import asyncio
  from .queue import TaskQueue
  from .task import Task, TaskState

  class WorkflowEngine:
      def __init__(self, queue: TaskQueue):
          self.queue = queue

      async def run_once(self):
          task: Task = await self.queue.dequeue()
          # simple prototype: mark complete immediately
          task.transition(TaskState.COMPLETED)
  ```
- Command:  
  `pytest tests/test_workflow_engine.py -q`
- Expected output:
  ```
  .                                                            [100%]
  ```

---

Once these steps run green, we will have the prototype 
foundation described in Phase 1 of the design. Let me know 
if you approve this plan or want adjustments before I save it.

## Implementation Status

All numbered tasks in this plan have now been executed during prior
sessions, and the corresponding code exists in the repository:

* `TaskState`, `Task`, `TaskQueue`, and `WorkflowEngine` implementations are
  all present under `src/core/workflow/` and are exercised by
  `tests/test_task_state.py`, `tests/test_task.py`,
  `tests/test_task_queue.py`, and `tests/test_workflow_engine.py` which
  currently pass.
* The CORT structure was added in `src/cort/__init__.py` and is covered by
  `tests/test_cort.py` and `tests/integration/test_context_and_skills.py`.
* Context management and skills registry packages are also available as
  described in the context management plan.

With these components in place and verified, the Phase 1 prototype of the
agent workflow is live and ready to serve as the basis for subsequent
enhancements.