#!/usr/bin/env python3
"""Validate that all projects in docs/project/ are fully implemented.

This checks each project folder for:
- presence of plan.md
- presence of brainstorm.md
- all checklist items in plan.md are completed (checked)
- optional: indicates whether project currently has any unchecked tasks

This script is intended to help confirm the agent-based project tracking system is
keeping projects in a "fully implemented" state.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_ROOT = ROOT / "docs" / "project"

CHECKBOX_RE = re.compile(r"^[\s\-\*]+\[([ xX])\]")


def _check_plan(path: Path) -> Tuple[int, int, List[str]]:
    """Return (total, done, missing_lines) for checkboxes in plan."""
    if not path.exists():
        return 0, 0, [f"MISSING: {path}"]

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    total = 0
    done = 0
    missing: List[str] = []
    for line in lines:
        m = CHECKBOX_RE.match(line)
        if not m:
            continue
        total += 1
        if m.group(1).strip().lower() == "x":
            done += 1
        else:
            missing.append(line.strip())
    return total, done, missing


def main() -> None:
    project_dirs = sorted(d for d in PROJECTS_ROOT.iterdir() if d.is_dir() and d.name.startswith("prj"))

    overall_ok = True

    for prj in project_dirs:
        plan = prj / "plan.md"
        brainstorm = prj / "brainstorm.md"

        total, done, missing = _check_plan(plan)
        has_brainstorm = brainstorm.exists()

        status = []
        if not plan.exists():
            status.append("MISSING plan.md")
        if not has_brainstorm:
            status.append("MISSING brainstorm.md")
        if total and done < total:
            status.append(f"{len(missing)} unchecked tasks")

        if status:
            overall_ok = False
            print(f"[WARN] {prj.name}: " + "; ".join(status))
            if missing:
                for line in missing:
                    print(f"    - {line}")
        else:
            print(f"[OK]   {prj.name}: fully implemented")

    if not overall_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
