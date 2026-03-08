#!/usr/bin/env python3
"""Consolidate repository LLM context into tiered llms*.txt files."""
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
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class ConsolidationConfig:
    """Runtime configuration parsed from command-line arguments."""
    repo_root: Path
    output_dir: Path
    apply: bool
    migrate_docstrings: bool


@dataclass(frozen=True)
class ConsolidationReport:
    """Result summary for consolidation execution."""

    merged: list[Path]
    deleted: list[Path]
    skipped: list[Path]
    errors: list[str]


LLM_CONTEXT_START = "LLM_CONTEXT_START"
LLM_CONTEXT_END = "LLM_CONTEXT_END"


def _build_llms_root_text() -> str:
    """Build root llms.txt content with pointers to tiered context files."""
    return "\n".join(
        [
            "# PyAgent LLM Context",
            "",
            "PyAgent is a multi-agent swarm system optimized for autonomous code improvement.",
            "",
            "## Tiered context files",
            "- llms-architecture.txt",
            "- llms-improvements.txt",
            "",
            "## Notes",
            "Use llms-architecture.txt for architecture and layout rules.",
            "Use llms-improvements.txt for consolidated improvements and lessons.",
            "",
        ]
    )


def _build_architecture_text() -> str:
    """Build baseline architecture tier content."""
    return "\n".join(
        [
            "# PyAgent Architecture Context",
            "",
            "This file contains architecture and codebase-level context.",
            "",
        ]
    )


def _build_improvements_text() -> str:
    """Build baseline improvements tier content."""
    return "\n".join(
        [
            "# PyAgent Improvements Context",
            "",
            "This file contains consolidated improvements and lessons learned.",
            "",
        ]
    )


def _safe_read_text(path: Path) -> str:
    """Read text using UTF-8 with replacement fallback for robustness."""
    return path.read_text(encoding="utf-8", errors="replace")


def _discover_architecture_files(repo_root: Path) -> list[Path]:
    """Discover architecture markdown files in deterministic order."""
    architecture_dir = repo_root / "docs" / "architecture"
    if not architecture_dir.exists():
        return []
    return sorted(p for p in architecture_dir.rglob("*.md") if p.is_file())


def _discover_improvements_files(repo_root: Path) -> list[Path]:
    """Discover *.description.md and *.improvements.md in deterministic order."""
    found: list[Path] = []
    for pattern in ("*.description.md", "*.improvements.md"):
        found.extend(p for p in repo_root.rglob(pattern) if p.is_file())
    return sorted(found)


def _format_section(source: Path, repo_root: Path, content: str) -> str:
    """Format a source markdown section with normalized relative path heading."""
    relative = source.relative_to(repo_root).as_posix()
    body = content.replace("\r\n", "\n").replace("\r", "\n").strip()
    return f"## Source: {relative}\n\n{body}\n"


def _merge_sections(base_text: str, sections: list[str]) -> str:
    """Merge base heading text with discovered source sections."""
    base = base_text.rstrip() + "\n\n"
    if not sections:
        return base
    return base + "\n".join(section.rstrip() for section in sections) + "\n"


def _module_path_for_markdown(path: Path) -> Path | None:
    """Resolve matching Python module for a description/improvements markdown file."""
    filename = path.name
    if filename.endswith(".description.md"):
        module_name = filename[: -len(".description.md")] + ".py"
    elif filename.endswith(".improvements.md"):
        module_name = filename[: -len(".improvements.md")] + ".py"
    else:
        return None

    candidate = path.with_name(module_name)
    return candidate if candidate.exists() else None


def _build_docstring_marker_block(sections: list[str]) -> str:
    """Build marker block to inject into module docstring region."""
    merged = "\n".join(section.rstrip() for section in sections).strip()
    return (
        '"""\n'
        f"{LLM_CONTEXT_START}\n\n"
        f"{merged}\n\n"
        f"{LLM_CONTEXT_END}\n"
        '"""\n\n'
    )


def _remove_existing_marker_blocks(text: str) -> str:
    """Remove previously injected marker block to keep migration idempotent."""
    pattern = re.compile(
        r'"""\nLLM_CONTEXT_START\n.*?\nLLM_CONTEXT_END\n"""\n*',
        re.DOTALL,
    )
    return re.sub(pattern, "", text)


def _inject_docstring_marker_block(module_path: Path, sections: list[str]) -> None:
    """Inject marker block after shebang/comments while preserving top header lines."""
    original = module_path.read_text(encoding="utf-8", errors="replace")
    cleaned = _remove_existing_marker_blocks(original)

    lines = cleaned.splitlines(keepends=True)
    idx = 0
    if idx < len(lines) and lines[idx].startswith("#!"):
        idx += 1
    while idx < len(lines) and lines[idx].startswith("#"):
        idx += 1
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1

    prefix = "".join(lines[:idx])
    rest = "".join(lines[idx:])
    block = _build_docstring_marker_block(sections)
    updated = prefix + block + rest
    module_path.write_text(updated, encoding="utf-8")


def _migrate_docstrings(repo_root: Path, markdown_paths: list[Path]) -> None:
    """Migrate markdown context into matching Python module marker blocks."""
    sections_by_module: dict[Path, list[str]] = {}
    for md_path in markdown_paths:
        module_path = _module_path_for_markdown(md_path)
        if module_path is None:
            continue
        section = _format_section(md_path, repo_root, _safe_read_text(md_path))
        sections_by_module.setdefault(module_path, []).append(section)

    for module_path in sorted(sections_by_module):
        _inject_docstring_marker_block(module_path, sections_by_module[module_path])


def _write_text(path: Path, text: str) -> None:
    """Write text using UTF-8 with normalized line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_text(normalized, encoding="utf-8")


def _write_report(path: Path, report: ConsolidationReport, repo_root: Path) -> None:
    """Write deterministic consolidation report text file."""
    merged_rel = [item.relative_to(repo_root).as_posix() for item in sorted(report.merged)]
    deleted_rel = [item.relative_to(repo_root).as_posix() for item in sorted(report.deleted)]
    skipped_rel = [item.relative_to(repo_root).as_posix() for item in sorted(report.skipped)]

    lines = [
        "# Consolidation Report",
        "",
        f"merged_count: {len(report.merged)}",
        f"deleted_count: {len(report.deleted)}",
        f"skipped_count: {len(report.skipped)}",
        f"error_count: {len(report.errors)}",
        "",
        "## Merged Files",
    ]
    lines.extend(merged_rel or ["(none)"])
    lines.extend(["", "## Deleted Files"])
    lines.extend(deleted_rel or ["(none)"])
    lines.extend(["", "## Skipped Files"])
    lines.extend(skipped_rel or ["(none)"])
    lines.extend(["", "## Errors"])
    lines.extend(report.errors or ["(none)"])
    lines.append("")

    _write_text(path, "\n".join(lines))


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for context consolidation."""
    parser = argparse.ArgumentParser(
        prog="consolidate_llm_context",
        description="Consolidate markdown context into llms*.txt files.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root path to scan (default: current directory).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for llms*.txt files (default: repo root).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply destructive changes (default is dry-run).",
    )
    parser.add_argument(
        "--migrate-docstrings",
        action="store_true",
        help="Also migrate markdown notes into matching Python module docstrings.",
    )
    return parser


def parse_args(argv: Sequence[str] | None = None) -> ConsolidationConfig:
    """Parse command-line arguments into immutable runtime config."""
    parser = build_parser()
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    output_dir = Path(args.output_dir) if args.output_dir is not None else repo_root

    return ConsolidationConfig(
        repo_root=repo_root,
        output_dir=output_dir,
        apply=bool(args.apply),
        migrate_docstrings=bool(args.migrate_docstrings),
    )


def run(config: ConsolidationConfig) -> int:
    """Execute consolidation workflow.

    Later phases populate this function with full consolidation behavior.
    """
    output_dir = config.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    merged_sources: list[Path] = []
    deleted_sources: list[Path] = []
    skipped_sources: list[Path] = []
    errors: list[str] = []

    _write_text(output_dir / "llms.txt", _build_llms_root_text())

    architecture_paths = _discover_architecture_files(config.repo_root)
    architecture_sections = []
    for path in architecture_paths:
        try:
            architecture_sections.append(_format_section(path, config.repo_root, _safe_read_text(path)))
            merged_sources.append(path)
        except OSError as exc:
            errors.append(f"{path.relative_to(config.repo_root).as_posix()}: {exc}")
            skipped_sources.append(path)
    architecture_text = _merge_sections(_build_architecture_text(), architecture_sections)
    _write_text(output_dir / "llms-architecture.txt", architecture_text)

    improvement_paths = _discover_improvements_files(config.repo_root)
    improvements_sections = []
    for path in improvement_paths:
        try:
            improvements_sections.append(_format_section(path, config.repo_root, _safe_read_text(path)))
            merged_sources.append(path)
        except OSError as exc:
            errors.append(f"{path.relative_to(config.repo_root).as_posix()}: {exc}")
            skipped_sources.append(path)
    improvements_text = _merge_sections(_build_improvements_text(), improvements_sections)
    _write_text(output_dir / "llms-improvements.txt", improvements_text)

    if config.migrate_docstrings:
        _migrate_docstrings(config.repo_root, improvement_paths)

    if config.apply:
        for path in sorted(set(merged_sources)):
            if path.exists():
                try:
                    path.unlink()
                    deleted_sources.append(path)
                except OSError as exc:
                    errors.append(f"Failed delete {path.relative_to(config.repo_root).as_posix()}: {exc}")

    report = ConsolidationReport(
        merged=sorted(set(merged_sources)),
        deleted=sorted(set(deleted_sources)),
        skipped=sorted(set(skipped_sources)),
        errors=errors,
    )
    _write_report(output_dir / "consolidation_report.txt", report, config.repo_root)

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint."""
    config = parse_args(argv)
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
