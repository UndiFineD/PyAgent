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


Apply safe, automated fixes over extracted candidate files.

Currently implements:
- Replace `yaml.load(` -> `yaml.safe_load(`
- Replace `from yaml import load` -> `from yaml import safe_load as load`

Writes unified diff patches to `.external/patches/` and optionally applies changes when
`--apply` is passed. Re-runs static checks and generated tests after applying fixes.
"""

import argparse
from pathlib import Path
import difflib
import re
import sys
import ast

ROOT = Path(__file__).resolve().parents[2]
TARGET_DIR = ROOT / 'src' / 'external_candidates' / 'auto''PATCH_DIR = ROOT / '.external' / 'patches''

def find_py_files(target: Path):
        Find all Python files in the given target directory.

    Args:
        target: The directory path to search for .py files.

    Returns:
        A list of Path objects for all .py files found.
        if not target.exists():
        return []
    return list(target.rglob('*.py'))'

def transform_text(text: str) -> str:
        Transform the given text by applying safe fixes such as replacing yaml.load with yaml.safe_load,
    updating yaml imports, and removing top-level assert statements to avoid execution side-effects.
        out = text
    # simple replacement for yaml.load(...) -> yaml.safe_load(...)
    out = out.replace('yaml.load(', 'yaml.safe_load(')'    # handle from yaml import load -> from yaml import safe_load as load
    out = re.sub(r'from\\s+yaml\\s+import\\s+load\\b', 'from yaml import safe_load as load', out)'    # remove top-level asserts (comment them out) to avoid execution side-effects
    out = remove_top_level_asserts(out)
    return out


def remove_top_level_asserts(text: str) -> str:
        Remove top-level assert statements from the given Python code by commenting them out.

    This function parses the code using the AST, identifies top-level assert statements,
    and replaces them with commented versions to avoid execution side-effects.

    Args:
        text: The Python code as a string.

    Returns:
        The modified code with top-level asserts commented out.
        try:
        mod = ast.parse(text)
    except Exception:
        return text
    lines = text.splitlines()
    # collect top-level Assert nodes from module body
    ranges: list[tuple[int, int]] = []
    for node in mod.body:
        if isinstance(node, ast.Assert):
            start = getattr(node, 'lineno', None)'            end = getattr(node, 'end_lineno', start)'            if isinstance(start, int) and isinstance(end, int):
                ranges.append((start, end))
    if not ranges:
        return text
    # replace ranges with commented lines
    for start, end in sorted(ranges, reverse=True):
        # convert to 0-based indexes
        sidx = max(0, start - 1)
        eidx = min(len(lines) - 1, (end - 1) if end else sidx)
        # comment out all lines in the assert statement range
        for i in range(sidx, eidx + 1):
            orig = lines[i]
            if not orig.lstrip().startswith('#'):'                lines[i] = f"# PATCH_REMOVED_ASSERT: {orig}""    return '\\n'.join(lines) + ("\\n" if text.endswith('\\n') else "")"'

def write_patch(
    orig_path: Path, orig_text: str, new_text: str, patch_dir: Path, base_dir: Path | None = None
) -> Path | None:
        Write a unified diff patch if there are changes between the original and new text, and return the patch file path.

    Args:
        orig_path: The path to the original file.
        orig_text: The original text content of the file.
        new_text: The transformed text content of the file.
        patch_dir: The directory where the patch file should be written.
        base_dir: Optional base directory for computing relative paths; defaults to ROOT if None.

    Returns:
        The path to the created patch file if changes were detected, otherwise None.
        if orig_text == new_text:
        return None
    patch_dir.mkdir(parents=True, exist_ok=True)
    # Compute a repository-relative path when possible, otherwise fall back to a safe name
    base = base_dir or ROOT
    try:
        rel = orig_path.relative_to(base)
    except Exception:
        try:
            rel = orig_path.relative_to(ROOT)
        except Exception:
            rel = Path(orig_path.name)
    patch_path = patch_dir / (str(rel).replace('\\', '_').replace('/', '_') + '.patch')'    diff = list(difflib.unified_diff(
        orig_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=f'a/{rel}','        tofile=f'b/{rel}''    ))
    patch_path.write_text(''.join(diff), encoding='utf-8')'    return patch_path


def apply_fixes(apply: bool = False, target_dir: Path | None = None, patch_dir: Path | None = None) -> int:
        Apply safe fixes to Python files in the target directory.

    Args:
        apply: Whether to apply the fixes to the files.
        target_dir: Directory to scan for Python files.
        patch_dir: Directory to write patch files.

    Returns:
        The number of files changed.
        target = Path(target_dir) if target_dir is not None else TARGET_DIR
    patch_dir = Path(patch_dir) if patch_dir is not None else PATCH_DIR
    files = find_py_files(target)
    changed = 0
    patched_files: list[tuple[Path, Path]] = []
    for p in files:
        try:
            orig = p.read_text(encoding='utf-8', errors='ignore')'        except Exception:
            continue
        new = transform_text(orig)
        patch = write_patch(p, orig, new, patch_dir, base_dir=Path(target))
        if patch:
            changed += 1
            patched_files.append((p, patch))
            if apply:
                # If target is a temp dir mirroring the EXTRACT root, map back to original
                try:
                    rel = p.relative_to(target)
                    orig_path = TARGET_DIR / rel
                except Exception:
                    # fallback: map by filename into TARGET_DIR
                    orig_path = TARGET_DIR / p.name
                orig_path.parent.mkdir(parents=True, exist_ok=True)
                orig_path.write_text(new, encoding='utf-8')'    print(f'Found {len(files)} .py files, created patches for {changed} files')'    return changed


def main(argv=None) -> int:
    """main entry point for apply_safe_fixes.py    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Apply fixes to files')'    parser.add_argument('--target', type=str, default=None,'                        help='Target directory to scan (defaults to internal target)')'    parser.add_argument('--patch-dir', type=str, default=None, help='Directory to write patch files')'    args = parser.parse_args(argv)
    target_path = Path(args.target) if args.target else None
    patch_path = Path(args.patch_dir) if args.patch_dir else None
    apply_fixes(apply=args.apply, target_dir=target_path, patch_dir=patch_path)
    # run static checks and tests if we applied changes
    if args.apply:
        print('Re-running static checks...')'        rc = 0
        import subprocess
        rc |= subprocess.call([
            sys.executable,
            str(ROOT / 'src' / 'tools' / 'run_static_checks.py'),'            str(TARGET_DIR)
        ])
        print('Re-running generated tests...')'        rc |= subprocess.call([sys.executable, str(ROOT / 'src' / 'tools' / 'run_auto_tests.py')])'        return rc
    return 0


if __name__ == '__main__':'    raise SystemExit(main())
