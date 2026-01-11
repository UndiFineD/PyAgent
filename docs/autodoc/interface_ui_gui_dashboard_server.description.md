# Description: `dashboard_server.py`

## Module purpose

PyAgent Dashboard Server Bridge
Acts as a stable bridge between the PyAgent backend and the React/Web frontend.
Provides REST API and WebSocket interfaces for real-time telemetry and management.

## Location
- Path: `interface\ui\gui\dashboard_server.py`

## Public surface
- Classes: ConnectionManager
- Functions: get_version, get_health, get_status, get_logs, get_thoughts, list_artifacts, websocket_telemetry

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `fastapi`, `fastapi.middleware.cors`, `typing`, `json`, `logging`, `pathlib`, `datetime`, `src.core.base.version`, `src.core.base.managers`, `uvicorn`

## Metadata

- SHA256(source): `78f805f61ffdc551`
- Last updated: `2026-01-11 12:54:07`
- File: `interface\ui\gui\dashboard_server.py`