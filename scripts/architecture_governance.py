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
import re
from datetime import date
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Status",
    "## Date",
    "## Owners",
    "## Context",
    "## Decision",
    "## Alternatives considered",
    "## Consequences",
    "## Implementation impact",
    "## Validation and monitoring",
    "## Related links",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _adr_dir(root: Path) -> Path:
    return root / "docs" / "architecture" / "adr"


def _template_path(root: Path) -> Path:
    return _adr_dir(root) / "0001-architecture-decision-record-template.md"


def _adr_files(root: Path) -> list[Path]:
    adr_dir = _adr_dir(root)
    if not adr_dir.exists():
        return []
    return sorted([p for p in adr_dir.glob("*.md") if re.match(r"^\d{4}-.+\.md$", p.name)])


def _slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug or "architecture-decision"


def _validate_numbering(files: list[Path]) -> list[str]:
    issues: list[str] = []
    nums = []
    for p in files:
        m = re.match(r"^(\d{4})-", p.name)
        if not m:
            issues.append(f"Invalid ADR filename: {p.name}")
            continue
        nums.append(int(m.group(1)))

    if not nums:
        return issues

    nums_sorted = sorted(nums)
    for idx in range(1, len(nums_sorted)):
        if nums_sorted[idx] != nums_sorted[idx - 1] + 1:
            issues.append(f"ADR numbering gap or jump around {nums_sorted[idx - 1]:04d} -> {nums_sorted[idx]:04d}")

    if nums_sorted[0] != 1:
        issues.append(f"ADR numbering should start at 0001; found {nums_sorted[0]:04d}")

    return issues


def _validate_sections(files: list[Path]) -> list[str]:
    issues: list[str] = []
    for p in files:
        if p.name.startswith("0001-"):
            # Template is intentionally not an ADR instance.
            continue
        text = p.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                issues.append(f"{p.name}: missing section '{section}'")
    return issues


def validate() -> int:
    root = _repo_root()
    issues: list[str] = []

    template = _template_path(root)
    if not template.exists():
        issues.append(f"Missing ADR template: {template.as_posix()}")

    files = _adr_files(root)
    if not files:
        issues.append("No ADR markdown files found in docs/architecture/adr/")

    issues.extend(_validate_numbering(files))
    issues.extend(_validate_sections(files))

    if issues:
        print("VALIDATION_FAILED")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("VALIDATION_OK")
    print(f"adr_files={len(files)}")
    return 0


def create_adr(title: str, owners: str, status: str) -> int:
    root = _repo_root()
    adr_dir = _adr_dir(root)
    adr_dir.mkdir(parents=True, exist_ok=True)

    files = _adr_files(root)
    nums = []
    for p in files:
        m = re.match(r"^(\d{4})-", p.name)
        if m:
            nums.append(int(m.group(1)))
    next_num = (max(nums) + 1) if nums else 1

    slug = _slugify(title)
    out = adr_dir / f"{next_num:04d}-{slug}.md"
    if out.exists():
        raise SystemExit(f"Refusing to overwrite existing ADR: {out.as_posix()}")

    today = date.today().isoformat()
    content = "\n".join(
        [
            f"# ADR-{next_num:04d} - {title}",
            "",
            "## Status",
            "",
            f"- {status}",
            "",
            "## Date",
            "",
            f"- {today}",
            "",
            "## Owners",
            "",
            f"- {owners}",
            "",
            "## Context",
            "",
            "Describe the problem, constraints, and why this decision is needed now.",
            "",
            "## Decision",
            "",
            "State the chosen option clearly and unambiguously.",
            "",
            "## Alternatives considered",
            "",
            "### Alternative A - Name",
            "",
            "- Summary:",
            "- Why not chosen:",
            "",
            "### Alternative B - Name",
            "",
            "- Summary:",
            "- Why not chosen:",
            "",
            "## Consequences",
            "",
            "### Positive",
            "",
            "- Clear benefit 1",
            "- Clear benefit 2",
            "",
            "### Negative / Trade-offs",
            "",
            "- Cost or complexity 1",
            "- Risk 1",
            "",
            "## Implementation impact",
            "",
            "- Affected components:",
            "- Migration/rollout notes:",
            "- Backward compatibility notes:",
            "",
            "## Validation and monitoring",
            "",
            "- Tests or checks required:",
            "- Runtime signals or metrics to monitor:",
            "- Rollback triggers:",
            "",
            "## Related links",
            "",
            "- Related project artifact(s):",
            "- Related architecture docs:",
            "- Supersedes/Superseded-by (if any):",
            "",
        ]
    )
    out.write_text(content, encoding="utf-8")
    print(f"CREATED {out.as_posix()}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Govern docs/architecture and ADR updates.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="Validate ADR naming/numbering/required sections.")

    create_parser = sub.add_parser("create", help="Create next ADR file from template conventions.")
    create_parser.add_argument("--title", required=True)
    create_parser.add_argument("--owners", default="TBD")
    create_parser.add_argument("--status", default="Proposed")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.cmd == "validate":
        return validate()
    if args.cmd == "create":
        return create_adr(title=args.title, owners=args.owners, status=args.status)

    parser.error(f"Unknown command: {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
