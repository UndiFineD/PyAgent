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

# VOYAGER STABILITY: Fleet Load Balancer (v1.5.0)

"""Fleet Web UI Engine for workflow visualization.
Generates data structures for internal/external dashboard consumers.
"""

import uvicorn
import json
import asyncio
import sys
import os
import time
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from src.infrastructure.security.auth.webauthn_manager import WebAuthnManager
from src.infrastructure.swarm.resilience.checkpoint_manager import CheckpointManager

# VOYAGER STABILITY: Fix for ZeroMQ on Windows Proactor Loop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Absolute resolution is critical on Windows
WEB_UI_DIR = Path(__file__).resolve().parent
# Workspace Root is 4 levels up: web -> ui -> interface -> src -> root
WORKSPACE_ROOT = WEB_UI_DIR.parent.parent.parent.parent
LOGS_DIR = WORKSPACE_ROOT / "data" / "logs"

# Global Fleet Instance
fleet_instance = None
auth_manager = WebAuthnManager()
checkpoint_manager = CheckpointManager(rank=0, world_size=1) # Default for web proxy

@asynccontextmanager
async def lifespan(app: FastAPI):
    global fleet_instance
    try:
        from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
        fleet_instance = FleetManager(str(WORKSPACE_ROOT))
        print(f"FleetManager initialized at {WORKSPACE_ROOT}")
    except Exception as e:
        print(f"Failed to initialize FleetManager: {e}")
    yield

app = FastAPI(title="PyAgent Fleet API", lifespan=lifespan)

# Helper for system metrics
def get_system_metrics():
    global fleet_instance
    if fleet_instance and hasattr(fleet_instance, "resource_monitor"):
        stats = fleet_instance.resource_monitor.get_latest_stats()
        # Map to UI keys
        return {
            "cpu": round(stats.get("cpu_usage", 0), 1),
            "mem": round(stats.get("memory_usage", 0), 1),
            "storage": round(stats.get("disk_usage", 0), 1),
            "network": abs(round(stats.get("network_io", {}).get("bytes_sent", 0) / 1024 / 1024, 2)) % 100, # Mock activity for bar
            "temp": round(stats.get("temp", 0), 1),
            "gpu": round(stats.get("gpu", {}).get("usage", 0), 1)
        }
    
    try:
        import psutil
        return {
            "cpu": psutil.cpu_percent(),
            "mem": psutil.virtual_memory().percent,
            "storage": psutil.disk_usage("/").percent,
            "network": 0,
            "temp": 0,
            "gpu": 0
        }
    except ImportError:
        return {"cpu": 0, "mem": 0, "storage": 0, "network": 0, "temp": 0, "gpu": 0}

# 1. SPECIFIC ROUTES FIRST
@app.get("/api/thoughts")
async def get_thoughts():
    """Returns the last 50 thoughts from the reasoning chain."""
    log_file = LOGS_DIR / "reasoning_chains.jsonl"
    thoughts = []
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-50:]:
                try:
                    data = json.loads(line)
                    # Map reasoning chain keys to UI expectations
                    mapped = {
                        "role": data.get("role", "assistant" if data.get("agent") else "user"),
                        "action": data.get("agent") or data.get("action"),
                        "content": data.get("content") or data.get("justification") or str(data.get("context_summary")),
                        "timestamp": data.get("timestamp") or 0
                    }
                    thoughts.append(mapped)
                except json.JSONDecodeError:
                    continue
    return thoughts

@app.post("/api/command")
async def handle_command(data: dict):
    """Dispatches a command to the swarm (Pillar 3)."""
    global fleet_instance
    command = data.get("command")
    if not command:
        return JSONResponse(status_code=400, content={"error": "No command provided"})
    
    if fleet_instance:
        # For Pillar 3, we route this to the FleetManager's command handler
        # which will use the UniversalAgent/Coores architecture
        if hasattr(fleet_instance, "handle_user_command"):
            asyncio.create_task(fleet_instance.handle_user_command(command))
            return {"status": "dispatched", "command": command}
        else:
            # Fallback for now: log it so it shows in Thoughts
            log_file = LOGS_DIR / "reasoning_chains.jsonl"
            entry = {
                "timestamp": time.time(),
                "role": "user",
                "content": command,
                "action": "input"
            }
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            return {"status": "logged", "command": command}

    return JSONResponse(status_code=503, content={"error": "Fleet not ready"})

@app.get("/api/topology")
async def get_topology():
    """Returns the current swarm topology."""
    topology_file = LOGS_DIR / "topology.json"
    if topology_file.exists():
        with open(topology_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"nodes": [], "links": []}

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            metrics = get_system_metrics()
            
            # Phase 326: Consensus Activity Reporting
            consensus_active = False
            if fleet_instance and hasattr(fleet_instance, "consensus_manager"):
                # Check for active consensus tasks (Mock logic for HUD)
                if hasattr(fleet_instance, "active_tasks"):
                    consensus_active = any("consensus" in str(t).lower() for t in fleet_instance.active_tasks.values())

            # Send system metrics for the bars
            await websocket.send_json({
                "event": "telemetry", 
                "data": metrics,
                "consensus": consensus_active
            })
            await asyncio.sleep(2) 
    except WebSocketDisconnect:
        pass

@app.get("/stream")
async def serve_stream():
    """Serves the Multi-Channel Stream Console."""
    target = (WEB_UI_DIR / "stream_console.html").resolve()
    if target.exists():
        return FileResponse(str(target), media_type="text/html")
    return JSONResponse(status_code=404, content={"detail": f"File not found at {target}"})

@app.get("/topology")
async def serve_topology():
    target = (WEB_UI_DIR / "topology_viewer.html").resolve()
    return FileResponse(str(target)) if target.exists() else {"error": "404"}

@app.get("/designer")
async def serve_designer():
    """Serves the Universal Shard (n8nstyle) Manifest Designer."""
    target = (WEB_UI_DIR / "manifest_designer.html").resolve()
    if target.exists():
        return FileResponse(str(target), media_type="text/html")
    return JSONResponse(status_code=404, content={"detail": "Designer HTML not found"})

@app.post("/manifest/create")
async def create_manifest(data: dict):
    """API for the designer to save new cognitive shards."""
    from src.core.base.lifecycle.manifest_repository import ManifestRepository
    from src.core.base.lifecycle.logic_manifest import LogicManifest
    
    repo = ManifestRepository()
    role = data.get("role", "custom_shard")
    manifest = LogicManifest.from_dict(data)
    repo.save_manifest(role, manifest)
    return {"status": "success", "role": role}

# --- File Explorer API (Phase 325) ---

@app.get("/api/files/list")
async def list_files(path: str = "."):
    """Lists files and directories in the workspace."""
    target_path = (WORKSPACE_ROOT / path).resolve()
    # Security: Ensure path is within workspace
    if not str(target_path).startswith(str(WORKSPACE_ROOT)):
        return JSONResponse(status_code=403, content={"error": "Access denied"})
    
    if not target_path.exists():
        return JSONResponse(status_code=404, content={"error": "Path not found"})
    
    items = []
    try:
        for entry in os.scandir(target_path):
            if entry.name.startswith((".", "__")): continue
            items.append({
                "name": entry.name,
                "is_dir": entry.is_dir(),
                "path": str(Path(path) / entry.name).replace("\\", "/")
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
        
    return sorted(items, key=lambda x: (not x["is_dir"], x["name"].lower()))

@app.get("/api/files/read")
async def read_workspace_file(path: str):
    """Reads the content of a file in the workspace."""
    target_path = (WORKSPACE_ROOT / path).resolve()
    if not str(target_path).startswith(str(WORKSPACE_ROOT)):
        return JSONResponse(status_code=403, content={"error": "Access denied"})
    
    if not target_path.is_file():
        return JSONResponse(status_code=404, content={"error": "File not found"})
    
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return {"content": f.read()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# --- WebAuthn / Biometric Auth (Phase 327) ---

@app.get("/api/auth/register/options")
async def get_registration_options(username: str):
    """Generates options for WebAuthn registration."""
    try:
        options = auth_manager.get_registration_options(username)
        return options
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

# --- RDMA Checkpointing (Phase 93) ---

@app.post("/api/resilience/checkpoint")
async def trigger_checkpoint(data: dict):
    """Triggers an RDMA checkpoint of the current swarm state."""
    state_payload = data.get("state", "{}").encode("utf-8")
    checkpoint_id = await checkpoint_manager.create_checkpoint(state_payload)
    if checkpoint_id:
        return {"status": "success", "checkpoint_id": checkpoint_id}
    return JSONResponse(status_code=500, content={"error": "RDMA Checkpoint failed"})

@app.get("/api/resilience/checkpoints/latest")
async def get_latest_checkpoint():
    """Returns metadata for the latest RDMA checkpoint."""
    latest = checkpoint_manager.get_latest_checkpoint()
    if latest:
        return {
            "id": latest.id,
            "timestamp": latest.timestamp,
            "peer_rank": latest.peer_rank,
            "data_size": latest.data_size
        }
    return {"status": "none"}

@app.post("/api/auth/register/verify")
async def verify_registration(username: str, data: dict):
    """Verifies WebAuthn registration response."""
    if auth_manager.verify_registration(username, data):
        return {"status": "success", "message": "Biometric credential registered"}
    return JSONResponse(status_code=400, content={"error": "Verification failed"})

@app.get("/api/auth/login/options")
async def get_login_options(username: str):
    """Generates options for WebAuthn authentication."""
    try:
        options = auth_manager.get_authentication_options(username)
        return options
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.post("/api/auth/login/verify")
async def verify_login(username: str, data: dict):
    """Verifies WebAuthn authentication response."""
    if auth_manager.verify_authentication(username, data):
        return {"status": "success", "token": "mock-jwt-token-v4"}
    return JSONResponse(status_code=401, content={"error": "Authentication failed"})

# 2. ROOT ROUTE
@app.get("/")
async def root():
    target = WEB_UI_DIR / "index.html"
    return FileResponse(str(target)) if target.exists() else {"status": "Active"}

# 3. STATIC MOUNTS LAST
app.mount("/static", StaticFiles(directory=str(WEB_UI_DIR)), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
