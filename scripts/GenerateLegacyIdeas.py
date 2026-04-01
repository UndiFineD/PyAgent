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
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MAX_IDEAS_PER_FILE = 10

TEMPLATE_SECTIONS = [
    "Idea summary",
    "Problem statement",
    "Why this matters now",
    "User persona and impacted systems",
    "Detailed proposal",
    "Scope suggestion",
    "Non-goals",
    "Requirements",
    "Dependencies and constraints",
    "Research findings",
    "Candidate implementation paths",
    "Success metrics",
    "Validation commands",
    "Risks and mitigations",
    "Failure handling and rollback",
    "Readiness status",
    "Priority scoring",
    "Merged from",
    "Source references",
]

DEFAULT_ARCHETYPES = [
    ("hardening", "Hardening", "Reduce defects and improve safety posture."),
    ("test-coverage", "Test Coverage", "Increase deterministic test coverage and reliability."),
    ("performance", "Performance", "Improve runtime performance and resource efficiency."),
    ("observability", "Observability", "Improve logs, metrics, and debugging visibility."),
    ("resilience", "Resilience", "Improve fault tolerance and recovery behavior."),
    ("api-consistency", "API Consistency", "Normalize interfaces and reduce behavioral drift."),
    ("documentation", "Documentation", "Improve docs and operational guidance quality."),
    ("security", "Security", "Reduce security exposure and harden boundaries."),
    ("developer-experience", "Developer Experience", "Reduce friction for contributors and operators."),
    ("migration-readiness", "Migration Readiness", "Prepare component for future migration or modernization."),
]

CODE_EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".rs",
    ".go",
    ".java",
    ".kt",
    ".cs",
    ".cpp",
    ".c",
    ".h",
}

DOC_EXTENSIONS = {".md", ".txt", ".rst", ".adoc"}


def _extract_text_sample(path: Path, max_file_bytes: int) -> tuple[str, str]:
    """Read a bounded sample from a file and return (head, tail)."""
    raw = path.read_bytes()[:max_file_bytes]
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    head = "\n".join(lines[:40])
    tail = "\n".join(lines[-20:])
    return head, tail


def _file_kind(path: Path) -> str:
    """Classify file kind for idea archetype tuning."""
    suffix = path.suffix.lower()
    if suffix in CODE_EXTENSIONS:
        return "code"
    if suffix in DOC_EXTENSIONS:
        return "docs"
    return "asset"


def _build_context_summary(path: Path, head: str, tail: str) -> dict[str, Any]:
    """Derive lightweight static signals from the sampled text."""
    text = f"{head}\n{tail}"
    function_count = len(re.findall(r"\b(def|function|fn|class|interface|struct)\b", text))
    todo_count = len(re.findall(r"\b(TODO|FIXME|HACK)\b", text, flags=re.IGNORECASE))
    has_tests = bool(re.search(r"\b(test|assert|pytest|unittest|spec)\b", text, flags=re.IGNORECASE))
    return {
        "path": path.as_posix(),
        "suffix": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "function_like_tokens": function_count,
        "todo_like_tokens": todo_count,
        "has_test_signal": has_tests,
    }


def _section_block(title: str, body: str) -> str:
    """Render one markdown section."""
    return f"## {title}\n{body.strip()}\n"


def _score_from_context(context: dict[str, Any], archetype_index: int) -> dict[str, int]:
    """Build simple deterministic scoring fields."""
    impact = min(5, 2 + int(context["function_like_tokens"] > 5) + int(context["todo_like_tokens"] > 0))
    confidence = 2 + int(context["has_test_signal"])
    effort = min(5, 2 + int(context["size_bytes"] > 20_000) + archetype_index % 2)
    risk = min(5, 2 + int(context["todo_like_tokens"] > 2))
    alignment = 3
    priority = impact + confidence + alignment - effort - risk
    return {
        "impact_score": impact,
        "confidence_score": confidence,
        "effort_score": effort,
        "risk_score": risk,
        "alignment_score": alignment,
        "priority_score": priority,
    }


def _build_idea_markdown(
    idea_id: str,
    title: str,
    source_path: str,
    context: dict[str, Any],
    archetype_focus: str,
    scoring: dict[str, int],
) -> str:
    """Render a near-complete @10idea template for one generated idea."""
    idea_summary = (
        f"Generate a focused improvement initiative for `{source_path}` "
        f"with objective: {archetype_focus}"
    )
    problem_statement = (
        f"Legacy file `{source_path}` from v3.7.0 may contain latent quality risks, "
        "drift, or missing modernization opportunities."
    )
    why_now = (
        "This file comes from the pre-breakage baseline and is a candidate "
        "for high-confidence recovery and modernization."
    )
    persona = (
        "Primary personas: maintainers, release engineers, and "
        "quality/security reviewers."
    )
    detailed = (
        "Perform a targeted review, codify findings as tests and safeguards, "
        "and evolve behavior with minimal regressions."
    )
    scope = (
        "In scope: this file and directly related tests/docs. "
        "Out of scope: unrelated subsystem redesign."
    )
    non_goals = (
        "Do not rewrite unrelated modules or perform broad architecture "
        "changes in this slice."
    )
    requirements = (
        "Preserve behavior parity where required, add deterministic validation, "
        "and keep changes auditable."
    )
    constraints = (
        "Constraints include existing coding standards, governance checks, "
        "and CI policy gates."
    )
    findings = (
        f"Static signals: size={context['size_bytes']} bytes, "
        f"function_like_tokens={context['function_like_tokens']}, "
        f"todo_like_tokens={context['todo_like_tokens']}, "
        f"has_test_signal={context['has_test_signal']}."
    )
    paths = (
        "Path A: hardening and tests first. "
        "Path B: refactor-first then test parity. "
        "Path C: documentation and observability uplift."
    )

    sections = [
        f"# {idea_id} - {title}",
        "",
        "Planned project mapping: none yet",
        "",
        _section_block("Idea summary", idea_summary),
        _section_block("Problem statement", problem_statement),
        _section_block("Why this matters now", why_now),
        _section_block("User persona and impacted systems", persona),
        _section_block("Detailed proposal", detailed),
        _section_block("Scope suggestion", scope),
        _section_block("Non-goals", non_goals),
        _section_block("Requirements", requirements),
        _section_block("Dependencies and constraints", constraints),
        _section_block("Research findings", findings),
        _section_block("Candidate implementation paths", paths),
        _section_block(
            "Success metrics",
            "All added tests pass, no regressions introduced, and CI checks remain green.",
        ),
        _section_block("Validation commands", "- pytest -q\n- pre-commit run --all-files"),
        _section_block("Risks and mitigations", "Risk: behavior drift. Mitigation: parity tests and scoped diffs."),
        _section_block(
            "Failure handling and rollback",
            "Use branch-isolated commits and revert scoped changes if validation fails.",
        ),
        _section_block("Readiness status", "ready"),
        _section_block(
            "Priority scoring",
            "\n".join(
                [
                    f"- impact_score: {scoring['impact_score']}",
                    f"- confidence_score: {scoring['confidence_score']}",
                    f"- effort_score: {scoring['effort_score']}",
                    f"- risk_score: {scoring['risk_score']}",
                    f"- alignment_score: {scoring['alignment_score']}",
                    f"- priority_score: {scoring['priority_score']}",
                ]
            ),
        ),
        _section_block("Merged from", "- none"),
        _section_block("Source references", f"- `{source_path}`"),
    ]
    return "\n".join(sections).strip() + "\n"


def _iter_source_files(root: Path) -> list[Path]:
    """List files recursively while excluding dot-directories."""
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part.startswith(".") for part in rel_parts[:-1]):
            continue
        files.append(path)
    files.sort()
    return files


def _generate_for_file(path: Path, root: Path, max_ideas_per_file: int, max_file_bytes: int) -> list[dict[str, Any]]:
    """Generate up to N template-filled ideas for one file."""
    head, tail = _extract_text_sample(path, max_file_bytes=max_file_bytes)
    relative_path = path.relative_to(root).as_posix()
    kind = _file_kind(path)

    archetypes = list(DEFAULT_ARCHETYPES)
    if kind == "docs":
        archetypes = archetypes[:6]
    elif kind == "asset":
        archetypes = archetypes[:4]

    max_count = max(1, min(MAX_IDEAS_PER_FILE, max_ideas_per_file, len(archetypes)))
    context = _build_context_summary(path, head, tail)

    ideas: list[dict[str, Any]] = []
    file_hash = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:10]
    base_name = path.stem.replace("_", "-").replace(" ", "-").lower()

    for index in range(max_count):
        slug, suffix_title, focus = archetypes[index]
        generated_idea_id = f"legacy-{file_hash}-{index + 1:02d}"
        title = f"{base_name} {suffix_title}".strip()
        scoring = _score_from_context(context, archetype_index=index)
        markdown = _build_idea_markdown(
            idea_id=generated_idea_id,
            title=title,
            source_path=relative_path,
            context=context,
            archetype_focus=focus,
            scoring=scoring,
        )

        ideas.append(
            {
                "idea_id": generated_idea_id,
                "source_file": relative_path,
                "kind": kind,
                "archetype": slug,
                "title": title,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "template_markdown": markdown,
            }
        )

    return ideas


def generate_ideas(
    legacy_root: Path,
    max_ideas_per_file: int,
    offset: int,
    limit: int | None,
    max_file_bytes: int,
) -> dict[str, Any]:
    """Generate template-filled ideas for files in the legacy tree."""
    all_files = _iter_source_files(legacy_root)
    start = max(0, offset)
    end = None if limit is None else start + max(0, limit)
    window = all_files[start:end]

    rows: list[dict[str, Any]] = []
    for source_file in window:
        rows.extend(
            _generate_for_file(
                source_file,
                root=legacy_root,
                max_ideas_per_file=max_ideas_per_file,
                max_file_bytes=max_file_bytes,
            )
        )

    return {
        "schema_version": 1,
        "legacy_root": legacy_root.as_posix(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "offset": start,
        "limit": limit,
        "available_file_count": len(all_files),
        "processed_file_count": len(window),
        "idea_count": len(rows),
        "ideas": rows,
    }


def _write_jsonl(output_path: Path, payload: dict[str, Any]) -> None:
    """Write generated ideas as a single jsonl file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for item in payload["ideas"]:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def _write_jsonl_split(output_dir: Path, payload: dict[str, Any]) -> list[str]:
    """Write one jsonl file per unique source_file, mirroring the source tree under output_dir.

    Returns a sorted list of written output paths (relative to output_dir).
    """
    # Group ideas by source_file
    groups: dict[str, list[dict[str, Any]]] = {}
    for item in payload["ideas"]:
        groups.setdefault(item["source_file"], []).append(item)

    written: list[str] = []
    for source_file, ideas in sorted(groups.items()):
        # Mirror directory structure: src/core/base/foo.py -> output_dir/src/core/base/foo.jsonl
        dest = output_dir / (Path(source_file).with_suffix(".jsonl"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", encoding="utf-8") as handle:
            for item in ideas:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
        written.append(dest.as_posix())

    return written


def _write_manifest(manifest_path: Path, payload: dict[str, Any], split_files: list[str] | None = None) -> None:
    """Write run manifest for resumable batch processing."""
    manifest = {
        key: payload[key]
        for key in [
            "schema_version",
            "legacy_root",
            "generated_at",
            "offset",
            "limit",
            "available_file_count",
            "processed_file_count",
            "idea_count",
        ]
    }
    if split_files is not None:
        manifest["split_output_file_count"] = len(split_files)
        manifest["split_output_files"] = split_files
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    """Build command-line parser."""
    parser = argparse.ArgumentParser(
        description="Generate template-filled ideas from legacy repository files."
    )
    parser.add_argument(
        "--legacy-root",
        required=True,
        help="Path to legacy repo root (e.g. C:\\Dev\\PyAgent.3.7.0)",
    )
    parser.add_argument(
        "--output",
        default="docs/project/legacy_ideas_3_7_0.jsonl",
        help="Output jsonl path for single-file mode (ignored when --output-dir is set)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=(
            "Directory for split-by-source-file mode. "
            "One jsonl is written per source file, mirroring the source tree. "
            "When set, --output is ignored."
        ),
    )
    parser.add_argument(
        "--manifest",
        default="docs/project/legacy_ideas_3_7_0.manifest.json",
        help="Run manifest output path",
    )
    parser.add_argument(
        "--max-ideas-per-file",
        type=int,
        default=10,
        help="Max generated ideas per file (1-10)",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Start file index for batch processing",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional number of files to process in this run",
    )
    parser.add_argument(
        "--max-file-bytes",
        type=int,
        default=262144,
        help="Max bytes sampled per source file",
    )
    return parser


def main() -> int:
    """Generate ideas and write outputs."""
    args = _build_parser().parse_args()
    legacy_root = Path(args.legacy_root).resolve()
    if not legacy_root.exists():
        raise SystemExit(f"LEGACY_ROOT_MISSING {legacy_root}")

    payload = generate_ideas(
        legacy_root=legacy_root,
        max_ideas_per_file=args.max_ideas_per_file,
        offset=args.offset,
        limit=args.limit,
        max_file_bytes=args.max_file_bytes,
    )

    manifest_path = Path(args.manifest).resolve()

    if args.output_dir is not None:
        output_dir = Path(args.output_dir).resolve()
        split_files = _write_jsonl_split(output_dir, payload)
        _write_manifest(manifest_path, payload, split_files=split_files)
        print(
            "LEGACY_IDEA_GENERATOR_OK "
            f"files={payload['processed_file_count']} "
            f"ideas={payload['idea_count']} "
            f"split_files={len(split_files)} "
            f"output_dir={output_dir} "
            f"manifest={manifest_path}"
        )
    else:
        output_path = Path(args.output).resolve()
        _write_jsonl(output_path, payload)
        _write_manifest(manifest_path, payload)
        print(
            "LEGACY_IDEA_GENERATOR_OK "
            f"files={payload['processed_file_count']} "
            f"ideas={payload['idea_count']} "
            f"output={output_path} "
            f"manifest={manifest_path}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
