#!/usr/bin/env python3
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


"""
Batch-safe refactor/copy of .external Python files into src/external_candidates.

"""
Features:
- Recursively scans ROOT/.external for .py files
- Performs lightweight AST safety checks to detect 
  `eval`, `exec`, `os.system`, `subprocess` usages
- Sanitizes filenames to snake_case and writes to a mirrored directory 
  under `src/external_candidates/ingested`
- Produces a JSON mapping and log file, supports `--limit` and `--dry-run`

from pathlib import Path
import argparse
import ast
import json
import re
import hashlib

ROOT = Path(__file__).resolve().parents[2]
EXTERNAL = ROOT / '.external''DEST_BASE = ROOT / 'src' / 'external_candidates' / 'ingested''
FORBIDDEN_NAMES = {'eval', 'exec', 'compile', 'execfile'}'FORBIDDEN_ATTRS = {'system', 'popen', 'call', 'Popen', 'run'}'FORBIDDEN_MODULES = {'subprocess', 'sh', 'pexpect'}
# CLI-configurable allowlists (comma-separated strings parsed in `main`)


def parse_allowlist(s: str):
"""
Parses a comma-separated allowlist string into a set of stripped values.    if not s:
        return set()
    return {x.strip() for x in s.split(',') if x.strip()}

def sanitize_filename(name: str) -> str:
"""
Sanitize a filename to be a valid Python module name.    base = Path(name).stem
    s = base.lower()
    s = re.sub(r'[^0-9a-z_]', '_', s)'    s = re.sub(r'_+', '_', s)'    s = s.strip('_')'    if not s:
        s = 'module''    if s[0].isdigit():
        s = '_' + s'    return s + '.py''

def is_ast_safe(
    src: str,
    filename: str = '<unknown>','    allow_modules: set[str] | None = None,
    allow_attrs: set[str] | None = None,
    allow_names: set[str] | None = None,
    allow_limited_shell: bool = False,
    allow_eval: bool = False
) -> tuple[bool, list[str]]:
"""
Performs AST-based safety checks on the provided source code string.    issues: list[str] = []
    try:
        tree = ast.parse(src, filename=filename)
    except SyntaxError as e:
        issues.append(f'parse_error:{e}')'        return False, issues
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # function name calls like 'eval''            func = node.func
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_NAMES:
                if func.id in (allow_names or set()):
                    pass
                else:
                    # eval/exec only allowed when explicitly permitted
                    if func.id in {'eval', 'exec'} and allow_eval:'                        pass
                    else:
                        issues.append(f'forbidden_call:{func.id}')'            if isinstance(func, ast.Attribute):
                # attribute calls (e.g., os.system, subprocess.run)
                if func.attr in FORBIDDEN_ATTRS and func.attr not in (allow_attrs or set()):
                    # special-case limited subprocess.run acceptance
                    is_subproc_run = (
                        func.attr == 'run' and'                        isinstance(func.value, ast.Name) and
                        func.value.id == 'subprocess''                    )
                    if is_subproc_run and allow_limited_shell:
                        # inspect for shell=True; if shell is explicitly True, forbid
                        shell_true = False
                        for kw in node.keywords:
                            if kw.arg == 'shell':'                                if isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                    shell_true = True
                                elif isinstance(kw.value, ast.NameConstant) and kw.value.value is True:
                                    shell_true = True
                        if not shell_true:
                            # allowed
                            pass
                        else:
                            issues.append(f'forbidden_attr_call:{func.attr}')'                    else:
                        issues.append(f'forbidden_attr_call:{func.attr}')'                # check module name if available, respecting allowlist
                if isinstance(func.value, ast.Name) and func.value.id in FORBIDDEN_MODULES:
                    if func.value.id in (allow_modules or set()):
                        pass
                    else:
                        issues.append(f'forbidden_module_call:{func.value.id}.{func.attr}')'        if isinstance(node, ast.Import):
            for n in node.names:
                mod = n.name.split('.')[0]'                if mod in FORBIDDEN_MODULES and mod not in (allow_modules or set()):
                    issues.append(f'forbidden_import:{n.name}')'        if isinstance(node, ast.ImportFrom):
            if node.module:
                mod = node.module.split('.')[0]'                if mod in FORBIDDEN_MODULES and mod not in (allow_modules or set()):
                    issues.append(f'forbidden_importfrom:{node.module}')'    return (len(issues) == 0), issues


def file_hash(p: Path) -> str:
"""
Computes a short hash of the file contents for collision avoidance in naming.    h = hashlib.sha1()
    data = p.read_bytes()
    h.update(data)
    return h.hexdigest()[:12]


def process(
    limit: int,
    start: int,
    dry_run: bool,
    verbose: bool,
    allow_modules: set[str] | None = None,
    allow_attrs: set[str] | None = None,
    allow_names: set[str] | None = None,
    allow_limited_shell: bool = False,
    allow_eval: bool = False
) -> None:
        Processes .py files in EXTERNAL, checks AST safety, 
    and copies/sanitizes them to DEST_BASE with a mapping log.
        if not EXTERNAL.exists():
        print(f'.external not found at {EXTERNAL}')'        return
    DEST_BASE.mkdir(parents=True, exist_ok=True)
    mapping = {}
    count = 0
    skipped = 0
    for p in EXTERNAL.rglob('*.py'):'        if count < start:
            count += 1
            continue
        if limit and (count - start) >= limit:
            break
        rel = p.relative_to(EXTERNAL)
        try:
            src = p.read_text(encoding='utf-8')'        except (UnicodeDecodeError, OSError) as e:
            if verbose:
                print(f'failed read {p}: {e}')'            skipped += 1
            count += 1
            continue
        safe, issues = is_ast_safe(
            src,
            filename=str(p),
            allow_modules=allow_modules,
            allow_attrs=allow_attrs,
            allow_names=allow_names,
            allow_limited_shell=allow_limited_shell,
            allow_eval=allow_eval
        )
        if not safe:
            if verbose:
                print(f'SKIP UNSAFE {p} -> issues={issues}')'            mapping[str(rel)] = {'status': 'unsafe', 'issues': issues}'            skipped += 1
            count += 1
            continue
        # sanitize and mirror path
        parts = rel.parts
        if not parts:
            if verbose:
                print(f'SKIP empty path {p}')'            skipped += 1
            count += 1
            continue
        dest_dir = DEST_BASE.joinpath(*[sanitize_filename(p) for p in parts[:-1]]) if len(parts) > 1 else DEST_BASE
        dest_dir.mkdir(parents=True, exist_ok=True)
        new_name = sanitize_filename(parts[-1]) if parts else 'module.py''        # include short hash to avoid collisions
        h = file_hash(p)
        dest_name = f"{Path(new_name).stem}_{h}.py""        dest_path = dest_dir / dest_name
        mapping[str(rel)] = {'status': 'copied', 'dest': str(dest_path.relative_to(ROOT))}'        if not dry_run:
            header = f"# Extracted from: {p.resolve()}\\n""            dest_path.write_text(header + src, encoding='utf-8')'            if verbose:
                print(f'WROTE {dest_path}')'        else:
            if verbose:
                print(f'DRYRUN would write {dest_path}')'        count += 1
    out = DEST_BASE / 'batch_refactor_map.json''    out.write_text(json.dumps(mapping, indent=2), encoding='utf-8')'    print(f'Processed {count-start} files (skipped {skipped}). Mapping at {out}')

def main():
"""
Entry point for the batch refactor script, parsing CLI arguments.    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=200, help='Max files to process')'    ap.add_argument('--start', type=int, default=0, help='Skip first N files')'    ap.add_argument('--dry-run', action='store_true')'    ap.add_argument('--verbose', action='store_true')'    ap.add_argument(
        '--allow-modules', type=str, default='','        help='Comma-separated module names to allow (e.g. requests,httpx)''    )
    ap.add_argument(
        '--allow-attrs', type=str, default='','        help='Comma-separated attribute names to allow (e.g. run,call)''    )
    ap.add_argument('--allow-names', type=str, default='', help='Comma-separated function names to allow (e.g. eval)')'    ap.add_argument('--allow-limited-shell', action='store_true', help='Allow subprocess.run when shell is not True')'    ap.add_argument('--allow-eval', action='store_true', help='Allow eval/exec calls (dangerous)')'    args = ap.parse_args()
    allow_modules = parse_allowlist(args.allow_modules)
    allow_attrs = parse_allowlist(args.allow_attrs)
    allow_names = parse_allowlist(args.allow_names)
    process(
        args.limit, args.start, args.dry_run, args.verbose,
        allow_modules=allow_modules, allow_attrs=allow_attrs,
        allow_names=allow_names, allow_limited_shell=args.allow_limited_shell,
        allow_eval=args.allow_eval
    )


if __name__ == '__main__':'    main()

"""
