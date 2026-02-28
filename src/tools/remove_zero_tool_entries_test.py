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
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUT = ROOT / "lint_results.json"
BACKUP = ROOT / "lint_results.json.post_filter.bak"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

# Backup
with open(BACKUP, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

original_files = len(data)
removed_tool_entries = 0
removed_files = 0

filtered = []
for entry in data:
    # Copy to avoid mutating original structure
    e = dict(entry)
    tools = ["flake8", "ruff", "mypy"]
    for t in tools:
        if t in e:
            if isinstance(e[t], dict):
                tool = e[t]
                exit_code = tool.get("exit_code")
                stdout = (tool.get("stdout") or "").strip()
                # Consider success cases: exit_code==0 OR stdout indicates success
                success = False
                if exit_code == 0:
                    success = True
                elif isinstance(stdout, str):
                    if stdout.startswith("Success: no issues found") or stdout.startswith("All checks passed"):
                        success = True

                if success:
                    try:
                        del e[t]
                        removed_tool_entries += 1
                    except Exception:
                        pass

    # If no tool keys remain, skip this file
    if not any(k in e for k in tools):
        removed_files += 1
        continue
    filtered.append(e)

with open(INPUT, "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2)

print(f"Original file entries: {original_files}")
print(f"Files removed entirely: {removed_files}")
print(f"Individual tool entries removed: {removed_tool_entries}")
print(f"Remaining file entries: {len(filtered)}")
print(f"Backup of pre-change results saved to: {BACKUP}")
