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

"""Consolidate scattered LLM context into deterministic tiered outputs.

This script discovers markdown sources throughout the repository and
consolidates them into a small set of canonical files:
- llms.txt
- llms-architecture.txt
- llms-improvements.txt

By default this script runs in dry-run mode (no file mutations). Use
`--apply` to write outputs and perform cleanup.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime
from pathlib import Path
from typing import Optional


@dataclasses.dataclass(frozen=True)
class ConsolidationConfig:
    """Configuration for the consolidation process, derived from CLI arguments."""

    repo_root: Path
    output_dir: Path
    apply: bool
    migrate_docstrings: bool
    verbose: bool


@dataclasses.dataclass
class ConsolidationReport:
    """Report summarizing the consolidation process,
    including discovered sources, outputs, and any errors.
    """

    repo_root: Path
    output_dir: Path
    apply: bool
    migrate_docstrings: bool
    timestamp: datetime.datetime
    sources: dict[str, list[Path]] = dataclasses.field(default_factory=dict)
    outputs_written: list[Path] = dataclasses.field(default_factory=list)
    outputs_skipped: list[Path] = dataclasses.field(default_factory=list)
    deleted_sources: list[Path] = dataclasses.field(default_factory=list)
    skipped_sources: list[Path] = dataclasses.field(default_factory=list)
    errors: list[str] = dataclasses.field(default_factory=list)

    def to_str(self) -> str:
        """Generate a human-readable report summarizing the consolidation process."""
        lines: list[str] = []
        lines.append("Consolidation Report")
        lines.append("====================")
        lines.append(f"Timestamp: {self.timestamp.isoformat()}")
        lines.append(f"Repo root: {self.repo_root}")
        lines.append(f"Output dir: {self.output_dir}")
        lines.append(f"Mode: {'apply' if self.apply else 'dry-run'}")
        lines.append(f"Migrate docstrings: {self.migrate_docstrings}")
        lines.append("")
        lines.append("Summary")
        lines.append("-------")
        lines.append(f"Sources discovered: {sum(len(v) for v in self.sources.values())}")
        for name, items in self.sources.items():
            lines.append(f"  {name}: {len(items)}")
        lines.append(f"Outputs written: {len(self.outputs_written)}")
        lines.append(f"Outputs skipped: {len(self.outputs_skipped)}")
        lines.append(f"Sources deleted: {len(self.deleted_sources)}")
        lines.append(f"Sources skipped (dry-run): {len(self.skipped_sources)}")
        lines.append(f"Errors: {len(self.errors)}")
        lines.append("")

        if self.errors:
            lines.append("Errors")
            lines.append("------")
            for err in self.errors:
                lines.append(f"- {err}")
            lines.append("")

        def section(title: str, items: list[Path]) -> None:
            """Helper to add a section to the report for a list of paths."""
            if not items:
                return
            lines.append(title)
            lines.append("-" * len(title))
            for p in sorted(items, key=str):
                lines.append(f"- {_normalize_path(p, self.repo_root)}")
            lines.append("")

        section("Sources discovered", [p for items in self.sources.values() for p in items])
        section("Outputs written", self.outputs_written)
        if not self.apply:
            section("Outputs that would be written", self.outputs_skipped)
            section("Sources that would be deleted", self.skipped_sources)
        else:
            section("Sources deleted", self.deleted_sources)

        return "\n".join(lines) + "\n"


LLMS_FILENAME = "llms.txt"
LLMS_ARCHITECTURE_FILENAME = "llms-architecture.txt"
LLMS_IMPROVEMENTS_FILENAME = "llms-improvements.txt"


def parse_args(argv: Optional[list[str]] = None) -> ConsolidationConfig:
    """Parse command-line arguments and return a ConsolidationConfig."""
    parser = argparse.ArgumentParser(
        description="Consolidate LLM context files into deterministic llms*.txt outputs."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to the repository root (default: current directory).",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to write output files into (default: repository root).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write files and perform cleanup. Defaults to dry-run.",
    )
    parser.add_argument(
        "--migrate-docstrings",
        action="store_true",
        help="Also migrate component markdown into Python module docstrings.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    args = parser.parse_args(argv)

    return ConsolidationConfig(
        repo_root=Path(args.repo_root).resolve(),
        output_dir=Path(args.output_dir).resolve(),
        apply=args.apply,
        migrate_docstrings=args.migrate_docstrings,
        verbose=args.verbose,
    )


def _normalize_path(path: Path, repo_root: Path) -> str:
    """Normalize a path to be relative to the repository root and use forward slashes."""
    # Use forward slashes for deterministic output across OSes.
    try:
        rel = path.relative_to(repo_root)
    except Exception:
        rel = path
    return str(rel).replace("\\", "/")


def _read_text(path: Path) -> str:
    """Read text from a file, replacing invalid characters to avoid encoding issues."""
    return path.read_text(encoding="utf-8", errors="replace")


def _write_text(path: Path, content: str, apply: bool, verbose: bool) -> bool:
    """Write text to a file if apply is True, otherwise log the intended action."""
    if not apply:
        if verbose:
            print(f"[dry-run] Would write: {path}")
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if verbose:
        print(f"Wrote: {path}")
    return True


def _is_ignored_path(path: Path) -> bool:
    """Determine if a path should be ignored based on common patterns."""
    # Skip common virtual environment and version control folders.
    ignore_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}
    return any(part in ignore_dirs for part in path.parts)


def _find_sources(repo_root: Path) -> dict[str, list[Path]]:
    """Discover source markdown files to be consolidated, categorized by type."""
    architecture_root = repo_root / "docs" / "architecture"
    sources: dict[str, list[Path]] = {
        "architecture": [],
        "improvements": [],
    }

    if architecture_root.exists():
        sources["architecture"] = sorted(
            [p for p in architecture_root.rglob("*.md") if p.is_file() and not _is_ignored_path(p)],
            key=lambda p: _normalize_path(p, repo_root),
        )

    for glob_pattern in ("**/*.description.md", "**/*.improvements.md"):
        sources["improvements"].extend(
            [
                p
                for p in repo_root.rglob(glob_pattern)
                if p.is_file() and not _is_ignored_path(p)
            ]
        )

    sources["improvements"] = sorted(
        sources["improvements"], key=lambda p: _normalize_path(p, repo_root)
    )

    return sources


def _build_llms_index(source_counts: dict[str, int]) -> str:
    """Build the content for llms.txt, which serves as an index
    to the consolidated LLM context files.
    """
    lines: list[str] = []
    lines.append("# llms.txt")
    lines.append("")
    lines.append("This file is generated by `scripts/consolidate_llm_context.py`. ")
    lines.append("It provides a stable entry point for LLMs and tooling to locate project context.")
    lines.append("")
    lines.append("## Generated files")
    lines.append("")
    lines.append("- llms-architecture.txt")
    lines.append("- llms-improvements.txt")
    lines.append("")
    lines.append("## Current source counts")
    lines.append("")
    lines.append(f"- architecture docs: {source_counts.get('architecture', 0)}")
    lines.append(f"- improvements docs: {source_counts.get('improvements', 0)}")
    lines.append("")
    lines.append("## Usage")
    lines.append("")
    lines.append("Run `python scripts/consolidate_llm_context.py --apply` to regenerate the LLM context files.")
    lines.append("")
    return "\n".join(lines) + "\n"


def _build_merge_output(title: str, sources: list[Path], repo_root: Path) -> str:
    """Build the content for a merged LLM context file
    (e.g. llms-architecture.txt) by concatenating source files with headers.
    """
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")

    if not sources:
        lines.append("*(No source documents found)*")
        lines.append("")
        return "\n".join(lines)

    for src in sources:
        rel = _normalize_path(src, repo_root)
        lines.append(f"## Source: {rel}")
        lines.append("")
        content = _read_text(src).rstrip("\n")
        lines.append(content)
        lines.append("")

    return "\n".join(lines)


def _make_docstring_block(markdown: str) -> str:
    """Format markdown content as a block to be inserted
    into a Python module docstring.
    """
    marker_start = "LLM CONTEXT (auto-generated) START"
    marker_end = "LLM CONTEXT (auto-generated) END"
    # Normalize line endings and strip leading/trailing whitespace.
    body = markdown.strip().replace("\r\n", "\n").strip()
    return "\n".join([marker_start, body, marker_end])


def _find_module_docstring_bounds(text: str) -> Optional[tuple[int, int]]:
    """Find the start and end line numbers of the module docstring, if present."""
    import io
    import tokenize

    reader = io.StringIO(text).readline
    try:
        for tok in tokenize.generate_tokens(reader):
            if tok.type == tokenize.STRING:
                # token.start/end are 1-indexed line/column
                start_line = tok.start[0]
                end_line = tok.end[0]
                return start_line - 1, end_line - 1
            if tok.type not in {tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT, tokenize.ENCODING}:
                break
    except tokenize.TokenError:
        return None
    return None


def _apply_docstring_migration(py_path: Path, markdown: str, apply: bool, verbose: bool) -> bool:
    """Apply docstring migration by inserting or updating a docstring block in the specified Python file."""
    if not py_path.exists():
        if verbose:
            print(f"Skipping docstring migration; module not found: {py_path}")
        return False

    text = _read_text(py_path)
    bounds = _find_module_docstring_bounds(text)
    block = _make_docstring_block(markdown)

    if bounds is None:
        # No existing module docstring; insert after initial comment block.
        lines = text.splitlines(keepends=True)
        insert_at = 0
        # Preserve shebang and initial comment header.
        while insert_at < len(lines) and (
            lines[insert_at].startswith("#!") or lines[insert_at].startswith("#") or lines[insert_at].strip() == ""
        ):
            insert_at += 1
        docstring = '"""\n' + block + "\n\"\"\"\n\n"
        lines.insert(insert_at, docstring)
        new_text = "".join(lines)
    else:
        start, end = bounds
        lines = text.splitlines(keepends=True)
        doc_lines = lines[start : end + 1]
        doc_text = "".join(doc_lines)
        # Remove existing block if present
        if "LLM CONTEXT (auto-generated)" in doc_text:
            # remove previous block between markers
            before, sep, after = doc_text.partition("LLM CONTEXT (auto-generated) START")
            if sep:
                # start at marker
                after_split = after.partition("LLM CONTEXT (auto-generated) END")
                if after_split[1]:
                    doc_text = before + after_split[2]
        # Insert block just before closing quotes
        if doc_text.strip().endswith('"""'):
            doc_text = doc_text.rstrip()
            doc_text = doc_text[: -3].rstrip() + "\n" + block + "\n\"\"\"\n"
        else:
            # Fallback: append at end
            doc_text = doc_text + "\n" + block + "\n"

        lines[start : end + 1] = [doc_text]
        new_text = "".join(lines)

    if apply:
        py_path.write_text(new_text, encoding="utf-8")
        if verbose:
            print(f"Updated module docstring: {py_path}")
        return True

    if verbose:
        print(f"[dry-run] Would update module docstring: {py_path}")
    return True


def _write_report(report_path: Path, report: "ConsolidationReport", apply: bool, verbose: bool) -> None:
    """Write the consolidation report to a file if apply is True, otherwise log the intended action."""
    content = report.to_str()
    if apply:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(content, encoding="utf-8")
        if verbose:
            print(f"Wrote report: {report_path}")
    else:
        if verbose:
            print(f"[dry-run] Would write report: {report_path}")


def run_consolidation(config: ConsolidationConfig) -> int:
    """Run the consolidation process based on the provided configuration."""
    sources = _find_sources(config.repo_root)
    report = ConsolidationReport(
        repo_root=config.repo_root,
        output_dir=config.output_dir,
        apply=config.apply,
        migrate_docstrings=config.migrate_docstrings,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        sources=sources,
    )

    # Build output contents
    outputs = {
        LLMS_FILENAME: _build_llms_index({k: len(v) for k, v in sources.items()}),
        LLMS_ARCHITECTURE_FILENAME: _build_merge_output(
            "LLM Architecture", sources.get("architecture", []), config.repo_root
        ),
        LLMS_IMPROVEMENTS_FILENAME: _build_merge_output(
            "LLM Improvements", sources.get("improvements", []), config.repo_root
        ),
    }

    for filename, content in outputs.items():
        out_path = config.output_dir / filename
        wrote = _write_text(out_path, content, config.apply, config.verbose)
        if wrote:
            report.outputs_written.append(out_path)
        else:
            report.outputs_skipped.append(out_path)

    # Optional docstring migration
    if config.migrate_docstrings:
        for source in sources.get("improvements", []):
            # Only migrate from files that were intended to be in sources
            base = source.name
            if base.endswith(".description.md"):
                module_name = base[: -len(".description.md")]
            elif base.endswith(".improvements.md"):
                module_name = base[: -len(".improvements.md")]
            else:
                continue
            module_path = source.with_name(module_name + ".py")
            try:
                _apply_docstring_migration(module_path, _read_text(source), config.apply, config.verbose)
            except Exception as e:
                report.errors.append(f"Failed docstring migration for {source}: {e}")

    # Cleanup source files (only apply mode)
    for src_list in sources.values():
        for src in src_list:
            if config.apply:
                try:
                    src.unlink()
                    report.deleted_sources.append(src)
                except Exception as e:
                    report.errors.append(f"Failed to delete {src}: {e}")
            else:
                report.skipped_sources.append(src)

    report_path = config.output_dir / "consolidation_report.txt"
    _write_report(report_path, report, config.apply, config.verbose)

    if config.verbose:
        print(report.to_str())

    return 1 if report.errors else 0


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for the consolidation script."""
    config = parse_args(argv)
    if config.verbose:
        print(f"Consolidation config: {config}")

    if config.apply:
        print("Applying consolidation (outputs will be written and source files may be deleted)")
    else:
        print("Dry-run: no files will be modified")

    return run_consolidation(config)


if __name__ == "__main__":
    raise SystemExit(main())
