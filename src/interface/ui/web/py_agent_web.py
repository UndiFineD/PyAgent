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
import uuid
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from src.tools.download_agent.core import DownloadAgent
from src.tools.download_agent.models import DownloadConfig
from src.infrastructure.security.auth.webauthn_manager import WebAuthnManager
from src.infrastructure.swarm.resilience.checkpoint_manager import CheckpointManager

# VOYAGER STABILITY: Fix for ZeroMQ on Windows Proactor Loop
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logger = logging.getLogger(__name__)

# Absolute resolution is critical on Windows
WEB_UI_DIR = Path(__file__).resolve().parent
# Workspace Root is 4 levels up: web -> ui -> interface -> src -> root
WORKSPACE_ROOT = WEB_UI_DIR.parent.parent.parent.parent
LOGS_DIR = WORKSPACE_ROOT / "data" / "logs"

# Global Fleet Instance
fleet_instance = None
auth_manager = WebAuthnManager()
checkpoint_manager = CheckpointManager(rank=0, world_size=1)  # Default for web proxy

@asynccontextmanager
async def lifespan(app: FastAPI):
    global fleet_instance
    try:
        from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
        fleet_instance = FleetManager(str(WORKSPACE_ROOT))
        logger.info(f"FleetManager initialized at {WORKSPACE_ROOT}")
    except Exception as e:
        logger.error(f"Failed to initialize FleetManager: {e}")
    yield
    # Cleanup logic here if needed

app = FastAPI(title="PyAgent Fleet API", lifespan=lifespan)


# Authentication Endpoints (Phase 327: Biometric Hardware Keys)
@app.post("/api/auth/register/options")
async def registration_options(request: Request):
    data = await request.json()
    username = data.get("username", "admin")
    options = auth_manager.generate_registration_options(username)
    # Store for verification
    auth_manager.last_challenge = options["challenge"]
    return options


@app.post("/api/auth/register/verify")
async def verify_registration(request: Request):
    data = await request.json()
    result = auth_manager.verify_registration(data.get("username", "admin"), data)
    return {"status": "success" if result else "error"}


@app.post("/api/auth/login/options")
async def authentication_options(request: Request):
    data = await request.json()
    username = data.get("username", "admin")
    options = auth_manager.generate_authentication_options(username)
    # Store for verification
    auth_manager.last_challenge = options["challenge"]
    return options


@app.post("/api/auth/login/verify")
async def verify_authentication(request: Request):
    data = await request.json()
    result = auth_manager.verify_authentication(data.get("username", "admin"), data)
    return {"status": "authenticated" if result else "denied"}


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
            "network": round(abs(stats.get("network_io", {}).get("bytes_sent", 0) / 1024 / 1024) % 100, 1),
            "temp": round(stats.get("temp", 0), 1),
            "gpu": round(stats.get("gpu", {}).get("usage", 0), 1)
        }

    try:
        import psutil
        return {
            "cpu": round(psutil.cpu_percent(), 1),
            "mem": round(psutil.virtual_memory().percent, 1),
            "storage": round(psutil.disk_usage("/").percent, 1),
            "network": 0.0,
            "temp": 0.0,
            "gpu": 0.0
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
                        "id": data.get("task_id") or str(uuid.uuid4())[:8],
                        "parent_id": data.get("parent_id") or data.get("context", {}).get("task_id"),
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

@app.get("/api/infection-guard")
async def get_infection_guard_events():
    """Returns the latest blocked events from Infection Guard."""
    global fleet_instance
    if fleet_instance and hasattr(fleet_instance, "infection_guard"):
        return fleet_instance.infection_guard.get_blocked_events()
    return []

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
            if entry.name.startswith((".", "__")):
                continue
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


# --- External Automation (n8n) Integration ---

@app.post("/api/n8n/execute")
async def n8n_execute(data: dict):
    """
    Bi-directional n8n Orchestration (Phase 322).
    Acts as an intelligent decision node for external workflows.
    """
    global fleet_instance
    if not fleet_instance:
        return JSONResponse(status_code=503, content={"error": "Fleet not initialized"})

    prompt = data.get("prompt", "")
    payload = data.get("data", {}) # Data for the agent to process

    # Combine data into prompt if present
    full_command = prompt
    if payload:
        full_command += f"\n\nData Context:\n{json.dumps(payload, indent=2)}"

    try:
        logger.info(f"n8n: Received automation request: {prompt[:50]}")
        result = await fleet_instance.handle_user_command(full_command)
        
        return {
            "status": "success",
            "output": result.get("result", ""),
            "metadata": {
                "agent": result.get("agent"),
                "timestamp": time.time()
            }
        }
    except Exception as e:
        logger.error(f"n8n: Execution error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


# --- Swarm Observability (Pillar 9) ---

@app.get("/api/observability/traces")
async def get_swarm_traces():
    """
    Returns the Global Trace Synthesis for the swarm (Pillar 9).
    Shows task lineage across the entire constellation.
    """
    trace_path = WORKSPACE_ROOT / "data" / "logs" / "reasoning_chains.jsonl"
    if not trace_path.exists():
        return {"traces": []}
    
    traces = []
    try:
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    traces.append(json.loads(line))
        
        # Limit to last 50 traces for visualization performance
        return {"traces": traces[-50:]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/observability/topology")
async def get_observability_topology():
    """
    Pillar 8: Real-Time Topology Mapper.
    Returns 3D (2D projected) node locations and data 'teleportation' routes.
    """
    topo_path = WORKSPACE_ROOT / "data" / "logs" / "topology.json"
    if not topo_path.exists():
        return {"nodes": [], "edges": []}
    
    with open(topo_path, "r") as f:
        return json.load(f)


@app.post("/api/tools/download")
async def trigger_download(request: Request):
    """
    Triggers a download via the DownloadAgent.
    """
    data = await request.json()
    url = data.get("url")
    if not url:
        return JSONResponse(status_code=400, content={"error": "URL required"})
    
    config = DownloadConfig(
        urls_file="",
        dry_run=data.get("dry_run", False),
        verbose=True,
        base_dir=str(WORKSPACE_ROOT)
    )
    agent = DownloadAgent(config)
    result = await asyncio.to_thread(agent.process_url, url)
    
    # Save to history
    history_path = WORKSPACE_ROOT / "temp" / "downloads.json"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    await asyncio.to_thread(agent.save_results, [result], str(history_path))
    
    return {"status": "success" if result.success else "failed", "result": result.__dict__}


# 2. ROOT ROUTE
@app.get("/")
async def root():
    target = WEB_UI_DIR / "index.html"
    return FileResponse(str(target)) if target.exists() else {"status": "Active"}

# 3. STATIC MOUNTS LAST
app.mount("/static", StaticFiles(directory=str(WEB_UI_DIR)), name="static")

if __name__ == "__main__":
    uvicorn.run("src.interface.ui.web.py_agent_web:app", host="0.0.0.0", port=8000, reload=True)
