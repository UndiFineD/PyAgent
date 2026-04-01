#!/usr/bin/env python3
"""Register prj0000113 as Released."""

import json
from pathlib import Path

projects_file = Path("data/projects.json")
kanban_file = Path("docs/project/kanban.json")

projects = json.loads(projects_file.read_text())
kanban = json.loads(kanban_file.read_text())

new_project = {
    "id": "prj0000113",
    "name": "legacy-idea-batch-generator",
    "lane": "Released",
    "summary": "Generate, propose merges, and promote legacy ideas from PyAgent.3.7.0 codebase. Add shared parallel agent register and CLI for atomic work coordination.",
    "branch": "merged",
    "pr": "#268",
    "priority": "P2",
    "budget_tier": "M",
    "tags": ["ideas", "legacy-generation", "parallel-coordination", "workflow-tooling"],
    "created": "2026-04-01",
    "updated": "2026-04-01",
}

projects.insert(0, new_project)
kanban["projects"].insert(0, {
    "id": new_project["id"],
    "name": new_project["name"],
    "lane": "Released",
    "summary": new_project["summary"],
    "tags": new_project["tags"],
})

projects_file.write_text(json.dumps(projects, indent=2, ensure_ascii=False) + "\n")
kanban_file.write_text(json.dumps(kanban, indent=2, ensure_ascii=False) + "\n")

print(f"✓ Added prj0000113 to projects.json and kanban.json")
