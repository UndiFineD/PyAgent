# Description: `AgentAPIServer.py`

## Module purpose

FastAPI-based API gateway for the PyAgent fleet.

## Location
- Path: `src\infrastructure\api\AgentAPIServer.py`

## Public surface
- Classes: TaskRequest, TelemetryManger
- Functions: root, list_agents, dispatch_task, websocket_endpoint

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `asyncio`, `fastapi`, `pydantic`, `typing`, `json`, `time`, `src.infrastructure.fleet.FleetManager`, `src.infrastructure.api.FleetLoadBalancer`, `uvicorn`

## Metadata

- SHA256(source): `d35806db49824345`
- Last updated: `2026-01-11 10:15:14`
- File: `src\infrastructure\api\AgentAPIServer.py`