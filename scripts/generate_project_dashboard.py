#!/usr/bin/env python3
"""Generate project folders and a dashboard from superpower plan + brainstorm files."""

from __future__ import annotations
import re
from datetime import datetime, timezone
from pathlib import Path

RE_PLAN = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<topic>.+?)(?:-plan|-implementation-plan|_plan)$")

ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / ".github" / "superpower" / "plan"
BRAINSTORM_DIR = ROOT / ".github" / "superpower" / "brainstorm"
OUT_ROOT = ROOT / "docs" / "project"

OUT_ROOT.mkdir(parents=True, exist_ok=True)

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

    topic_key = re.sub(r"\s+", "-", topic.strip())
    topic_key = re.sub(r"[^a-zA-Z0-9_-]", "", topic_key)

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

    # Detect actual code presence (basic heuristic): look for matching module/file names.
    snake = topic_key.replace("-", "_")
    code_found = False
    match_paths = []

    src_root = ROOT / "src"
    if src_root.exists():
        for p in src_root.rglob(f"*{snake}*"):
            if p.is_file() and p.suffix in {".py", ".pyi", ".rs"}:
                code_found = True
                match_paths.append(p.relative_to(ROOT))
                break

    rust_root = ROOT / "rust_core" / "src"
    if not code_found and rust_root.exists():
        for p in rust_root.rglob(f"*{snake}*.rs"):
            code_found = True
            match_paths.append(p.relative_to(ROOT))
            break

    out_file = prj_dir / f"{topic_key}.project.md"
    out_lines = [f"# {topic_key}", "", f"**Project ID:** `{prj_id}`", "", "## Links", "", f"- Plan: `{plan.relative_to(ROOT)}`"]

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

    # Code presence detection
    out_lines += ["", "## Code detection", ""]
    if code_found:
        out_lines += ["- Code detected in:"]
        out_lines += [f"  - `{p}`" for p in match_paths]
    else:
        out_lines += ["- No obvious implementation files found in `src/` or `rust_core/src/`."
                      "  (This is a heuristic; adjust project topic naming if needed.)"]

    if not design_exists:
        out_lines += ["", "## Missing design", "", f"Design file not found: `{design_path.relative_to(ROOT)}`"]

    out_file.write_text("\n".join(out_lines), encoding="utf-8")

    # Detect actual code presence (basic heuristic): look for matching module/file names.
    snake = topic_key.replace("-", "_")
    code_found = False
    match_paths = []

    src_root = ROOT / "src"
    if src_root.exists():
        for p in src_root.rglob(f"*{snake}*"):
            if p.is_file() and p.suffix in {".py", ".pyi", ".rs"}:
                code_found = True
                match_paths.append(p.relative_to(ROOT))
                break

    rust_root = ROOT / "rust_core" / "src"
    if not code_found and rust_root.exists():
        for p in rust_root.rglob(f"*{snake}*.rs"):
            code_found = True
            match_paths.append(p.relative_to(ROOT))
            break

    projects.append({
        "ProjectId": prj_id,
        "Topic": topic_key,
        "Completed": done,
        "Total": total,
        "MissingDesign": not design_exists,
        "CodeFound": code_found,
        "CodeMatches": match_paths,
    })

# Build dashboard
lines = ["# Project Dashboard", "", f"Generated: {datetime.now(timezone.utc).isoformat()}Z", "", "| Project | Completion | Code | Missing Design |", "|--------|------------|------|----------------|"]
for p in projects:
    pct = round((p["Completed"] / p["Total"] * 100) if p["Total"] else 0)
    md = "Yes" if p["MissingDesign"] else "No"
    code = "Yes" if p.get("CodeFound") else "No"
    lines.append(f"| {p['ProjectId']} | {pct}% ({p['Completed']}/{p['Total']}) | {code} | {md} |")

(OUT_ROOT / 'PROJECT_DASHBOARD.md').write_text("\n".join(lines), encoding="utf-8")

print(f"Generated {len(projects)} project folders and dashboard.")
