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

import os

AGENTS_DIR = os.path.join(os.getcwd(), "data", "agents")
EXCLUDE = {
    "dashboard", "firewall", "javascript", "kubernetes", "management", 
    "monitoring", "networking", "orchestrator", "performance", "powershell",
    "production", "profiling", "provisioning", "reasoning", "reflection",
    "regression", "resilience", "scheduler", "scripting", "security",
    "simulation", "strategist", "supervisor", "synthesis", "telemetry",
    "terraform", "visualizer", "workload", "workspace", "architect", "benchmark", 
    "compliance", "middleware", "classifier", "controller", "department"
}

def find_candidates():
    if not os.path.exists(AGENTS_DIR):
        print(f"Agents dir not found: {AGENTS_DIR}")
        return

    print(f"Scanning {AGENTS_DIR}")
    for name in os.listdir(AGENTS_DIR):
        path = os.path.join(AGENTS_DIR, name)
        if not os.path.isdir(path):
            continue
            
        # Heuristic: no underscores, length > 8, not in exclude list
        if "_" not in name and len(name) > 8 and name not in EXCLUDE:
            print(f"Candidate: {name}")

if __name__ == "__main__":
    find_candidates()
