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

"""Run security scans (code quality + CodeQL) for the @8ql workflow.

This tool is intended to be invoked from within the repository by the
`@8ql` agent and produces a markdown report at:

  docs/project/<project>/<project>.8ql.md

The tool runs `python -m src.tools code_quality` against the changed files
relative to a base branch, then runs CodeQL (if configured) and embeds the
output in the report.
"""

from __future__ import annotations

import argparse
import datetime
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from src.tools.tool_registry import register_tool


def _run_cmd(cmd: list[str], capture: bool = False) -> Tuple[int, str, str]:
    """Run a command in a subprocess and optionally capture its output."""
    proc = subprocess.run(cmd, check=False, capture_output=capture, text=True)  # noqa: S603
    out = proc.stdout or ""
    err = proc.stderr or ""
    if capture:
        if out:
            print(out, end="")
        if err:
            print(err, file=sys.stderr, end="")
    return proc.returncode, out, err


def _get_merge_base(base: str) -> Optional[str]:
    """Get the merge base commit hash for the current HEAD and the given base branch."""
    proc = subprocess.run(["git", "merge-base", "HEAD", base], capture_output=True, text=True)  # noqa: S603 S607
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _get_changed_files(base: str) -> List[str]:
    """Get the list of files changed relative to the given base branch."""
    merge_base = _get_merge_base(base)
    if not merge_base:
        return []
    proc = subprocess.run(  # noqa: S603
        ["git", "diff", "--name-only", merge_base, "HEAD"],  # noqa: S607
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def _guess_project_name(branch: str) -> str:
    """Guess the project name from the branch name using common patterns."""
    # Common pattern: prjNNN-description
    # Fallback to last path segment
    branch = branch.strip()
    if "/" in branch:
        branch = branch.split("/")[-1]
    return branch


def _get_current_branch() -> str:
    """Get the current Git branch name."""
    proc = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)  # noqa: S603 S607
    if proc.returncode != 0:
        return ""  # best effort
    return proc.stdout.strip()


def _ensure_report_path(project: str) -> Path:
    """Ensure the report path exists for the given project and return the full path to the 8QL report."""
    # Ensure we have a project directory to store the report.
    report_dir = Path("docs") / "project" / project
    report_dir.mkdir(parents=True, exist_ok=True)
    return report_dir / f"{project}.8ql.md"


def _render_markdown_report(
    project: str,
    base: str,
    changed_files: List[str],
    code_quality_log: str,
    codeql_log: str,
    codeql_enabled: bool,
) -> str:
    """Render a markdown report for the 8QL security scan.

    Args:
        project: The project name.
        base: The base branch for comparison.
        changed_files: List of changed files.
        code_quality_log: Output from the code quality tool.
        codeql_log: Output from CodeQL.
        codeql_enabled: Whether CodeQL was enabled.

    Returns:
        A string containing the markdown report.

    """
    date = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    header = f"# {project} — 8QL Security Scan\n\n"
    header += "_Status: IN_PROGRESS_\n"
    header += f"_Scanner: @8ql | Updated: {date}_\n\n"

    scope = [
        "## Scan Scope",
        "| File | Scan type | Tool |",
        "|---|---|---|",
    ] + [
        f"| {f} | {('CodeQL + Code quality' if f.endswith('.py') else 'CodeQL')} | code_quality + codeql |"
        for f in changed_files
    ]

    summary = [
        "## Summary",
        f"- Base branch: `{base}`",
        f"- Changed files: {len(changed_files)}`",
        f"- CodeQL enabled: {codeql_enabled}",
    ]

    code_quality_section = [
        "## Code Quality Output",
        "```",
        code_quality_log.strip(),
        "```",
    ]

    codeql_section = [
        "## CodeQL Output",
        "```",
        codeql_log.strip(),
        "```",
    ]

    return "\n".join(
        [
            header,
            "\n".join(scope),
            "\n",
            "\n".join(summary),
            "\n",
            "\n".join(code_quality_section),
            "\n",
            "\n".join(codeql_section),
        ]
    )


def main(args: list[str] | None = None) -> int:
    """Main entry point for the `ql` tool."""
    parser = argparse.ArgumentParser(prog="ql")
    parser.add_argument("--base", default="main", help="Base branch to compare changes against")
    parser.add_argument("--files", nargs="*", help="Explicit list of files to scan (overrides git diff)")
    parser.add_argument("--project", help="Project folder name under docs/project")
    parser.add_argument(
        "--output",
        help="Path to write the 8ql report (defaults to docs/project/<project>/<project>.8ql.md)",
    )
    parser.add_argument(
        "--skip-codeql",
        action="store_true",
        help="Skip running CodeQL (useful when CodeQL CLI isn't available)",
    )

    parsed = parser.parse_args(args=args)

    branch = _get_current_branch()
    project = parsed.project or _guess_project_name(branch) or "unknown"
    report_path = Path(parsed.output) if parsed.output else _ensure_report_path(project)

    changed_files = _get_changed_files(parsed.base)
    print(f"Detected {len(changed_files)} changed files relative to {parsed.base}")

    # Run code quality checks on the same changed files.
    print("Running code_quality on changed files...")
    cq_cmd: list[str] = [
        sys.executable,
        "-m",
        "src.tools",
        "code_quality",
        "--base",
        parsed.base,
    ]
    if changed_files:
        cq_cmd.append("--files")
        cq_cmd.extend(changed_files)
    cq_rc, cq_out, cq_err = _run_cmd(cq_cmd, capture=True)
    cq_log = (cq_out + "\n" + cq_err).strip()

    # Optionally run CodeQL
    codeql_enabled = False
    codeql_log = ""
    if not parsed.skip_codeql and shutil.which("codeql"):
        codeql_enabled = True
        langs = (
            {"python" for f in changed_files if f.endswith(".py")}
            | {"rust" for f in changed_files if f.endswith(".rs")}
            | {"javascript-typescript" for f in changed_files if f.endswith(".js") or f.endswith(".ts")}
        )
        if not langs:
            codeql_log = "No supported CodeQL languages detected in changed files. Skipping CodeQL."
        else:
            with tempfile.TemporaryDirectory(prefix="pyagent-codeql-") as tmpdir:
                db_dir = Path(tmpdir) / "codeql-db"
                # Use a simple database create for the first language.
                # Note: CodeQL requires a build step for compiled languages.
                lang = sorted(langs)[0]
                codeql_log += f"Creating CodeQL database for language: {lang}\n"
                create_cmd = [
                    "codeql",
                    "database",
                    "create",
                    str(db_dir),
                    "--language",
                    lang,
                    "--source-root",
                    ".",
                ]
                # Limit the database to the changed files when possible to avoid scanning legacy/broken files.
                if changed_files:
                    create_cmd += [item for f in changed_files for item in ("--include", f)]
                rc, out, err = _run_cmd(create_cmd, capture=True)
                codeql_log += out + "\n" + err + "\n"
                if rc != 0:
                    codeql_log += f"CodeQL database creation failed (rc={rc}).\n"
                else:
                    out_path = Path(tmpdir) / "codeql-results.sarif"
                    codeql_log += "Running CodeQL analysis...\n"
                    rc2, out2, err2 = _run_cmd(
                        [
                            "codeql",
                            "database",
                            "analyze",
                            str(db_dir),
                            "--format=sarif-latest",
                            "--output",
                            str(out_path),
                            "--query",
                            "security-and-quality",
                        ],
                        capture=True,
                    )
                    codeql_log += out2 + "\n" + err2 + "\n"
                    if rc2 != 0:
                        codeql_log += f"CodeQL analysis failed (rc={rc2}).\n"
                    elif out_path.exists():
                        codeql_log += f"CodeQL SARIF written to {out_path}\n"
                        codeql_log += "(Note: SARIF is not embedded in this markdown report.)\n"
    else:
        codeql_log = "CodeQL skipped: CLI not found or --skip-codeql specified."

    report = _render_markdown_report(project, parsed.base, changed_files, cq_log, codeql_log, codeql_enabled)

    report_path.write_text(report, encoding="utf-8")
    print(f"Wrote 8ql report to {report_path}")

    return 1 if cq_rc != 0 else 0


register_tool(
    "ql",
    main,
    "Run code quality and CodeQL scans, and write a markdown report under docs/project/<project>/<project>.8ql.md",
)
