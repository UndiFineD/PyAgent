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
from pathlib import Path


def ensure_file(path: Path, header: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(header)


def main():
    root = Path(os.getcwd()) / "project"
    docs = {
        "governance.md": "# Governance\n\nRoles and RACI matrix go here.\n",
        "milestones.md": "# Milestones\n\n- Deliverable - Date\n",
        "budget.md": "# Budget\n\nExpense tracker placeholder.\n",
        "risk.md": "# Risk\n\nRisk matrix template.\n",
    }
    for fname, header in docs.items():
        ensure_file(root / fname, header)

    dirs = ["metrics", "standups", "incidents", "templates"]
    for d in dirs:
        dpath = root / d
        dpath.mkdir(parents=True, exist_ok=True)

    # add sample template placeholder
    sample = root / "templates" / "status_email.md"
    if not sample.exists():
        sample.write_text("# Status Email\n\n- Date: {{DATE}}\n- Highlights:\n- Blockers:\n")


if __name__ == "__main__":
    main()
