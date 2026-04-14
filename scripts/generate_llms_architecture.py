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

"""Generate llms-architecture.txt by consolidating docs/architecture content.

This script is intended to provide a stable, deterministic context file that
agents can use as input for reasoning or prompting. It collapses the markdown
files under `docs/architecture/` (excluding `archive/` and `adr/`) into a single
text file that can be consumed by an LLM.

Usage:
    python scripts/generate_llms_architecture.py --output project/llms-architecture.txt

It is safe to run repeatedly; output is deterministic and always rewrites the
same file.
"""

from __future__ import annotations

import argparse
import pathlib


def _discover_architecture_docs(root: pathlib.Path) -> list[pathlib.Path]:
    """Find markdown files under docs/architecture.

    Includes:
    - `docs/architecture/Architecture.md` (only its pre-generated portion)
    - files under `docs/architecture/adr/` (e.g., ADR templates)
    - other top-level architecture docs

    Excludes:
    - `docs/architecture/archive/` (deep dive archives)
    - the generated section of Architecture.md (to avoid recursion)
    """
    base = root / "docs" / "architecture"
    files: list[pathlib.Path] = []

    for path in sorted(base.rglob("*.md")):
        # Skip archive folder.
        if "archive" in path.parts:
            continue
        # Skip generated output files (this script's own output and similar).
        if path.name.endswith(".generated.md"):
            continue
        # Include ADR files.
        if "adr" in path.parts:
            files.append(path)
            continue
        # Include Architecture.md, but it will be rendered only up to the marker.
        files.append(path)

    return sorted(files)


def _render_file(path: pathlib.Path, repo_root: pathlib.Path) -> str:
    """Render a markdown file with a header that includes its relative path."""
    rel = path.relative_to(repo_root).as_posix()
    content = path.read_text(encoding="utf-8")

    # For Architecture.md, only include the portion above the generated marker.
    if path.name == "Architecture.md":
        marker = "<!-- GENERATED: DO NOT EDIT BELOW -->"
        if marker in content:
            content = content.split(marker, 1)[0].rstrip()

    header = f"\n\n---\n# Source: {rel}\n---\n\n"
    return header + content.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate llms-architecture.txt from docs/architecture/")
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("docs/architecture/Architecture.generated.md"),
        help="Output file path (default: docs/architecture/Architecture.generated.md)",
    )
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        default=pathlib.Path("."),
        help="Repository root path (default: current working directory)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output_path = (repo_root / args.output).resolve()

    docs = _discover_architecture_docs(repo_root)

    # Determine whether we should embed into an existing Architecture.md or write a new file.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    generated: list[str] = []
    for doc in docs:
        generated.append(_render_file(doc, repo_root))

    generated_text = "\n".join(generated)

    # Add an index of ADR files to the generated section.
    adr_dir = repo_root / "docs" / "architecture" / "adr"
    adr_files = []
    if adr_dir.exists():
        adr_files = sorted(adr_dir.glob("*.md"))

    if adr_files:
        adr_section = "\n## Architecture Decision Records\n"
        for adr in adr_files:
            adr_rel = adr.relative_to(repo_root).as_posix()
            adr_section += f"- {adr_rel}\n"
        adr_section += "\n"
        generated_text = adr_section + generated_text

    if output_path.name == "Architecture.md" and output_path.exists():
        # Preserve the top portion of Architecture.md above the marker.
        content = output_path.read_text(encoding="utf-8")
        marker = "<!-- GENERATED: DO NOT EDIT BELOW -->"
        if marker in content:
            prefix, _ = content.split(marker, 1)
            output_text = prefix.rstrip() + "\n\n" + marker + "\n\n" + generated_text
        else:
            output_text = content.rstrip() + "\n\n" + marker + "\n\n" + generated_text
    else:
        output_text = "# Architecture\n\n" + generated_text

    output_path.write_text(output_text, encoding="utf-8")

    print(f"Wrote {output_path} (included {len(docs)} docs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
