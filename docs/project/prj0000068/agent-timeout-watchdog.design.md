# agent-timeout-watchdog — Design

_Owner: @3design_

## Interface

```python
class AgentWatchdog:
    def __init__(self, timeout_s: float = 30.0, max_retries: int = 3): ...
    async def run(self, agent_id: str, coro) -> dict: ...
    def status(self) -> dict: ...
    @property
    def dead_letter_queue(self) -> list[dict]: ...
```

### `run(agent_id, coro) -> dict`
- Wraps `coro` with `asyncio.wait_for(coro, timeout_s)`
- On success: returns `{"status": "ok", "agent_id": ..., "result": ...}`
- On `asyncio.TimeoutError`: increments per-agent retry counter; if retries < max_retries, re-raises for caller to retry; otherwise pushes to DLQ and returns `{"status": "dead_letter", ...}`
- On other exceptions: propagates

### `status() -> dict`
Returns `{"timeout_s": ..., "max_retries": ..., "dlq_size": ..., "retry_counts": {...}}`

## REST endpoint
`GET /api/watchdog/status` — returns `watchdog.status()`

## Module-level singleton
`watchdog = AgentWatchdog()` in `backend/watchdog.py`
