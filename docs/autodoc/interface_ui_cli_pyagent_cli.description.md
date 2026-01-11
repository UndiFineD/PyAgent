# Description: `pyagent_cli.py`

## Module purpose

PyAgent CLI Interface.
Connects to the Fleet Load Balancer via the Agent API Server.

## Location
- Path: `interface\ui\cli\pyagent_cli.py`

## Public surface
- Classes: (none)
- Functions: check_server, list_agents, run_task, main

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Uses `argparse` for CLI parsing.

## Key dependencies
- Top imports: `src.core.base.version`, `sys`, `json`, `requests`, `argparse`, `pathlib`, `rich.console`, `rich.table`, `rich.panel`, `src.core.base.ConnectivityManager`, `src.infrastructure.backend.LocalContextRecorder`

## Metadata

- SHA256(source): `7a321cab15d9542e`
- Last updated: `2026-01-11 12:54:04`
- File: `interface\ui\cli\pyagent_cli.py`