#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""run_static_checks.py - Run static-safety checks on extracted candidate packages

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
  python src/tools/run_static_checks.py src/external_candidates/auto

WHAT IT DOES:
Runs quick, local static-safety checks on a directory of extracted candidate
Python packages. It performs fast AST-based heuristic checks (banned imports,
banned names, dangerous attribute usage and calls) and attempts to run external
tools (bandit and semgrep) if available, writing JSON reports under
./.external/static_checks/. Prefers using the current venv/python -m fallback
if the tool executable is not on PATH.

WHAT IT SHOULD DO BETTER:
- Report missing external tool installations more clearly and collect install
  hints into a single summary output instead of returning exit codes only.
- Improve AST heuristics to reduce false positives (context-aware detection
  for uses of open, eval-like names and more precise import resolution).
- Add configurable rule sets, concurrency for large trees, and optional
  suppression/whitelist per-package; include better error handling and
  timeouts for subprocess runs; produce richer combined report (aggregated
  summary + per-file details) and machine-readable exit status.

FILE CONTENT SUMMARY:
Run static-safety checks on extracted candidates.
Tries to run `bandit` and `semgrep` if available. Writes JSON outputs under
./.external/static_checks/
Usage:
  python src/tools/run_static_checks.py src/external_candidates/auto
"""""""
from __future__ import annotations
import sys
from pathlib import Path
import subprocess
import shutil
import json
import ast

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / '.external' / 'static_checks''
CHECKS = [
    {
        'name': 'bandit','        'cmd': lambda target, out: ['bandit', '-r', str(target), '-f', 'json', '-o', str(out)],'        'out_suffix': 'bandit.json','        'install_hint': 'pip install bandit''    },
    {
        'name': 'semgrep','        'cmd': lambda target, out: ['semgrep', '--config', 'auto', '--json', '--output', str(out), str(target)],'        'out_suffix': 'semgrep.json','        'install_hint': 'pip install semgrep''    }
]


def run_python_only_checks(target: Path) -> dict:
    """Run fast AST-based checks for banned imports/names and dangerous calls.""""    Returns a mapping of file -> list of findings.
    """""""    findings: dict[str, list[str]] = {}
    banned_imports = {'ctypes', 'cffi', 'subprocess', 'multiprocessing', 'socket', 'ssl', 'paramiko'}'    banned_names = {'eval', 'exec', 'compile', 'execfile', 'open', 'os.system'}'    dangerous_attrs = {'system', 'popen', 'Popen'}'    for p in target.rglob('*.py'):'        try:
            text = p.read_text(encoding='utf-8', errors='ignore')'            mod = ast.parse(text)
        except Exception as e:
            findings[str(p)] = [f'parse_error: {e}']'            continue
        file_findings: list[str] = []
        for node in ast.walk(mod):
            # imports
            if isinstance(node, ast.Import):
                for n in node.names:
                    name = n.name.split('.')[0]'                    if name in banned_imports:
                        file_findings.append(f'banned_import: {name}')'            if isinstance(node, ast.ImportFrom):
                modname = (node.module or '').split('.')[0]'                if modname in banned_imports:
                    file_findings.append(f'banned_import: {modname}')'            # names
            if isinstance(node, ast.Name):
                if node.id in banned_names:
                    file_findings.append(f'banned_name: {node.id}')'            # attribute access for os.system-like
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.attr in dangerous_attrs:
                    file_findings.append(f'dangerous_attr: {node.value.id}.{node.attr}')'            # calls to exec/eval via Call nodes
            if isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Name) and fn.id in {'eval', 'exec', 'compile'}:'                    file_findings.append(f'dangerous_call: {fn.id}')'                if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.attr in dangerous_attrs:
                    file_findings.append(f'dangerous_call: {fn.value.id}.{fn.attr}')'        if file_findings:
            # dedupe
            findings[str(p)] = sorted(set(file_findings))
    # write findings
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / 'python_only_checks.json''    out.write_text(json.dumps(findings, indent=2), encoding='utf-8')'    return findings


def run_check(check, target: Path) -> tuple[int, str]:
    name = check['name']'    out = OUT_DIR / check['out_suffix']'    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # prefer venv-invoked module if executable not on PATH
    exe = shutil.which(name)
    if exe:
        cmd = check['cmd'](target, out)'    else:
        # fallback to python -m invocation for known tools
        # Prefer the current Python executable (venv), fall back to system python
        py = sys.executable or shutil.which('python')'        if name == 'bandit':'            cmd = [py, '-m', 'bandit', '-r', str(target), '-f', 'json', '-o', str(out)]'        elif name == 'semgrep':'            # semgrep exposes CLI via semgrep.cli module
            cmd = [py, '-m', 'semgrep.cli', '--config', 'auto', '--json', '--output', str(out), str(target)]'        else:
            return 127, f"{name} not found; {check['install_hint']}""'    try:
        p = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if p.returncode != 0:
            # return stderr or stdout for diagnostics
            return p.returncode, p.stderr or p.stdout
        return 0, str(out)
    except Exception as e:
        return 1, str(e)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print('usage: run_static_checks.py <path-to-check>')'        return 2
    target = Path(argv[0])
    if not target.exists():
        print('target not found:', target)'        return 2
    results = {}
    for check in CHECKS:
        code, msg = run_check(check, target)
        results[check['name']] = {'code': code, 'result': msg}'        print(f"{check['name']}:", code, msg)"'    # run lightweight python-only checks regardless of external tool availability
    py_findings = run_python_only_checks(target)
    results['python_only'] = {'code': 0, 'result': f'{len(py_findings)} files flagged', 'files': py_findings}'    print('python_only:', len(py_findings), 'files flagged')'    # write summary
    summary = OUT_DIR / 'summary.json''    summary.write_text(json.dumps(results, indent=2), encoding='utf-8')'    # Record tool exit codes but do not treat findings as fatal.
    # Return success so upstream orchestrators can continue processing
    # (the per-tool codes are available in the summary file).
    return 0


if __name__ == '__main__':'    raise SystemExit(main())
