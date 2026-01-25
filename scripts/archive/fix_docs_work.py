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
"""
Fix Docs Work module.
"""

import os

files = [
    "FLEET_AUTO_DOC.md",
    "IMPROVEMENT_RESEARCH.md",
    "OPTIONAL_TOOLS.md",
    "PHASE_1_RUST_PROGRESS.md",
    "PHASE_2_SECURITY_HARDENING.md",
    "PHASE_3_DEEP_OPTIMIZATION.md",
    "PROGRESS_DASHBOARD.md",
    "PROGRESS_REPORT.md",
    "ROADMAP_PHASES.md",
    "RUST_Ready.md"
]

root = r"c:\DEV\PyAgent\docs\work"

for f in files:
    old = os.path.join(root, f)
    new = os.path.join(root, f.lower())
    if os.path.exists(old):
        temp = old + ".tmp"
        os.rename(old, temp)
        os.rename(temp, new)
        print(f"Renamed {f} to {f.lower()}")