# agent_workflow - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-20_

## Implementation Summary
Workflow state machine, async queue, engine, and CoRT scaffold implemented under `src/core/workflow/` and `src/cort/`.

## Modules
| Module | Status |
|---|---|
| `src/core/workflow/__init__.py` | DONE |
| `src/core/workflow/task.py` | DONE |
| `src/core/workflow/queue.py` | DONE |
| `src/core/workflow/engine.py` | DONE |
| `src/cort/__init__.py` | DONE |

## Related modules (agent registry / state manager)
| Module | Status |
|---|---|
| `src/core/agent_registry.py` | DONE |
| `src/core/agent_state_manager.py` | DONE |
| `src/swarm/agent_registry.py` | DONE |
| `src/tools/agent_plugins.py` | DONE |

## Test Run
```powershell
python -m pytest tests/ -k "workflow or task_state or cort" -q
# 9 passed
```

## Deferred Items
- Priority queue and retry-backoff scheduling
- Full swarm orchestration (tracked in prj022-swarm_architecture)
