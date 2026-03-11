#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""LLM_CONTEXT_START

## Source: src-old/pyagent_cli.description.md

# pyagent_cli

**File**: `src\pyagent_cli.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 11 imports  
**Lines**: 161  
**Complexity**: 4 (simple)

## Overview

PyAgent CLI Interface.
Connects to the Fleet Load Balancer via the Agent API Server.

## Functions (4)

### `check_server()`

Verify that the API server is running with 15m TTL caching.

### `list_agents()`

Get list of active agents from the fleet.

### `run_task(agent_id, task)`

Dispatch a task to a specific agent via the Load Balancer.

### `main()`

## Dependencies

**Imports** (11):
- `argparse`
- `json`
- `pathlib.Path`
- `requests`
- `rich.console.Console`
- `rich.panel.Panel`
- `rich.table.Table`
- `src.classes.backend.LocalContextRecorder.LocalContextRecorder`
- `src.classes.base_agent.ConnectivityManager.ConnectivityManager`
- `src.version.VERSION`
- `sys`

---
*Auto-generated documentation*
## Source: src-old/pyagent_cli.improvements.md

# Improvements for pyagent_cli

**File**: `src\pyagent_cli.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 161 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `pyagent_cli_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
PyAgent CLI Interface.
Connects to the Fleet Load Balancer via the Agent API Server.
"""


# from functools import lru_cache

import argparse
import sys

# import time
from pathlib import Path

import requests

# # # from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.classes.backend.LocalContextRecorder import LocalContextRecorder

# Infrastructure
from src.classes.base_agent.ConnectivityManager import ConnectivityManager

console = Console()
API_BASE_URL = "http://localhost:8000"
session = requests.Session()

# Initializing infrastructure with generic workspace root
WORKSPACE_ROOT = Path("c:/DEV/PyAgent")
conn_manager = ConnectivityManager(str(WORKSPACE_ROOT))
recorder = LocalContextRecorder(WORKSPACE_ROOT, "CLI_System")


def check_server() -> bool:
    """Verify that the API server is running with 15m TTL caching."""
    if not conn_manager.is_endpoint_available("AgentAPIServer"):
        return False

    try:
        response = session.get(f"{API_BASE_URL}/", timeout=2)
        available = response.status_code == 200
        conn_manager.update_status("AgentAPIServer", available)
        return available
    except requests.exceptions.RequestException:
        conn_manager.update_status("AgentAPIServer", False)
        return False


def list_agents() -> None:
    """Get list of active agents from the fleet."""
    try:
        response = session.get(f"{API_BASE_URL}/agents")
        if response.status_code == 200:
            agents = response.json().get("agents", [])
            table = Table(title="PyAgent Fleet: Active Agents")
            table.add_column("Agent ID", style="cyan")
            table.add_column("Type", style="magenta")

            for agent in agents:
                table.add_row(agent["id"], agent["type"])

            console.print(table)

            # Intelligence Harvesting
            recorder.record_lesson("cli_list_agents", {"count": len(agents)})
        else:
            console.print(f"[red]Error fetching agents: {response.text}[/red]")
    except Exception as e:
        console.print(f"[red]Connection failed: {e}[/red]")


def run_task(agent_id: str, task: str) -> None:
    """Dispatch a task to a specific agent via the Load Balancer."""
    payload = {"agent_id": agent_id, "task": task, "interface": "CLI", "context": {}}

    console.print(
        f"[yellow]Dispatching task to {agent_id} via Load Balancer...[/yellow]"
    )

    # Intelligence Harvesting
    recorder.record_lesson("cli_task_dispatch", payload)

    try:
        response = session.post(f"{API_BASE_URL}/task", json=payload)
        data = response.json()

        if response.status_code == 200 and data.get("status") == "success":
            console.print(
                Panel(data["result"], title="Task Result", border_style="green")
            )
            recorder.record_lesson("cli_task_success", {"result": data["result"]})
        elif data.get("code") == 429:
            console.print(
                f"[bold red]Load Balancer Rejected Request: {data.get('message')}[/bold red]"
            )
            recorder.record_lesson("cli_task_rejected", {"reason": data.get("message")})
        else:
            console.print(f"[red]Error: {data.get('message', 'Unknown error')}[/red]")
            recorder.record_lesson("cli_task_error", {"error": data.get("message")})

    except Exception as e:
        console.print(f"[red]Connection failed: {e}[/red]")
        recorder.record_lesson("cli_task_network_failure", {"exception": str(e)})


def main() -> None:
    parser = argparse.ArgumentParser(description="PyAgent Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    subparsers.add_parser("list", help="List all available agents in the fleet")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a task on a specific agent")
    run_parser.add_argument("agent", help="ID of the agent to use")
    run_parser.add_argument("task", help="The task description/prompt")

    # Stats command
    subparsers.add_parser("status", help="Check system and Load Balancer status")

    args = parser.parse_args()

    if not check_server():
        console.print("[bold red]Error: API Server is not running.[/bold red]")
        console.print(
            "[yellow]Please start the server first: python -m uvicorn src.classes.api.AgentAPIServer:app[/yellow]"
        )
        sys.exit(1)

    if args.command == "list":
        list_agents()
    elif args.command == "run":
        run_task(args.agent, args.task)
    elif args.command == "status":
        try:
            response = session.get(f"{API_BASE_URL}/")
            data = response.json()
            lb_stats = data.get("lb_stats", {})

            status_text = f"Version: {data['version']}\n"
            status_text += f"Fleet Size: {data['fleet_size']}\n"
            status_text += f"LB Queue Depth: {lb_stats.get('queue_depth', 0)}\n"
            status_text += f"LB Interface Diversity: {', '.join(lb_stats.get('interface_diversity', []))}"

            console.print(
                Panel(status_text, title="System Status", border_style="blue")
            )
        except Exception as e:
            console.print(f"[red]Could not retrieve status: {e}[/red]")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
