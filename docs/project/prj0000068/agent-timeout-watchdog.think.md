# agent-timeout-watchdog — Think

_Owner: @2think_

## Problem
Agents can hang indefinitely. We need:
1. Per-agent execution timeout (configurable)
2. Automatic retry on timeout (with a retry budget)
3. Dead-letter queue for tasks that exhaust retries

## Alternatives

### A — asyncio.wait_for wrapper (chosen)
Wrap each task coroutine with `asyncio.wait_for(coro, timeout)`. On `asyncio.TimeoutError`, increment retry counter; if under budget, re-queue; otherwise push to DLQ.

### B — threading.Timer
Works but mixes threads and asyncio — complexity overhead, not idiomatic.

### C — External process supervisor
Overkill for the scope and budget tier M.

## Decision
Option A — pure asyncio, lightweight, easy to test with mocks.
