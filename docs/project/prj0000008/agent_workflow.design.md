# agent_workflow - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-20_

## Design Summary
A four-module workflow layer under `src/core/workflow/` implementing a task state machine,
async queue, and a minimal engine. CoRT (Recursive Chain of Thought) scaffolded in `src/cort/`.

## Architecture
```
src/core/workflow/
  __init__.py      — re-exports TaskState, Task, TaskQueue, WorkflowEngine
  task.py          — TaskState enum + Task dataclass with state transition methods
  queue.py         — TaskQueue wrapping asyncio.Queue for enqueue/dequeue
  engine.py        — WorkflowEngine: consumes queue, drives state updates

src/cort/
  __init__.py      — Minimal CoRT scaffolding: branching chain-of-thought loop
```

## State Machine
```
PENDING → ACTIVE → COMPLETED
                 → FAILED → RETRYING → ACTIVE
                 → PAUSED  → ACTIVE
```

## Module Contracts
- `TaskState`: enum with PENDING, ACTIVE, PAUSED, FAILED, COMPLETED, RETRYING
- `Task`: dataclass with `task_id`, `state`, `metadata`; methods `activate()`, `complete()`, `fail()`, `pause()`, `retry()`
- `TaskQueue`: `async enqueue(task)`, `async dequeue() → Task`
- `WorkflowEngine`: `async process(task) → Task` — drives state transitions

## Dependencies
- Python `asyncio`, `dataclasses`, `enum` — stdlib only
- `context_manager` and `skills_registry` packages (already present)
