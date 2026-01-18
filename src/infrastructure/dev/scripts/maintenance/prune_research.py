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


"""Script for pruning large research research files to keep only recent relevant findings."""

from __future__ import annotations
from src.core.base.Version import VERSION
import os

__version__ = VERSION

file_path = r"c:\DEV\PyAgent\docs\IMPROVEMENT_RESEARCH.md"
if os.path.exists(file_path):
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    found_findings_header = False
    found_lessons_header = False

    # We want to keep the main headers but only the first (or last) occurrence of the repeated sections.
    # Actually, let's just keep everything until the first "## 🚀 Recent Autonomous Findings"
    # and then handle the findings and lessons specifically.

    cutoff_idx = -1
    for i, line in enumerate(lines):
        if "## 🚀 Recent Autonomous Findings" in line:
            cutoff_idx = i
            break

    if cutoff_idx != -1:
        new_lines = lines[:cutoff_idx]
        new_lines.append("## 🚀 Recent Autonomous Findings\n\n")

        # Now find the latest findings block
        latest_findings = []
        for i in range(len(lines) - 1, -1, -1):
            if "### Latest Autonomous Scan" in lines[i]:
                # Found the start of the last scan block
                # Scan forward until the next header or end
                for j in range(i, len(lines)):
                    if j > i and ("### " in lines[j] or "## " in lines[j]):
                        break
                    latest_findings.append(lines[j])
                break

        new_lines.extend(latest_findings)

        # Now find lessons
        new_lines.append(
            "\n\n### 🧠 AI Lessons Derived from Deep Shard Analysis (Phase 108)\n"
        )
        unique_lessons = set()
        for line in lines:
            if line.strip().startswith("- Intelligence Shard"):
                unique_lessons.add(line.strip())

        for lesson in sorted(list(unique_lessons)):
            new_lines.append(lesson + "\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Pruned {file_path}")
else:
    print(f"File not found: {file_path}")
