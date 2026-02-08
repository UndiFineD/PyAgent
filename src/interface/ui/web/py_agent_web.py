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
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Absolute resolution is critical on Windows
WEB_UI_DIR = Path(__file__).resolve().parent

app = FastAPI(title="PyAgent Fleet API")

# 1. SPECIFIC ROUTES FIRST
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

# 2. ROOT ROUTE
@app.get("/")
async def root():
    target = WEB_UI_DIR / "index.html"
    return FileResponse(str(target)) if target.exists() else {"status": "Active"}

# 3. STATIC MOUNTS LAST
app.mount("/static", StaticFiles(directory=str(WEB_UI_DIR)), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
