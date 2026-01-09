import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import time
from src.classes.fleet.FleetManager import FleetManager

app = FastAPI(title="PyAgent Unified API")

# Global fleet instance
workspace_root = "c:/DEV/PyAgent"
fleet = FleetManager(workspace_root)

class TaskRequest(BaseModel):
    agent_id: str
    task: str
    context: Dict[str, Any] = {}

class TelemetryManger:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

telemetry = TelemetryManger()

@app.get("/")
async def root():
    return {"status": "online", "version": "1.5.0", "fleet_size": len(fleet.agents)}

@app.get("/agents")
async def list_agents():
    return {
        "agents": [
            {"id": k, "type": type(v).__name__} for k, v in fleet.agents.items()
        ]
    }

@app.post("/task")
async def dispatch_task(request: TaskRequest):
    # Log task start to telemetry
    await telemetry.broadcast(json.dumps({
        "type": "task_started",
        "agent": request.agent_id,
        "timestamp": time.time()
    }))
    
    # Simulate routing to agent
    # In a real scenario, we'd use fleet.get_agent(request.agent_id).run(...)
    try:
        # Mock result for now
        result = f"Task '{request.task}' received by {request.agent_id}"
        
        await telemetry.broadcast(json.dumps({
            "type": "task_completed",
            "agent": request.agent_id,
            "status": "success",
            "timestamp": time.time()
        }))
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await telemetry.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo or handle incoming messages
    except WebSocketDisconnect:
        telemetry.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
