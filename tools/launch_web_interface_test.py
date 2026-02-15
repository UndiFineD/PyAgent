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

import subprocess
import time
import webbrowser
import os
import sys
from pathlib import Path

def launch():
    print("🚀 Launching PyAgent Web Interface & Voyager Discovery...")
    
    # Get workspace root
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    
    # 1. Start the Dashboard Server (FastAPI + Voyager)
    server_path = "src/interface/ui/gui/dashboard_server.py"
    print(f"📡 Starting Dashboard Server: {server_path}")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    
    process = subprocess.Popen(
        [sys.executable, server_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env
    )
    
    # Wait for server to be ready
    print("⏳ Waiting for server to initialize...")
    time.sleep(3)
    
    # 2. Open the browser
    url = "http://localhost:8000"
    print(f"🌍 Opening Web UI at {url}")
    webbrowser.open(url)
    
    print("\n✅ System Online.")
    print("Press Ctrl+C to stop the server.")
    
    try:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(f"[Server] {line.strip()}")
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        process.terminate()

if __name__ == "__main__":
    launch()
