"""
LLM_CONTEXT_START

## Source: src-old/classes/api/AgentAPIServer.description.md

# AgentAPIServer

**File**: `src\classes\api\AgentAPIServer.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 15 imports  
**Lines**: 131  
**Complexity**: 2 (simple)

## Overview

FastAPI-based API gateway for the PyAgent fleet.

## Classes (2)

### `TaskRequest`

**Inherits from**: BaseModel

Class TaskRequest implementation.

### `TelemetryManger`

Class TelemetryManger implementation.

**Methods** (2):
- `__init__(self)`
- `disconnect(self, websocket)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `fastapi.FastAPI`
- `fastapi.WebSocket`
- `fastapi.WebSocketDisconnect`
- `json`
- `pydantic.BaseModel`
- `src.core.base.version.VERSION`
- `src.infrastructure.api.FleetLoadBalancer.FleetLoadBalancer`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uvicorn`

---
*Auto-generated documentation*
## Source: src-old/classes/api/AgentAPIServer.improvements.md

# Improvements for AgentAPIServer

**File**: `src\classes\api\AgentAPIServer.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 131 lines (medium)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **2 undocumented classes**: TaskRequest, TelemetryManger

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentAPIServer_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
FastAPI-based API gateway for the PyAgent fleet.
"""

from src.core.base.version import VERSION
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import time
from src.infrastructure.fleet.FleetManager import FleetManager
from src.infrastructure.api.FleetLoadBalancer import FleetLoadBalancer

__version__ = VERSION

app = FastAPI(title="PyAgent Unified API")

# Global instances
workspace_root = str(Path(__file__).resolve().parents[3]) + ""
fleet = FleetManager(workspace_root)
load_balancer = FleetLoadBalancer(fleet)


class TaskRequest(BaseModel):
    agent_id: str
    task: str
    context: dict[str, Any] = {}
    interface: str | None = "Web"  # Default to web if not specified


class TelemetryManger:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass


telemetry = TelemetryManger()


@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "status": "online",
        "version": "2.0.0",
        "fleet_size": len(fleet.agents),
        "lb_stats": load_balancer.get_stats(),
    }


@app.get("/agents")
async def list_agents() -> dict[str, Any]:
    return {
        "agents": [{"id": k, "type": type(v).__name__} for k, v in fleet.agents.items()]
    }


@app.post("/task")
async def dispatch_task(request: TaskRequest) -> dict[str, Any]:
    # Route through Load Balancer
    lb_result = load_balancer.balance_request(request.interface, request.task)
    if lb_result.get("status") == "REJECTED":
        return {"status": "error", "message": lb_result.get("reason"), "code": 429}

    # Log task start to telemetry
    await telemetry.broadcast(
        json.dumps(
            {
                "type": "task_started",
                "agent": request.agent_id,
                "interface": request.interface,
                "timestamp": time.time(),
                "lb_metadata": lb_result,
            }
        )
    )

    # Simulate routing to agent
    # In a real scenario, we'd use fleet.get_agent(request.agent_id).run(...)
    try:
        # Mock result for now
        result = f"Task '{request.task}' received by {request.agent_id}"

        await telemetry.broadcast(
            json.dumps(
                {
                    "type": "task_completed",
                    "agent": request.agent_id,
                    "status": "success",
                    "timestamp": time.time(),
                }
            )
        )
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await telemetry.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
            # Echo or handle incoming messages
    except WebSocketDisconnect:
        telemetry.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
