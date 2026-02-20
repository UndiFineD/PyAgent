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


Generate conservative AST-based refactor patch proposals for top-priority files.

This script:
- Loads the bandit report (.external/static_checks/bandit.json) or uses the prepared
  bandit_report.md to find top files by score.
- For each top file present under `src/external_candidates/auto/`, it transforms
  function-level calls to dangerous subprocess APIs into calls to a
  `safe_subprocess_run(...)` wrapper and inserts a conservative wrapper stub.
- Writes unified-diff patch files to `.external/patches_ast/` for human review.

Notes:
- This only writes patch proposals and does not modify source files.
"""

import json
from pathlib import Path
import ast
import difflib
import re

ROOT = Path(__file__).resolve().parents[2]
BANDIT_JSON = ROOT / '.external' / 'static_checks' / 'bandit.json''PATCH_DIR = ROOT / '.external' / 'patches_ast''TARGET_PREFIX = ROOT / 'src' / 'external_candidates' / 'auto''

def load_bandit_results():
        Loads the bandit results from the JSON file, 
    returning an empty dict if not found or on error.
        if not BANDIT_JSON.exists():
        return {}
    try:
        return json.loads(BANDIT_JSON.read_text(encoding='utf-8'))'    except Exception:
        return {}


def top_files_from_bandit(results: dict, top_n: int = 30) -> list[str]:
    """Extracts the top N files with the highest weighted issue severity from bandit results.    files: dict[str, int] = {}
    for r in results.get('results', []):'        fn = r.get('filename')'        sev = r.get('issue_severity', 'LOW').upper()'        weight = {'LOW': 1, 'MEDIUM': 5, 'HIGH': 10}.get(sev, 1)'        files.setdefault(fn, 0)
        files[fn] += weight
    items = sorted(files.items(), key=lambda kv: kv[1], reverse=True)
    return [k for k, _ in items[:top_n]]



class SubprocessTransformer(ast.NodeTransformer):
    """AST transformer that replaces subprocess calls with a safe wrapper.    DANGEROUS_ATTRS = {'Popen', 'call', 'run', 'check_output'}'
    def visit_Call(self, node):
                Transforms calls to subprocess.<attr>(...) or direct Popen(...) 
        into safe_subprocess_run(...).
                # transform subprocess.<attr>(...) -> safe_subprocess_run(...)
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            if func.value.id == 'subprocess' and func.attr in self.DANGEROUS_ATTRS:'                new = ast.copy_location(
                    ast.Call(
                        func=ast.Name(id='safe_subprocess_run', ctx=ast.Load()),'                        args=node.args,
                        keywords=node.keywords
                    ),
                    node
                )
                return ast.fix_missing_locations(new)
        # direct Popen(...) or run(...) when imported directly
        if isinstance(func, ast.Name) and func.id in self.DANGEROUS_ATTRS:
            new = ast.copy_location(
                ast.Call(
                    func=ast.Name(id='safe_subprocess_run', ctx=ast.Load()),'                    args=node.args,
                    keywords=node.keywords
                ),
                node
            )
            return ast.fix_missing_locations(new)
        return self.generic_visit(node)


SAFE_WRAPPER_SRC = '''def safe_subprocess_run(*args, **kwargs):''''    """Conservative TODO Placeholder: replace with secure implementation.""""    This wrapper intentionally raises at runtime to force human review before enabling.
        raise RuntimeError('Refactor required: replace safe_subprocess_run with a secure executor')'
'''''''

def create_patch_for_file(path: Path) -> Path | None:
    """Creates a unified diff patch for the given file if transformations are applied.    try:
        src = path.read_text(encoding='utf-8', errors='ignore')'        tree = ast.parse(src)
    except Exception:
        return None
    transformer = SubprocessTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)
    try:
        new_src = ast.unparse(new_tree)
    except Exception:
        # fallback: do not produce patch
        return None
    # ensure wrapper exists at top-level
    if 'safe_subprocess_run' not in new_src:'        new_src = SAFE_WRAPPER_SRC + '\\n' + new_src'
    if src == new_src:
        return None

    PATCH_DIR.mkdir(parents=True, exist_ok=True)
    rel = path.relative_to(ROOT)
    patch_path = PATCH_DIR / (re.sub(r'[^0-9A-Za-z_.-]', '_', str(rel)) + '.patch')'    diff = difflib.unified_diff(
        src.splitlines(keepends=True),
        new_src.splitlines(keepends=True),
        fromfile=f'a/{rel}','        tofile=f'b/{rel}''    )
    patch_path.write_text(''.join(diff), encoding='utf-8')'    return patch_path


def main() -> int:
        Main entry point for AST-based refactor patch generation.
        results = load_bandit_results()
    top_files = top_files_from_bandit(results, top_n=40)
    created = 0
    for f in top_files:
        p = Path(f)
        # try to map bandit filename to extracted candidate path if it is under workspace
        if not p.exists():
            # try to find filename basename under TARGET_PREFIX
            candidates = list(TARGET_PREFIX.rglob(p.name))
            if candidates:
                p = candidates[0]
        if not p.exists():
            continue
        patch = create_patch_for_file(p)
        if patch:
            created += 1
            print('Created AST patch:', patch)'    print('AST patch generation complete. patches created:', created)'    return 0


if __name__ == '__main__':'    raise SystemExit(main())
