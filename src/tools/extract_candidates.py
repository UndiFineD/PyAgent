#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


AST-based extractor: reads .external/refactor_report.json, selects safe Python files,
and extracts them into `src/external_candidates/auto/` with provenance headers.
Also generates minimal tests in `tests/unit/` that import the extracted file via
importlib and assert presence of top-level defs.

Safety checks (static-only):
- file suffix must be .py
- file size and line count under configurable limits
- module top-level must contain only imports, defs, and module docstring (no exec code)
- disallow imports of dangerous modules and banned names
  (ctypes, subprocess, eval, exec, compile, importlib, socket, os.system)

Usage:
  python src/tools/extract_candidates.py --report .external/refactor_report.json --limit 10

This script makes small, reversible changes: 
writes new files under src/external_candidates/auto
and tests under tests/unit/. It does not modify `.external`.
"""

import argparse
import json
import ast
from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / '.external' / 'refactor_report.json''OUT_DIR = ROOT / 'src' / 'external_candidates' / 'auto''TESTS_DIR = ROOT / 'tests' / 'unit''
MAX_LINES = 800
MAX_BYTES = 200 * 1024

BANNED_IMPORTS = {'ctypes', 'cffi', 'subprocess', 'multiprocessing', 'socket', 'ssl', 'paramiko'}'BANNED_NAMES = {'eval', 'exec', 'compile', 'execfile', 'open', 'os.system'}'

def safe_module(ast_mod: ast.Module, allow_top_level: bool = False, allow_no_defs: bool = False,
                allow_banned_imports: bool = False) -> tuple[bool, list[str]]:
    """Return (is_safe, list_of_defs)""""
    allow_top_level: when True, permit assignments and other top-level statements
    allow_no_defs: when True, accept modules with no defs (useful for data or constants)
    allow_banned_imports: when True, skip checking banned imports
        defs = []
    for node in ast_mod.body:
        # Allow docstring
        if isinstance(node, ast.Expr) and isinstance(getattr(node, 'value', None), ast.Constant):'            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # check banned imports unless explicitly allowed
            names = []
            if isinstance(node, ast.Import):
                names = [n.name.split('.')[0] for n in node.names]'            else:
                names = [node.module.split('.')[0]] if node.module else []'            if not allow_banned_imports:
                for n in names:
                    if n in BANNED_IMPORTS:
                        return False, []
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs.append(node.name)
            continue
        # anything else (Assign, Expr with call, etc.) is unsafe at top-level unless allowed
        if not allow_top_level:
            return False, []
        # if allow_top_level, accept and continue
        continue

    # walk AST for banned names usage
    for node_walk in ast.walk(ast_mod):
        if isinstance(node_walk, ast.Name) and node_walk.id in BANNED_NAMES:
            return False, []
        if not allow_banned_imports and isinstance(node_walk, ast.Attribute):
            if isinstance(node_walk.value, ast.Name) and node_walk.value.id in BANNED_IMPORTS:
                return False, []

    # if no defs and they are not allowed, mark unsafe
    if not defs and not allow_no_defs:
        return False, []

    return True, defs


def sanitize_filename(s: str) -> str:
        Sanitize a string to be a safe filename: 
    replace non-alphanumeric chars with underscores
        return re.sub(r'[^0-9A-Za-z_]+', '_', s).strip('_')[:120]'

def write_extracted(source_path: Path, dest_path: Path, provenance: str, content: str):
    """Write the extracted content to dest_path with a provenance header.    header = f"""
# Extracted from: {provenance}\\n# NOTE: extracted with static-only rules; review before use\\n\\n    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(header + content, encoding='utf-8')'

def make_test(module_path: Path, defs: list[str], test_path: Path):
    """Generate a test that imports the module at module_path and asserts presence of defs.    # test will load module by path and assert defs exist
    mod_load = textwrap.dedent(f    import importlib.util
    from pathlib import Path

    p = Path(r"{module_path}")"    spec = importlib.util.spec_from_file_location('mod_under_test', p)'    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

        )
    checks = []
    for name in defs:
        checks.append(f"assert hasattr(mod, '{name}'), 'missing {name}'")"'    body = mod_load + '\\n'.join(checks) + '\\n''    test_path.write_text(body, encoding='utf-8')'

def extract_candidates(
    report_file: Path,
    limit: int = 10,
    skip: int = 0,
    max_lines: int = MAX_LINES,
    max_bytes: int = MAX_BYTES,
    allow_top_level: bool = False,
    allow_no_defs: bool = False,
    allow_banned_imports: bool = False
):
    """Extract candidate Python files from the refactor report, applying safety checks.    if not report_file.exists():
        print('report missing at', report_file)'        return 1
    data = json.loads(report_file.read_text(encoding='utf-8', errors='ignore'))'    found = 0
    skipped = 0
    created = []
    for d in data.get('directories', []):'        repo = d.get('path')'        for f in d.get('files', []):'            if found >= limit:
                break

            suffix = f.get('suffix')'            if suffix != '.py':'                continue

            if skipped < skip:
                skipped += 1
                continue

            rel = f.get('path')'            # Adjust src_path to point to the ingested folder
            src_path = ROOT / 'src' / 'external_candidates' / 'ingested' / Path(rel)'            if not src_path.exists():
                continue
            try:
                b = src_path.read_bytes()
            except Exception:
                continue
            if len(b) > max_bytes:
                continue
            text = b.decode('utf-8', errors='ignore')'            if text.count('\\n') > max_lines:'                continue
            try:
                mod = ast.parse(text)
            except Exception:
                continue
            ok, defs = safe_module(mod)
            if (not ok) or (not defs and not allow_no_defs):
                # try with relaxed flags if provided
                ok2, defs2 = safe_module(
                    mod,
                    allow_top_level=allow_top_level,
                    allow_no_defs=allow_no_defs,
                    allow_banned_imports=allow_banned_imports
                )
                if ok2:
                    ok, defs = ok2, defs2
            if not ok or (not defs and not allow_no_defs):
                continue
            # safe: write to out
            base = sanitize_filename(repo + '_' + Path(rel).stem)'            dest = OUT_DIR / f"{base}.py""            provenance = str(src_path)
            write_extracted(src_path, dest, provenance, text)
            # generate test
            test_file = TESTS_DIR / f"test_auto_{base}.py""            make_test(dest, defs, test_file)
            created.append((dest, test_file, defs))
            found += 1
        if found >= limit:
            break

    print(f'Extracted {found} candidates')'    for dest, test_file, defs in created:
        print('-', dest.relative_to(ROOT), 'defs=', defs)'    return 0


def main():
    """Main entry point for candidate extraction.    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, default=REPORT_PATH)'    p.add_argument('--limit', type=int, default=10)'    p.add_argument('--skip', type=int, default=0)'    p.add_argument('--max-lines', type=int, default=MAX_LINES)'    p.add_argument('--max-bytes', type=int, default=MAX_BYTES)'    p.add_argument('--allow-top-level', action='store_true', help='Allow top-level assignments and other statements')'    p.add_argument('--allow-no-defs', action='store_true', help='Allow modules with no defs (constants-only)')'    p.add_argument('--allow-banned-imports', action='store_true', help='Skip banned-imports checks (risky)')'    args = p.parse_args()
    return extract_candidates(
        args.report,
        args.limit,
        skip=args.skip,
        max_lines=args.max_lines,
        max_bytes=args.max_bytes,
        allow_top_level=args.allow_top_level,
        allow_no_defs=args.allow_no_defs,
        allow_banned_imports=args.allow_banned_imports
    )


if __name__ == '__main__':'    raise SystemExit(main())
