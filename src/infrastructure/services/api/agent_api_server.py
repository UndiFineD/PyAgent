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


"""
FastAPI-based API gateway for the PyAgent fleet.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.services.api.fleet_load_balancer import \
    FleetLoadBalancer
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

__version__ = VERSION

app = FastAPI(title="PyAgent Unified API")

# Global instances
workspace_root = str(Path(__file__).resolve().parents[3]) + ""
fleet = FleetManager(workspace_root)
load_balancer = FleetLoadBalancer(fleet)


class TaskRequest(BaseModel):
    """Schema for incoming task requests via the REST API."""

    agent_id: str

    task: str

    context: dict[str, Any] = {}
    interface: str | None = "Web"  # Default to web if not specified


class TelemetryManager:
    """Manages WebSocket connections for real-time fleet telemetry."""

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
            except Exception:  # pylint: disable=broad-exception-caught
                pass


telemetry = TelemetryManager()


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
    return {"agents": [{"id": k, "type": type(v).__name__} for k, v in fleet.agents.items()]}


@app.get("/discovery/peers")
async def list_discovery_peers() -> dict[str, Any]:
    """Returns the list of peers discovered on the LAN."""
    return {"peers": [p.to_dict() for p in fleet.get_lan_peers()]}


@app.get("/discovery/peers/fastest")
async def list_fastest_peers() -> dict[str, Any]:
    """Returns the top 5 lowest-latency peers discovered."""
    return {"peers": [p.to_dict() for p in fleet.get_fastest_peers()]}


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
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
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
