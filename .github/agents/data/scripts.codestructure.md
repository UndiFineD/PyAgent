# Code Structure Index

Domain index for `scripts` paths.

Format: `## <file>` followed by `- line: code` entries.

## scripts/AgentDocFrequency.py

- 26: from __future__ import annotations
- 28: import argparse
- 29: import subprocess
- 30: from dataclasses import dataclass, field
- 31: from datetime import datetime, timezone
- 32: from pathlib import Path
- 36: class DocStats:
- 46: def _git_log_count(path: Path, repo_root: Path) -> int:
- 62: def _git_last_modified(path: Path, repo_root: Path) -> datetime \| None:
- 80: def analyse_docs(
- 121: def format_table(stats: list[DocStats]) -> str:
- 133: def main() -> None:
- 152: raise SystemExit(1)

## scripts/FlmTpsBenchmark.py

- 37: from __future__ import annotations
- 39: import argparse
- 40: import os
- 41: import sys
- 42: import time
- 43: from dataclasses import dataclass, field
- 44: from pathlib import Path
- 45: from typing import Any
- 51: _ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
- 54: from dotenv import load_dotenv
- 73: from openai import OpenAI
- 82: _DEFAULT_PROMPT = (
- 90: _RESET = "\033[0m"
- 91: _BOLD = "\033[1m"
- 92: _GREEN = "\033[32m"
- 93: _CYAN = "\033[36m"
- 94: _YELLOW = "\033[33m"
- 102: class _RequestResult:
- 111: def tps(self) -> float:
- 120: class _Stats:
- 125: def record(self, r: _RequestResult) -> None:
- 130: def completed(self) -> int:
- 135: def total_completion_tokens(self) -> int:
- 140: def total_prompt_tokens(self) -> int:
- 145: def total_tokens(self) -> int:
- 150: def total_elapsed(self) -> float:
- 155: def avg_tps(self) -> float:
- 162: def last_tps(self) -> float:
- 167: def max_tps(self) -> float:
- 172: def min_tps(self) -> float:
- 177: def avg_completion_tokens(self) -> float:
- 188: def _build_parser() -> argparse.ArgumentParser:
- 253: def _fmt_tps(v: float) -> str:
- 258: def _fmt_dur(seconds: float) -> str:
- 264: def _bar(fraction: float, width: int = 30) -> str:
- 270: def _print_live(stats: _Stats, elapsed_wall: float, duration: float) -> None:
- 288: def _print_summary(stats: _Stats, wall_time: float, args: argparse.Namespace) -> None:
- 323: def _run_benchmark(client: Any, args: argparse.Namespace) -> _Stats:
- 386: def main(argv: list[str] \| None = None) -> int:

## scripts/GeneratePmTemplates.py

- 19: from __future__ import annotations
- 21: import argparse
- 22: import os
- 23: from pathlib import Path
- 25: _TEMPLATES: dict[str, str] = {
- 92: def generate(out_dir: str) -> list[str]:
- 104: def main() -> None:

## scripts/SetupTests.py

- 23: from __future__ import annotations
- 25: import argparse
- 26: import os
- 27: from pathlib import Path
- 30: def _placeholder_test(pkg: str) -> str:
- 39: def create_test_structure(src_root: str, tests_root: str, dry_run: bool = False) -> list[str]:
- 64: def main() -> None:

## scripts/changelog.py

- 15: from __future__ import annotations
- 17: import subprocess
- 18: from pathlib import Path
- 21: def generate_entry() -> str:
- 56: def main() -> None:

## scripts/ci/run_checks.py

- 13: from __future__ import annotations
- 15: import argparse
- 16: import subprocess
- 17: from pathlib import Path
- 20: CORE_TEST_FILES = [
- 51: PRECOMMIT_TEST_FILES = [
- 94: CODEQL_TEST_FILES = [
- 102: def run_command(cmd: list[str], env: dict[str, str] \| None = None) -> None:
- 108: def _filter_python_targets(paths: list[str]) -> list[str]:
- 119: def run_ruff(paths: list[str] \| None = None) -> None:
- 135: def run_mypy() -> None:
- 140: def run_pytest(files: list[str], extra_args: list[str] \| None = None) -> None:
- 148: def profile_precommit(paths: list[str] \| None = None) -> None:
- 159: def profile_ci() -> None:
- 171: def main(argv: list[str] \| None = None) -> int:
- 199: raise SystemExit(main())

## scripts/clear_caches.ps1

- 22: $RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
- 25: $cacheDirNames = @('__pycache__', '.pytest_cache', '.mypy_cache', '.hypothesis', '.ruff_cache', '.tox')
- 26: $cacheFileNames = @('*.pyc', '*.pyo')
- 27: $excludeDirs = @('.git', '.venv', 'venv', 'node_modules', 'env')
- 56: $items = @()
- 57: $stack = new-object System.Collections.Stack
- 61: $current = $stack.Pop()
- 68: $children = Get-ChildItem -LiteralPath $current.FullName -Force -ErrorAction SilentlyContinue
- 71: foreach ($child in $children) {
- 82: foreach ($pattern in $cacheFileNames) {
- 95: $allTargets = @(Get-TargetItems)
- 99: foreach ($target in $allTargets) {

## scripts/compile_diagrams.py

- 17: from __future__ import annotations
- 19: import subprocess
- 20: from pathlib import Path
- 22: diagram_dir = Path("docs/architecture")
- 25: def compile_diagrams() -> None:

## scripts/consolidate_llm_context.py

- 27: from __future__ import annotations
- 29: import argparse
- 30: import dataclasses
- 31: import datetime
- 32: from pathlib import Path
- 33: from typing import Optional
- 37: class ConsolidationConfig:
- 47: class ConsolidationReport:
- 63: def to_str(self) -> str:
- 93: def section(title: str, items: list[Path]) -> None:
- 114: LLMS_FILENAME = "llms.txt"
- 115: LLMS_ARCHITECTURE_FILENAME = "llms-architecture.txt"
- 116: LLMS_IMPROVEMENTS_FILENAME = "llms-improvements.txt"
- 119: def parse_args(argv: Optional[list[str]] = None) -> ConsolidationConfig:
- 161: def _normalize_path(path: Path, repo_root: Path) -> str:
- 171: def _read_text(path: Path) -> str:
- 176: def _write_text(path: Path, content: str, apply: bool, verbose: bool) -> bool:
- 190: def _is_ignored_path(path: Path) -> bool:
- 197: def _find_sources(repo_root: Path) -> dict[str, list[Path]]:
- 227: def _build_llms_index(source_counts: dict[str, int]) -> str:
- 253: def _build_merge_output(title: str, sources: list[Path], repo_root: Path) -> str:
- 277: def _make_docstring_block(markdown: str) -> str:
- 287: def _find_module_docstring_bounds(text: str) -> Optional[tuple[int, int]]:
- 289: import io
- 290: import tokenize
- 307: def _apply_docstring_migration(py_path: Path, markdown: str, apply: bool, verbose: bool) -> bool:
- 366: def _write_report(report_path: Path, report: "ConsolidationReport", apply: bool, verbose: bool) -> None:
- 379: def run_consolidation(config: ConsolidationConfig) -> int:
- 448: def main(argv: Optional[list[str]] = None) -> int:
- 463: raise SystemExit(main())

## scripts/deploy.py

- 6: def deploy(env: str) -> None:

## scripts/dryrun_move.py

- 6: import json
- 7: from pathlib import Path
- 9: MAPPINGS = {
- 14: def dryrun(root: Path = Path('.')) -> dict[str, list[str]]:
- 24: def main() -> None:

## scripts/enforce_branch.py

- 26: from __future__ import annotations
- 28: import re
- 29: import subprocess
- 33: _PRJ_BRANCH = re.compile(r"^(prj\d{3,7})-[a-z0-9-]+$")
- 35: _PRJ_PATH = re.compile(r"docs/project/(prj\d{3,7})/")
- 37: _BASE_BRANCHES = {"main", "master", "dev", "develop"}
- 40: def _run(args: list[str]) -> str:
- 46: def get_current_branch() -> str:
- 51: def get_staged_files() -> list[str]:
- 57: def extract_project_ids(staged: list[str]) -> set[str]:
- 69: def main() -> int:
- 122: raise SystemExit(main())

## scripts/fix_indentation.py

- 29: def method(self):
- 31: from functools import reduce   # should be 8 spaces
- 38: def method(self):
- 40: from functools import reduce
- 46: module scope instead of inside the class.
- 48: class Foo:
- 49: def good(self): ...
- 51: def bad(self): ...                # missing 4 spaces
- 83: from __future__ import annotations
- 85: import argparse
- 88: import re
- 89: import sys
- 90: import time
- 91: from pathlib import Path
- 92: from typing import Optional
- 97: CONTEXT_WINDOW = 20        # lines to scan before/after for indent inference
- 98: MIN_INDENT_STEP = 4        # smallest natural indent step in Python
- 99: MAX_PASSES = 20            # safety cap on repair passes per file
- 102: _IMPORT_RE = re.compile(r"^(from\s+\S\|\bimport\s+\S)")
- 103: _DEF_RE = re.compile(r"^def\s+\w+\s*\(")
- 104: _ASYNC_DEF_RE = re.compile(r"^async\s+def\s+\w+\s*\(")
- 107: _BLOCK_OPENER_RE = re.compile(r":\s*(?:#.*)?$")
- 113: def _indent(line: str) -> int:
- 118: def _is_blank_or_comment(line: str) -> bool:
- 124: def _compile_check(path: Path) -> Optional[SyntaxError]:
- 127: source = path.read_text(encoding="utf-8", errors="replace")
- 134: def _parse_error_log(log_path: Path, project_root: Path) -> dict[Path, set[int]]:
- 167: def _context_indent(lines: list[str], idx: int, window: int = CONTEXT_WINDOW) -> int:
- 203: from collections import Counter
- 219: def _prev_nonblank_index(lines: list[str], idx: int) -> int:
- 227: def _preceding_block_indent(lines: list[str], idx: int) -> int:
- 251: def _is_import_or_simple_stmt(stripped: str) -> bool:
- 256: def pass_fix_orphan_imports(
- 345: def pass_indent_after_except(
- 391: def pass_fix_misindented_blocks(
- 404: def method(self):
- 406: from functools import reduce      # <-- wrong
- 522: def pass_fix_escaped_methods(
- 626: def _infer_method_indent(lines: list[str], idx: int) -> int:
- 643: from collections import Counter
- 647: def _find_block_end(lines: list[str], start: int, base_indent: int) -> int:
- 663: def pass_dedup_method_aliases(lines: list[str]) -> tuple[list[str], int]:
- 674: def repair_file(
- 758: def _compile_check_lines(lines: list[str]) -> Optional[SyntaxError]:
- 759: source = "".join(lines)
- 770: def main() -> int:

## scripts/fix_triple_quotes.py

- 21: from __future__ import annotations
- 23: import argparse
- 24: import pathlib
- 25: import re
- 26: import sys
- 28: TRIPLE_QUOTE_PATTERNS = [r'"""', r"'''"]
- 31: def normalize_raw_docstring_markers(text: str) -> str:
- 40: def ensure_balanced_triple_quotes(text: str) -> tuple[str, int]:
- 57: def _find_module_docstring_open(txt: str) -> tuple[int, str] \| None:
- 89: def rawify_if_escapes(txt: str) -> tuple[str, int]:
- 147: def process_file(path: pathlib.Path, dry_run: bool) -> int:
- 159: def main(argv: list[str] \| None = None) -> int:
- 205: raise SystemExit(main())

## scripts/generate_llms_architecture.py

- 29: from __future__ import annotations
- 31: import argparse
- 32: import pathlib
- 35: def _discover_architecture_docs(root: pathlib.Path) -> list[pathlib.Path]:
- 67: def _render_file(path: pathlib.Path, repo_root: pathlib.Path) -> str:
- 82: def main() -> int:
- 147: raise SystemExit(main())

## scripts/generate_project_dashboard.py

- 11: from __future__ import annotations
- 13: import json
- 14: import re
- 15: from datetime import datetime, timezone
- 16: from pathlib import Path
- 17: from typing import List, Set
- 19: RE_PLAN = re.compile(
- 23: ROOT = Path(__file__).resolve().parents[1]
- 24: PROJECTS_ROOT = ROOT / "docs" / "project"
- 25: PROJECTS_REGISTRY = ROOT / "data" / "projects.json"
- 26: RE_PROJECT_DIR = re.compile(r"^prj\d{7}(?:-.+)?$")
- 30: OUT_ROOT = PROJECTS_ROOT
- 34: def _normalize_topic_key(topic: str) -> str:
- 42: def _load_registry_topics() -> dict[str, str]:
- 68: def _extract_task_progress(plan_path: Path, project_dir: Path) -> tuple[int, int, List[str]]:
- 96: def _code_search_candidates(topic_key: str) -> Set[str]:
- 113: def _find_code_files(topic_key: str) -> List[Path]:
- 150: projects = []
- 151: registry_topics = _load_registry_topics()
- 154: project_dirs = sorted(
- 235: lines = [
- 245: def _color_yes_no(value: str) -> str:

## scripts/generate_test_data.py

- 5: def generate_sample_fixture(path: str) -> None:

## scripts/install_codeql.ps1

- 55: $ErrorActionPreference = "Stop"
- 62: $releaseInfo = Invoke-RestMethod `
- 65: $Version = $releaseInfo.tag_name   # e.g. "codeql-bundle-v2.20.3"
- 70: $semver = $Version -replace '^codeql-bundle-', ''
- 72: $assetName = "codeql-bundle-win64.tar.gz"
- 73: $downloadUrl = "https://github.com/github/codeql-action/releases/download/codeql-bundle-$semver/$assetName"
- 78: $tempFile = Join-Path $env:TEMP $assetName
- 90: $parentDir = Split-Path $InstallDir -Parent
- 99: $exePath = Join-Path $InstallDir "codeql.exe"
- 102: $nested = Join-Path $InstallDir "codeql\codeql.exe"

## scripts/prepend_async_note.py

- 1: import glob
- 3: prefix = (

## scripts/prepend_plan_note.py

- 1: import glob
- 3: prefix = (

## scripts/scaffold_new_layout.py

- 16: from pathlib import Path
- 18: NEW_DIRS = ["core", "agents", "interfaces", "tools", "plugins"]
- 21: def create_dirs(root: str \| Path = ".") -> None:
- 28: def main() -> None:

## scripts/security/run_secret_scan.py

- 17: from __future__ import annotations
- 19: import argparse
- 20: import sys
- 21: from pathlib import Path
- 23: REPO_ROOT = Path(__file__).resolve().parents[2]
- 27: from src.security.secret_scan_service import SecretScanService
- 30: def parse_args() -> argparse.Namespace:
- 43: def main() -> int:

## scripts/security/verify_no_key_material.py

- 17: from __future__ import annotations
- 19: from pathlib import Path
- 21: SCAN_PATHS = ("rust_core", "docs/security")
- 22: KNOWN_KEY_ARTIFACT = Path("rust_core/2026-03-11-keys.priv")
- 25: def has_known_key_artifact() -> bool:
- 35: def main() -> int:
- 50: raise SystemExit(main())

## scripts/setup_deployment.py

- 4: import os
- 7: def create_deployment_structure(root: str) -> None:

## scripts/setup_governance.py

- 15: import os
- 16: from pathlib import Path
- 19: def ensure_file(path: Path, header: str) -> None:
- 25: def main():

## scripts/setup_structure.py

- 8: import os
- 11: def create_core_structure(root: str) -> None:

## scripts/setup_tests.py

- 3: import os
- 6: def create_test_structure(root: str) -> None:

## scripts/validate_project_implementation.py

- 14: from __future__ import annotations
- 16: import re
- 17: from pathlib import Path
- 18: from typing import List, Tuple
- 20: ROOT = Path(__file__).resolve().parents[1]
- 21: PROJECTS_ROOT = ROOT / "docs" / "project"
- 23: CHECKBOX_RE = re.compile(r"^[\s\-\*]+\[([ xX])\]")
- 26: def _check_plan(path: Path) -> Tuple[int, int, List[str]]:
- 49: def main() -> None:
- 83: raise SystemExit(1)

## scripts/write_readme.py

- 20: from __future__ import annotations
- 22: import argparse
- 23: import json
- 24: import re
- 25: from pathlib import Path
- 28: def _load_project_counts(projects_path: Path) -> tuple[int, int]:
- 35: def _update_readme_counts(content: str, total_projects: int, released_projects: int) -> str:
- 49: def _parse_args() -> argparse.Namespace:
- 73: def main() -> int:
- 79: raise FileNotFoundError(f"README not found: {readme_path}")
- 81: raise FileNotFoundError(f"Project registry not found: {projects_path}")
- 104: raise SystemExit(main())

## scripts/codestructure_governance.py

- 15: from __future__ import annotations
- 17: import argparse
- 18: import re
- 19: from pathlib import Path
- 22: def _repo_root() -> Path:
- 26: def _normalize_rel(path: Path, root: Path) -> str:
- 30: def _parse_manifest_split_files(manifest_path: Path) -> dict[str, str]:
- 43: def _target_split_file(rel_path: str, split_map: dict[str, str]) -> str:
- 50: def _matches_anchor(ext: str, stripped: str) -> bool:
- 93: def _extract_anchors(file_path: Path) -> list[tuple[int, str]]:
- 125: def _remove_section(lines: list[str], rel_path: str, heading_prefix: str) -> list[str]:
- 153: def _append_section(lines: list[str], rel_path: str, heading_prefix: str, anchors: list[tuple[int, str]]) -> list[str]:
- 165: def _rewrite_split_file(path: Path, rel_path: str, heading_prefix: str, anchors: list[tuple[int, str]]) -> None:
- 173: def _heading_for_split(split_filename: str) -> str:
- 178: def _all_split_filenames(split_map: dict[str, str]) -> list[str]:
- 190: def main() -> int:
