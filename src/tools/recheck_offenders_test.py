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

import json
import os
import subprocess

LINT_RESULTS_PATH = r"c:\Dev\PyAgent\lint_results.json"
PYTHON_PATH = r"c:\Dev\PyAgent\.venv\Scripts\python.exe"

def run_ruff(file_path):
    try:
        res = subprocess.run([PYTHON_PATH, "-m", "ruff", "check", file_path], capture_output=True, text=True)
        return res.stdout
    except Exception:
        return ""

def run_flake8(file_path):
    try:
        res = subprocess.run([PYTHON_PATH, "-m", "flake8", file_path, "--max-line-length=120"], capture_output=True, text=True)
        return res.stdout
    except Exception:
        return ""

def main():
    if not os.path.exists(LINT_RESULTS_PATH):
        print("lint_results.json not found")
        return

    with open(LINT_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # We only re-check the top 20 or so from the OLD list to see progress
    file_issues = []
    for entry in data:
        file_path = entry["file"]
        # Skip files that don't exist anymore or renamed
        if not os.path.exists(file_path):
            continue
            
        print(f"Checking {file_path}...")
        ruff_out = run_ruff(file_path)
        flake_out = run_flake8(file_path)
        
        issues = len([line for line in ruff_out.splitlines() if line.strip()])
        issues += len([line for line in flake_out.splitlines() if line.strip()])
        
        file_issues.append((file_path, issues))

    file_issues.sort(key=lambda x: x[1], reverse=True)

    print("\nUPDATED Top 20 Offending Files:")
    for f, count in file_issues[:20]:
        print(f"{count:4} : {f}")

if __name__ == "__main__":
    main()
