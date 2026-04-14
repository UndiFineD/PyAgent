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
"""Generate governance template files under project/templates/.

Usage:
    python scripts/GeneratePmTemplates.py [--out project/templates]
"""

from __future__ import annotations

import argparse
# import os
from pathlib import Path

_TEMPLATES: dict[str, str] = {
    "standup.md": """\
# Daily Stand-up — {{date}}

**What did I do yesterday?**
-

**What will I do today?**
-

**Blockers?**
- None
""",
    "incident.md": """\
# Incident Report — {{incident_id}}

**Date:** {{date}}
**Severity:** {{severity}}
**Summary:**

## Timeline

| Time | Event |
|------|-------|
| | |

## Root Cause

## Resolution

## Action Items

| Item | Owner | Due |
|------|-------|-----|
| | | |
""",
    "sprint_review.md": """\
# Sprint Review — Sprint {{sprint_number}}

**Dates:** {{start_date}} – {{end_date}}

## Completed Stories

| Story | Points |
|-------|--------|
| | |

## Velocity

- Planned: {{planned_points}} pts
- Completed: {{completed_points}} pts
- Health: {{health}}

## Next Sprint Goals

1.
""",
    "risk_matrix.md": """\
# Risk Matrix — {{project}}

| Title | Probability | Impact | Mitigation |
|-------|-------------|--------|------------|
| Example risk | medium | high | Add automated tests |
""",
}


def generate(out_dir: str) -> list[str]:
    """Write template files to *out_dir*; return list of created paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for name, content in _TEMPLATES.items():
        target = out / name
        target.write_text(content, encoding="utf-8")
        created.append(str(target))
    return created


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Generate PM governance templates")
    parser.add_argument("--out", default="project/templates", help="Output directory")
    args = parser.parse_args()
    created = generate(args.out)
    for path in created:
        print(f"  created: {path}")
    print(f"Generated {len(created)} template(s) in {args.out}")


if __name__ == "__main__":
    main()
