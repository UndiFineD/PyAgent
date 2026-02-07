#!/usr/bin/env python3
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

# VOYAGER STABILITY: Unified Dashboard Server (Final V1.5.0)

from __future__ import annotations
import asyncio, json, logging, psutil
from datetime import datetime
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# --- CONFIG & PATHS ---
WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
WEB_UI_DIR = (WORKSPACE_ROOT / "src" / "interface" / "ui" / "web").resolve()
EPISODIC_LOG_FILE = (WORKSPACE_ROOT / "data" / "logs" / "episodic_memory.jsonl").resolve()

# --- INITIALIZATION ---
app = FastAPI(title="PyAgent Unified Voyager API", version="1.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- TELEMETRY ENGINE ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)
    def disconnect(self, ws: WebSocket):
        if ws in self.active_connections: self.active_connections.remove(ws)
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try: await connection.send_json(message)
            except: pass

manager = ConnectionManager()

async def telemetry_loop():
    """Background task to broadcast system vitals."""
    while True:
        try:
            await manager.broadcast({
                "event": "telemetry",
                "data": {
                    "cpu": psutil.cpu_percent(),
                    "mem": psutil.virtual_memory().percent,
                    "network": psutil.net_io_counters().bytes_sent % 100,
                    "timestamp": datetime.now().timestamp()
                }
            })
        except: pass
        await asyncio.sleep(1.0)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telemetry_loop())

# --- PRIMARY NAVIGATION (Prioritized Routes) ---

@app.get("/stream")
async def serve_stream():
    """PRIORITY: Serves the draggable Multi-Channel Stream Console."""
    path = WEB_UI_DIR / "stream_console.html"
    if path.exists():
        return FileResponse(str(path), media_type="text/html")
    return JSONResponse(status_code=404, content={"error": f"Console not found at {path}"})

@app.get("/topology")
async def serve_topology():
    path = WEB_UI_DIR / "topology_viewer.html"
    return FileResponse(str(path), media_type="text/html") if path.exists() else {"error": "404"}

@app.get("/")
async def serve_index():
    path = WEB_UI_DIR / "index.html"
    if path.exists():
        return FileResponse(str(path), media_type="text/html")
    return {"status": "Dashboard Active (No index.html found)"}

# --- API ENDPOINTS ---

@app.get("/api/thoughts")
async def get_thoughts():
    if not EPISODIC_LOG_FILE.exists(): return []
    try:
        with open(EPISODIC_LOG_FILE, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f.readlines()[-50:][::-1]]
    except: return []

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- MOUNTS (MUST COME LAST) ---
if WEB_UI_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(WEB_UI_DIR)), name="web")

if __name__ == "__main__":
    import uvicorn
    # Using 0.0.0.0 to ensure accessibility across the LAN if needed
    uvicorn.run(app, host="0.0.0.0", port=8000)
