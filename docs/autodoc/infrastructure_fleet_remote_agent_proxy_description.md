# Description: `RemoteAgentProxy.py`

## Module purpose

Proxy for agents running on remote nodes.
Allows FleetManager to transparently call tools on other machines.

## Location
- Path: `infrastructure\fleet\RemoteAgentProxy.py`

## Public surface
- Classes: RemoteAgentProxy
- Functions: (none)

## Behavior summary
- Pure module (no obvious CLI / side effects).

## Key dependencies
- Top imports: `__future__`, `requests`, `json`, `logging`, `os`, `time`, `typing`, `src.core.base.BaseAgent`, `src.core.base.ConnectivityManager`, `src.infrastructure.backend.LocalContextRecorder`

## Metadata

- SHA256(source): `e4832c15f3ecac16`
- Last updated: `2026-01-11 12:53:44`
- File: `infrastructure\fleet\RemoteAgentProxy.py`