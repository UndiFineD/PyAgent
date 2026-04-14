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
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PRIORITY_RE = re.compile(r"-\s*priority_score:\s*(-?\d+)", re.IGNORECASE)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _parse_priority(markdown: str) -> int:
    match = PRIORITY_RE.search(markdown)
    if match is None:
        return 0
    return int(match.group(1))


def _cluster_by_source(rows: list[dict[str, Any]], min_priority: int) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        priority = _parse_priority(str(row.get("template_markdown", "")))
        if priority < min_priority:
            continue
        source_file = str(row.get("source_file", ""))
        if not source_file:
            continue
        grouped[source_file].append(
            {
                "legacy_id": str(row.get("idea_id", "")),
                "title": str(row.get("title", "")),
                "archetype": str(row.get("archetype", "")),
                "priority": priority,
            }
        )

    for ideas in grouped.values():
        ideas.sort(key=lambda item: (-item["priority"], item["legacy_id"]))
    return grouped


def propose_merges(
    input_path: Path,
    output_json: Path,
    output_markdown: Path,
    min_group_size: int,
    max_group_size: int,
    min_priority: int,
) -> dict[str, Any]:
    rows = _read_jsonl(input_path)
    grouped = _cluster_by_source(rows, min_priority=min_priority)

    proposals: list[dict[str, Any]] = []
    for source_file, ideas in sorted(grouped.items()):
        if len(ideas) < min_group_size:
            continue

        selected = ideas[:max_group_size]
        archetypes = [item["archetype"] for item in selected]
        titles = [item["title"] for item in selected]

        proposals.append(
            {
                "cluster_id": f"cluster-{len(proposals) + 1:05d}",
                "source_file": source_file,
                "member_count": len(selected),
                "member_legacy_ids": [item["legacy_id"] for item in selected],
                "average_priority": round(sum(item["priority"] for item in selected) / len(selected), 2),
                "recommended_merge_title": f"{Path(source_file).stem} consolidated modernization",
                "rationale": (
                    "Ideas share the same source file and have compatible scopes. "
                    "Merge into one implementation plan to reduce duplication."
                ),
                "archetypes": archetypes,
                "titles": titles,
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": input_path.as_posix(),
        "proposal_count": len(proposals),
        "proposals": proposals,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines: list[str] = []
    lines.append("# Legacy Idea Merge Proposals")
    lines.append("")
    lines.append(f"Generated: {payload['generated_at']}")
    lines.append(f"Input: `{input_path.as_posix()}`")
    lines.append(f"Total proposals: {payload['proposal_count']}")
    lines.append("")

    for item in proposals:
        lines.append(f"## {item['cluster_id']}")
        lines.append(f"- Source file: `{item['source_file']}`")
        lines.append(f"- Member count: {item['member_count']}")
        lines.append(f"- Average priority: {item['average_priority']}")
        lines.append(f"- Recommended merge title: {item['recommended_merge_title']}")
        lines.append(f"- Legacy IDs: {', '.join(item['member_legacy_ids'])}")
        lines.append(f"- Archetypes: {', '.join(item['archetypes'])}")
        lines.append(f"- Rationale: {item['rationale']}")
        lines.append("")

    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create merge proposals from legacy generated ideas.")
    parser.add_argument("--input", required=True, help="Input legacy ideas jsonl file")
    parser.add_argument(
        "--output-json",
        default="docs/project/legacy_idea_merge_proposals.json",
        help="Output proposals JSON",
    )
    parser.add_argument(
        "--output-markdown",
        default="docs/project/legacy_idea_merge_proposals.md",
        help="Output human-readable proposals markdown",
    )
    parser.add_argument("--min-group-size", type=int, default=2, help="Minimum ideas per source file for proposal")
    parser.add_argument("--max-group-size", type=int, default=4, help="Maximum ideas included in each proposal")
    parser.add_argument("--min-priority", type=int, default=2, help="Minimum priority score for clustering")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    payload = propose_merges(
        input_path=Path(args.input).resolve(),
        output_json=Path(args.output_json).resolve(),
        output_markdown=Path(args.output_markdown).resolve(),
        min_group_size=max(2, args.min_group_size),
        max_group_size=max(2, args.max_group_size),
        min_priority=args.min_priority,
    )

    print(
        "LEGACY_IDEA_MERGE_PROPOSALS_OK "
        f"proposals={payload['proposal_count']} "
        f"json={Path(args.output_json).resolve()} "
        f"markdown={Path(args.output_markdown).resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
