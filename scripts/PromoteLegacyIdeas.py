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

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IDEA_ID_RE = re.compile(r"idea(\d{6})", re.IGNORECASE)
PRIORITY_RE = re.compile(r"-\s*priority_score:\s*(-?\d+)", re.IGNORECASE)
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Candidate:
    """Represents one promotable legacy-generated idea candidate."""

    legacy_id: str
    source_file: str
    archetype: str
    title: str
    priority: int
    template_markdown: str


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "idea"


def _parse_priority(markdown: str) -> int:
    match = PRIORITY_RE.search(markdown)
    if match is None:
        return 0
    return int(match.group(1))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _find_next_id(ideas_dir: Path, archive_dir: Path) -> int:
    ids: list[int] = []
    for root in (ideas_dir, archive_dir):
        if not root.exists():
            continue
        for path in root.glob("idea*.md"):
            match = IDEA_ID_RE.search(path.name)
            if match:
                ids.append(int(match.group(1)))
    return (max(ids) + 1) if ids else 1


def _load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"promoted_legacy_ids": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _replace_heading(markdown: str, new_heading: str) -> str:
    if HEADING_RE.search(markdown):
        return HEADING_RE.sub(f"# {new_heading}", markdown, count=1)
    return f"# {new_heading}\n\n{markdown.strip()}\n"


def _collect_candidates(rows: list[dict[str, Any]], min_priority: int) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in rows:
        markdown = str(row.get("template_markdown", ""))
        priority = _parse_priority(markdown)
        if priority < min_priority:
            continue
        candidates.append(
            Candidate(
                legacy_id=str(row.get("idea_id", "")),
                source_file=str(row.get("source_file", "")),
                archetype=str(row.get("archetype", "")),
                title=str(row.get("title", "")),
                priority=priority,
                template_markdown=markdown,
            )
        )

    candidates.sort(key=lambda item: (-item.priority, item.source_file, item.archetype, item.legacy_id))
    return candidates


def promote(
    input_path: Path,
    ideas_dir: Path,
    archive_dir: Path,
    state_path: Path,
    top_n: int,
    min_priority: int,
    max_per_source: int,
    manifest_path: Path,
) -> dict[str, Any]:
    rows = _read_jsonl(input_path)
    state = _load_state(state_path)
    promoted_ids: set[str] = set(state.get("promoted_legacy_ids", []))

    candidates = _collect_candidates(rows, min_priority=min_priority)

    ideas_dir.mkdir(parents=True, exist_ok=True)
    next_id = _find_next_id(ideas_dir, archive_dir)

    per_source_count: dict[str, int] = {}
    promoted: list[dict[str, Any]] = []

    for candidate in candidates:
        if len(promoted) >= top_n:
            break
        if candidate.legacy_id in promoted_ids:
            continue

        count = per_source_count.get(candidate.source_file, 0)
        if count >= max_per_source:
            continue

        idea_number = f"idea{next_id:06d}"
        title_slug = _slugify(candidate.title)
        filename = f"{idea_number}-{title_slug}.md"
        output_path = ideas_dir / filename

        heading = f"{idea_number} - {candidate.title}"
        content = _replace_heading(candidate.template_markdown, heading)
        output_path.write_text(content, encoding="utf-8")

        promoted.append(
            {
                "idea_id": idea_number,
                "file": output_path.as_posix(),
                "legacy_id": candidate.legacy_id,
                "source_file": candidate.source_file,
                "priority": candidate.priority,
            }
        )

        promoted_ids.add(candidate.legacy_id)
        per_source_count[candidate.source_file] = count + 1
        next_id += 1

    state["promoted_legacy_ids"] = sorted(promoted_ids)
    _save_state(state_path, state)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": input_path.as_posix(),
        "top_n": top_n,
        "min_priority": min_priority,
        "max_per_source": max_per_source,
        "selected_count": len(promoted),
        "selected": promoted,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return manifest


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Promote legacy generated ideas into docs/project/ideas markdown files."
    )
    parser.add_argument("--input", required=True, help="Input legacy ideas jsonl file")
    parser.add_argument("--ideas-dir", default="docs/project/ideas", help="Ideas output directory")
    parser.add_argument("--archive-dir", default="docs/project/ideas/archive", help="Ideas archive directory")
    parser.add_argument(
        "--state-file",
        default="docs/project/legacy_ideas_promoted_state.json",
        help="Promotion state file for idempotent reruns",
    )
    parser.add_argument(
        "--manifest",
        default="docs/project/legacy_ideas_promotion.manifest.json",
        help="Promotion manifest",
    )
    parser.add_argument("--top-n", type=int, default=100, help="Maximum ideas to promote")
    parser.add_argument("--min-priority", type=int, default=2, help="Minimum priority score to promote")
    parser.add_argument("--max-per-source", type=int, default=1, help="Maximum promotions per source file")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    manifest = promote(
        input_path=Path(args.input).resolve(),
        ideas_dir=Path(args.ideas_dir).resolve(),
        archive_dir=Path(args.archive_dir).resolve(),
        state_path=Path(args.state_file).resolve(),
        top_n=max(0, args.top_n),
        min_priority=args.min_priority,
        max_per_source=max(1, args.max_per_source),
        manifest_path=Path(args.manifest).resolve(),
    )

    print(
        "LEGACY_IDEA_PROMOTION_OK "
        f"selected={manifest['selected_count']} "
        f"manifest={Path(args.manifest).resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
