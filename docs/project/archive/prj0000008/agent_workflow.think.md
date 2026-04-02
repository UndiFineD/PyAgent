# agent_workflow - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-20_

## Root Cause Analysis
- PyAgent needs a stable task lifecycle model before swarm orchestration can be built.
- Without a state machine, task transitions (ACTIVE → PAUSED → FAILED → RETRYING → COMPLETED)
  are inconsistent or implicit across agents.
- A queue and engine are required to coordinate concurrent task execution safely with asyncio.

## Options

### Option A — Minimal workflow layer under `src/core/workflow/`
`TaskState` enum + `Task` dataclass + `TaskQueue` (asyncio.Queue wrapper) + `WorkflowEngine`
coordinator. Small, focused, testable.
Pros: Low coupling, direct TDD path, consistent with mixin architecture.
Cons: Future extensions require more modules (e.g., priority queue, retry backoff).

### Option B — Integrate directly into `BaseAgent`
Embed task state tracking inside the base agent class.
Pros: Fewer files.
Cons: Violates Core/Agent separation principle; hard to test in isolation.

### Option C — Use an external workflow library (e.g., Prefect, Temporal)
Pros: Feature-rich out of the box.
Cons: Heavy dependency, overkill for internal agent orchestration, breaks autonomy goals.

## Decision Matrix
| Criterion | Opt A | Opt B | Opt C |
|---|---|---|---|
| Testability | High | Low | Medium |
| Coupling | Low | High | Medium |
| Delivery speed | Fast | Fast | Slow |
| Consistency with architecture | High | Low | Low |

## Selected Option
**Option A** — Minimal `src/core/workflow/` module set. Consistent with mixin-based architecture,
full TDD, and zero external dependencies.
