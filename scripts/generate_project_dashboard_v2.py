#!/usr/bin/env python3
"""Generate project folders and a dashboard from superpower plan + brainstorm files.

This is a more robust successor to the original generator. It:
- Keeps the same project folder + dashboard structure.
- Improves implementation detection by searching common repo locations and
  matching multiple token variants.
- Avoids duplicated code detection logic.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Set

RE_PLAN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<topic>.+?)(?:-plan|-implementation-plan|_plan)$"
)

ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / ".github" / "superpower" / "plan"
BRAINSTORM_DIR = ROOT / ".github" / "superpower" / "brainstorm"
OUT_ROOT = ROOT / "docs" / "project"

OUT_ROOT.mkdir(parents=True, exist_ok=True)


def _normalize_topic_key(topic: str) -> str:
    """Normalize a topic string into a stable file-system friendly key."""

    key = re.sub(r"\s+", "-", topic.strip())
    key = re.sub(r"[^a-zA-Z0-9_-]", "", key)
    return key


def _code_search_candidates(topic_key: str) -> Set[str]:
    """Generate a set of search tokens used to detect implementation files."""

    snake = topic_key.replace("-", "_")
    parts = re.split(r"[-_]+", topic_key)

    candidates: Set[str] = {topic_key, snake}
    candidates.update(parts)

    # Common two-word variants like "async-runtime" -> "async_runtime".
    if len(parts) > 1:
        candidates.add("-".join(parts[:2]))
        candidates.add("_".join(parts[:2]))

    return {c for c in candidates if c}


def _find_code_files(topic_key: str) -> List[Path]:
    """Return a list of repository paths that appear to implement a given topic."""

    candidates = _code_search_candidates(topic_key)

    # Common locations where work is often found.
    search_dirs = [ROOT, ROOT / "scripts", ROOT / "tests"]
    extensions = [".py", ".pyi", ".rs"]

    matches: Set[Path] = set()

    # Exact file matches (fast path for straightforward topic names).
    for base in search_dirs:
        if not base.exists():
            continue
        for cand in candidates:
            for ext in extensions:
                p = base / f"{cand}{ext}"
                if p.exists():
                    matches.add(p.relative_to(ROOT))

    # Fallback: scan key source trees for file names containing a candidate token.
    for tree in [ROOT / "src", ROOT / "rust_core" / "src"]:
        if not tree.exists():
            continue
        for ext in extensions:
            for p in tree.rglob(f"*{ext}"):
                name = p.stem.lower()
                if any(cand.lower() in name for cand in candidates):
                    matches.add(p.relative_to(ROOT))

    return sorted(matches)


plan_files = sorted(PLAN_DIR.glob("*.md"))
projects = []

for idx, plan in enumerate(plan_files, start=1):
    base = plan.stem
    m = RE_PLAN.match(base)
    if m:
        date = m.group("date")
        topic = m.group("topic")
    else:
        date = ""
        topic = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", base)
        topic = re.sub(r"(-plan|-implementation-plan|_plan)$", "", topic)

    topic_key = _normalize_topic_key(topic)

    prj_id = f"prj{idx:03d}-{topic_key}"
    prj_dir = OUT_ROOT / prj_id
    prj_dir.mkdir(parents=True, exist_ok=True)

    design_filename = f"{date}-{topic_key}-design.md" if date else f"{topic_key}-design.md"
    design_path = BRAINSTORM_DIR / design_filename
    design_exists = design_path.exists()

    text = plan.read_text(encoding="utf-8")
    lines = [l.rstrip() for l in text.splitlines() if re.match(r"^[\s\-*]+\[[ xX]\]", l)]
    total = len(lines)
    done = len([l for l in lines if re.match(r"^[\s\-*]+\[\s*[xX]\s*\]", l)])

    match_paths = _find_code_files(topic_key)
    code_found = bool(match_paths)

    out_file = prj_dir / f"{topic_key}.project.md"
    out_lines = [
        f"# {topic_key}",
        "",
        f"**Project ID:** `{prj_id}`",
        "",
        "## Links",
        "",
        f"- Plan: `{plan.relative_to(ROOT)}`",
    ]

    if design_exists:
        out_lines.append(f"- Design: `{design_path.relative_to(ROOT)}`")
    else:
        out_lines.append(f"- Design: **MISSING** (`{design_path.relative_to(ROOT)}`)")

    out_lines += ["", "## Tasks", ""]
    if total > 0:
        out_lines.extend(lines)
    else:
        out_lines.append("_No checkbox tasks found in the plan file._")

    out_lines += ["", "## Status", "", f"{done} of {total} tasks completed"]

    out_lines += ["", "## Code detection", ""]
    if code_found:
        out_lines += ["- Code detected in:"]
        out_lines += [f"  - `{p}`" for p in match_paths]
    else:
        out_lines += [
            "- No obvious implementation files found in `src/`, `rust_core/src/`, or repository root.",
            "  (This is a heuristic; adjust project topic naming if needed.)",
        ]

    if not design_exists:
        out_lines += [
            "",
            "## Missing design",
            "",
            f"Design file not found: `{design_path.relative_to(ROOT)}`",
        ]

    out_file.write_text("\n".join(out_lines), encoding="utf-8")

    projects.append(
        {
            "ProjectId": prj_id,
            "Topic": topic_key,
            "Completed": done,
            "Total": total,
            "MissingDesign": not design_exists,
            "CodeFound": code_found,
            "CodeMatches": match_paths,
        }
    )

# Build dashboard
lines = [
    "# Project Dashboard",
    "",
    f"Generated: {datetime.now(timezone.utc).isoformat()}Z",
    "",
    "| Project | Completion | Code | Missing Design |",
    "|--------|------------|------|----------------|",
]
for p in projects:
    pct = round((p["Completed"] / p["Total"] * 100) if p["Total"] else 0)
    md = "Yes" if p["MissingDesign"] else "No"
    code = "Yes" if p.get("CodeFound") else "No"
    lines.append(
        f"| {p['ProjectId']} | {pct}% ({p['Completed']}/{p['Total']}) | {code} | {md} |"
    )

(OUT_ROOT / "PROJECT_DASHBOARD.md").write_text("\n".join(lines), encoding="utf-8")

print(f"Generated {len(projects)} project folders and dashboard.")
