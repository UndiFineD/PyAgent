#!/usr/bin/env python3
"""Generate prioritized bandit report and prepare AST-based refactor patch proposals.

Produces:
- .external/static_checks/bandit_report.md  (summary, prioritized)
- .external/patches/<sanitized_filename>.patch  (human-review patch proposals)

This script does NOT apply patches; it only writes suggestions for reviewers.
"""
from __future__ import annotations
import json
from pathlib import Path
import ast
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
BANDIT_JSON = ROOT / '.external' / 'static_checks' / 'bandit.json'
OUT_DIR = ROOT / '.external' / 'static_checks'
PATCH_DIR = ROOT / '.external' / 'patches'


SEVERITY_WEIGHT = {'LOW': 1, 'MEDIUM': 5, 'HIGH': 10}


def sanitize_name(p: Path) -> str:
    s = str(p).replace(':', '').replace('\\', '_').replace('/', '_')
    s = re.sub(r'[^0-9A-Za-z_.-]', '_', s)
    return s


def load_bandit() -> dict:
    if not BANDIT_JSON.exists():
        raise FileNotFoundError(f"{BANDIT_JSON} not found")
    return json.loads(BANDIT_JSON.read_text(encoding='utf-8'))


def aggregate(results: dict) -> dict:
    files: dict[str, dict] = {}
    for r in results.get('results', []):
        fn = r.get('filename')
        sev = r.get('issue_severity', 'LOW').upper()
        test = r.get('test_name')
        lineno = r.get('line_number')
        text = r.get('issue_text')
        files.setdefault(fn, {'count': 0, 'score': 0, 'findings': []})
        files[fn]['count'] += 1
        files[fn]['score'] += SEVERITY_WEIGHT.get(sev, 1)
        files[fn]['findings'].append({'severity': sev, 'test': test, 'line': lineno, 'text': text})
    return files


def make_report(agg: dict, top_n: int = 50) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PATCH_DIR.mkdir(parents=True, exist_ok=True)
    entries = sorted(agg.items(), key=lambda kv: kv[1]['score'], reverse=True)
    report = ["# Bandit Prioritized Report\n"]
    report.append(f"Generated patches directory: {PATCH_DIR}\n")
    report.append("\n## Top files by score\n")
    for i, (fn, meta) in enumerate(entries[:top_n], 1):
        report.append(f"\n### {i}. {fn}\n")
        report.append(f"- Findings: {meta['count']}  |  Score: {meta['score']}\n")
        for f in meta['findings']:
            report.append(f"  - [{f['severity']}] L{f.get('line')} {f['test']}: {f['text']}\n")
        # create a patch proposal
        try:
            create_patch_proposal(fn, meta['findings'])
            report.append(f"- Patch proposal: .external/patches/{sanitize_name(Path(fn))}.patch\n")
        except Exception as e:
            report.append(f"- Patch creation failed: {e}\n")

    out = OUT_DIR / 'bandit_report.md'
    out.write_text('\n'.join(report), encoding='utf-8')


def create_patch_proposal(filename: str, findings: list[dict]) -> None:
    p = Path(filename)
    if not p.exists():
        # skip if file not present in workspace (bandit referenced external path)
        return
    text = p.read_text(encoding='utf-8', errors='ignore').splitlines()
    patches: list[str] = []
    patches.append(f"--- a/{filename}")
    patches.append(f"+++ b/{filename}")
    # For each finding, produce a conservative replacement suggestion
    handled_lines = set()
    for f in findings:
        ln = f.get('line') or 0
        sev = f.get('severity')
        desc = f.get('text', '')
        # show context
        start = max(0, ln - 3 - 1)
        end = min(len(text), ln + 2)
        patches.append(f"@@ -{start+1},{end-start} +{start+1},{end-start}")
        for idx in range(start, end):
            orig = text[idx]
            if (idx + 1) == ln and (idx + 1) not in handled_lines:
                # suggest conservative replacement for dangerous calls/imports
                suggestion = suggest_replacement(orig)
                patches.append(f"-{orig}")
                patches.append(f"+{suggestion}  # PATCH_PROPOSAL: {sev} {desc}")
                handled_lines.add(idx + 1)
            else:
                patches.append(f" {orig}")
    outp = PATCH_DIR / f"{sanitize_name(p)}.patch"
    outp.write_text('\n'.join(patches), encoding='utf-8')


def suggest_replacement(line: str) -> str:
    # naive heuristics: detect eval/exec/compile or import of banned modules
    s = line.strip()
    if re.search(r"\beval\s*\(", s) or re.search(r"\bexec\s*\(", s):
        return "raise RuntimeError('Refactor required: remove eval/exec; see .external/patches')"
    if re.match(r"from\s+\w+\s+import|import\s+\w+", s):
        # comment out import as conservative proposal
        return f"# TODO: remove or replace risky import -> {s}"
    if 'subprocess' in s or 'Popen' in s or 'os.system' in s:
        return "raise RuntimeError('Refactor required: avoid running subprocesses directly')"
    # default: add TODO comment
    return s + "  # TODO: review this line for safety"


def main() -> int:
    data = load_bandit()
    agg = aggregate(data)
    make_report(agg)
    print('Wrote report and patch proposals to .external/static_checks and .external/patches')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
