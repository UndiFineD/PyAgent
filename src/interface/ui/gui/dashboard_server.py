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
PyAgent Dashboard Server Bridge
Acts as a stable bridge between the PyAgent backend and the React/Web frontend.
Provides REST API and WebSocket interfaces for real-time telemetry and management.
"""

from __future__ import annotations
from src.core.base.version import VERSION
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import json
import logging
from pathlib import Path
from datetime import datetime
from src.core.base.managers import HealthChecker

# Internal Imports
__version__ = VERSION

# Absolute Workspace Configuration
WORKSPACE_ROOT = Path("c:/DEV/PyAgent")
LOG_DIR = WORKSPACE_ROOT / "data" / "logs"
AGENT_LOG_FILE = LOG_DIR / "agent.log"
EPISODIC_LOG_FILE = LOG_DIR / "episodic_memory.jsonl"
SCREENSHOTS_DIR = LOG_DIR / "screenshots"
GENERATED_DIR = WORKSPACE_ROOT / "src" / "generated"

app = FastAPI(
    title="PyAgent Unified Desktop API",
    description="Bridge for PyAgent React/Web frontend",
    version=VERSION
)

# Global Manager Instances
health_checker = HealthChecker(repo_root=WORKSPACE_ROOT)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    """Manages active WebSocket connections for real-time telemetry."""
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]) -> None:
        """Send a JSON broadcast to all connected clients."""
        payload = message # message is already a dict, send_json will handle it
        for connection in self.active_connections:
            try:
                await connection.send_json(payload)
            except Exception:
                # Connection might be dead
                pass

manager = ConnectionManager()

@app.get("/api/version")
async def get_version() -> Dict[str, str]:
    """Returns the current PyAgent version."""
    return {"version": VERSION}

@app.get("/api/health")
async def get_health() -> Dict[str, Any]:
    """Returns the system health status from the HealthChecker manager."""
    try:
        return health_checker.check()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/api/status")
async def get_status() -> Dict[str, Any]:
    """Returns the current system status and metadata."""
    return {
        "status": "online",
        "agent": "PyAgent",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(),
        "workspace": str(WORKSPACE_ROOT)
    }

@app.get("/api/logs")
async def get_logs(limit: int = 100) -> List[str]:
    """Retrieve the last N lines of the agent log file if it exists."""
    if not AGENT_LOG_FILE.exists():
        # Fallback to check episodic memory if agent.log is missing
        if not EPISODIC_LOG_FILE.exists():
            return ["No log files found."]
        return [f"Log file not found at {AGENT_LOG_FILE}."]
    
    try:
        with open(AGENT_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-limit:]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading logs: {str(e)}")

@app.get("/api/thoughts")
async def get_thoughts(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve the latest episodic memories (agent thoughts/actions)."""
    if not EPISODIC_LOG_FILE.exists():
        return []
    
    thoughts = []
    try:
        with open(EPISODIC_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                if line.strip():
                    thoughts.append(json.loads(line))
    except (json.JSONDecodeError, Exception) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing thoughts: {str(e)}")
    
    return thoughts[::-1] # Newest first

@app.get("/api/artifacts")
async def list_artifacts() -> List[Dict[str, Any]]:
    """List files in the generated and screenshots directories."""
    artifacts = []
    monitored_paths = [
        {"type": "generated", "path": GENERATED_DIR},
        {"type": "screenshot", "path": SCREENSHOTS_DIR}
    ]
    
    for item in monitored_paths:
        p = item["path"]
        if p.exists() and p.is_dir():
            for entry in p.iterdir():
                if entry.is_file():
                    stat = entry.stat()
                    artifacts.append({
                        "name": entry.name,
                        "type": item["type"],
                        "path": str(entry),
                        "size": stat.st_size,
                        "modified": stat.st_mtime
                    })
    return artifacts

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time telemetry streaming."""
    await manager.connect(websocket)
    try:
        # Send initial connection success message
        await websocket.send_json({"event": "connected", "msg": "PyAgent Telemetry Bridge Active"})
        while True:
            # Wait for any messages from client (keeping connection open)
            data = await websocket.receive_text()
            # Simple heartbeat or specific command handling can go here
            await manager.broadcast({"event": "telemetry_echo", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        logging.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)