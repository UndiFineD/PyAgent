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
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _normalize_rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _parse_manifest_split_files(manifest_path: Path) -> dict[str, str]:
    text = manifest_path.read_text(encoding="utf-8")
    mapping: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*-\s*([^:]+):\s*`([^`]+)`\s*$", line)
        if not match:
            continue
        key = match.group(1).strip()
        target = match.group(2).strip()
        mapping[key] = target
    return mapping


def _target_split_file(rel_path: str, split_map: dict[str, str]) -> str:
    first_part = rel_path.split("/", 1)[0]
    if first_part in split_map:
        return split_map[first_part]
    return split_map.get("other", "other.codestructure.md")


def _matches_anchor(ext: str, stripped: str) -> bool:
    py_patterns = [
        r"^(from\s+\S+\s+import\s+.+)$",
        r"^(import\s+.+)$",
        r"^class\s+\w+",
        r"^def\s+\w+",
        r"^async\s+def\s+\w+",
        r"^[A-Z][A-Z0-9_]*\s*=",
    ]
    ps_patterns = [
        r"^function\s+\w+",
        r"^class\s+\w+",
        r"^\$[A-Za-z_][A-Za-z0-9_]*\s*=",
    ]
    js_patterns = [
        r"^import\s+.+",
        r"^export\s+.+",
        r"^class\s+\w+",
        r"^function\s+\w+",
        r"^(const|let|var)\s+\w+\s*=",
        r"^(interface|type|enum)\s+\w+",
    ]
    rs_patterns = [
        r"^(pub\s+)?use\s+.+",
        r"^(pub\s+)?(struct|enum|trait|mod)\s+\w+",
        r"^(pub\s+)?fn\s+\w+",
        r"^(pub\s+)?const\s+\w+",
        r"^(pub\s+)?static\s+\w+",
        r"^impl\s+",
    ]

    if ext == ".py":
        return any(re.match(p, stripped) for p in py_patterns)
    if ext == ".ps1":
        return any(re.match(p, stripped, re.IGNORECASE) for p in ps_patterns)
    if ext in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        return any(re.match(p, stripped) for p in js_patterns)
    if ext == ".rs":
        return any(re.match(p, stripped) for p in rs_patterns)

    return bool(re.search(r"\b(class|def|function|fn|interface|enum|struct|trait|impl|import)\b", stripped))


def _extract_anchors(file_path: Path) -> list[tuple[int, str]]:
    """Extract anchors from a file for code structure documentation."""
    ext = file_path.suffix.lower()
    lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    anchors: list[tuple[int, str]] = []

    for index, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("#") and ext in {".py", ".ps1", ".sh"}:
            continue
        if stripped.startswith("//") and ext in {".js", ".jsx", ".ts", ".tsx", ".rs"}:
            continue

        if _matches_anchor(ext, stripped):
            anchors.append((index, stripped))

    if anchors:
        return anchors

    fallback: list[tuple[int, str]] = []
    for index, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped:
            continue
        fallback.append((index, stripped))
        if len(fallback) >= 25:
            break
    return fallback


def _remove_section(lines: list[str], rel_path: str, heading_prefix: str) -> list[str]:
    """Remove a section with the given heading prefix and relative path from the lines."""
    section_header = f"{heading_prefix} {rel_path}"
    output: list[str] = []
    i = 0
    found = False

    while i < len(lines):
        current = lines[i].rstrip("\n")
        if current.strip() == section_header:
            found = True
            i += 1
            while i < len(lines):
                nxt = lines[i].rstrip("\n")
                if nxt.startswith(f"{heading_prefix} "):
                    break
                i += 1
            continue
        output.append(current)
        i += 1

    if found:
        while len(output) >= 2 and output[-1] == "" and output[-2] == "":
            output.pop()

    return output


def _append_section(lines: list[str], rel_path: str, heading_prefix: str, anchors: list[tuple[int, str]]) -> list[str]:
    """Append a section with anchors to the given lines."""
    content = [line.rstrip("\n") for line in lines]
    if content and content[-1] != "":
        content.append("")
    content.append(f"{heading_prefix} {rel_path}")
    content.append("")
    for line_no, code in anchors:
        content.append(f"- {line_no}: {code}")
    return content


def _rewrite_split_file(path: Path, rel_path: str, heading_prefix: str, anchors: list[tuple[int, str]]) -> None:
    """Rewrite a split file with updated anchors for a given section."""
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    cleaned = _remove_section(existing, rel_path, heading_prefix)
    rewritten = _append_section(cleaned, rel_path, heading_prefix, anchors)
    path.write_text("\n".join(rewritten).rstrip() + "\n", encoding="utf-8")


def _heading_for_split(split_filename: str) -> str:
    """Return the appropriate heading prefix for a given split filename."""
    return "###" if split_filename == "other.codestructure.md" else "##"


def _all_split_filenames(split_map: dict[str, str]) -> list[str]:
    """Return all split filenames in a consistent order."""
    ordered: list[str] = []
    for key in ("backend", "rust_core", "scripts", "src", "tests", "web", "other"):
        if key in split_map:
            ordered.append(split_map[key])
    for value in split_map.values():
        if value not in ordered:
            ordered.append(value)
    return ordered


def main() -> int:
    """Update the appropriate split code-structure file with anchors from a target file, removing any stale entries."""
    parser = argparse.ArgumentParser(
        description="Update .github/agents/data/*codestructure.md for a single file.",
    )
    parser.add_argument("--file", required=True, help="Target file path to index (absolute or repo-relative).")
    args = parser.parse_args()

    root = _repo_root()
    manifest = root / ".github" / "agents" / "data" / "codestructure.md"
    data_dir = manifest.parent

    if not manifest.exists():
        raise SystemExit(f"Missing manifest: {manifest}")

    split_map = _parse_manifest_split_files(manifest)
    if not split_map:
        raise SystemExit("Could not parse split files from codestructure.md manifest")

    target = Path(args.file)
    if not target.is_absolute():
        target = root / target
    if not target.exists() or not target.is_file():
        raise SystemExit(f"Target file not found: {target}")

    rel_path = _normalize_rel(target, root)
    anchors = _extract_anchors(target)
    if not anchors:
        raise SystemExit(f"No indexable content found in: {rel_path}")

    # Remove stale sections from all split files first.
    for split_name in _all_split_filenames(split_map):
        split_path = data_dir / split_name
        if not split_path.exists():
            continue
        heading = _heading_for_split(split_name)
        lines = split_path.read_text(encoding="utf-8").splitlines()
        cleaned = _remove_section(lines, rel_path, heading)
        split_path.write_text("\n".join(cleaned).rstrip() + "\n", encoding="utf-8")

    destination = _target_split_file(rel_path, split_map)
    destination_path = data_dir / destination
    heading_prefix = _heading_for_split(destination)
    _rewrite_split_file(destination_path, rel_path, heading_prefix, anchors)

    print(f"Updated {destination_path.as_posix()} for {rel_path} with {len(anchors)} anchors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
