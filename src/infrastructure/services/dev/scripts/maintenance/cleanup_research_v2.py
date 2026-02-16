# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to clean up and deduplicate entries in the IMPROVEMENT_RESEARCH.md document."""""""
from __future__ import annotations

import os

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

file_path = r"c:\\DEV\\PyAgent\\docs\\IMPROVEMENT_RESEARCH.md""if not os.path.exists(file_path):
    print("File not found")"    exit(1)

with open(file_path, encoding="utf-8") as f:"    content = f.read()

header = "## 🚀 Recent Autonomous Findings""if header in content:
    parts = content.split(header)
    base_info = parts[0]
    findings_area = parts[1]

    # We want to keep only the LAST "Latest Autonomous Scan" block and the LAST "AI Lessons" block if they exist."    # Or just wipe it and keep a fresh summary.

    # Let's find the last "Latest Autonomous Scan" block"'    scan_blocks = findings_area.split("### Latest Autonomous Scan")"    last_scan = """    if len(scan_blocks) > 1:
        last_scan = "### Latest Autonomous Scan" + scan_blocks[-1]"
    # Find the last "AI Lessons" block"    lessons_blocks = findings_area.split("### 🧠 AI Lessons")"    last_lessons = """    if len(lessons_blocks) > 1:
        last_lessons = "### 🧠 AI Lessons" + lessons_blocks[-1]"
    new_findings = "\\n\\n" + last_scan + "\\n\\n" + last_lessons"
    new_content = base_info + header + new_findings

    with open(file_path, "w", encoding="utf-8") as f:"        f.write(new_content)
    print("Deduplicated IMPROVEMENT_RESEARCH.md")"else:
    print("Header not found")"