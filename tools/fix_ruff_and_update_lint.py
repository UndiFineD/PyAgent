#!/usr/bin/env python3
import json
import subprocess
import shutil
from pathlib import Path
import sys
import datetime

ROOT = Path(__file__).resolve().parents[1]
LINT_FILE = ROOT / "lint_results.json"


def run_cmd(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True)
        return {"exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    except FileNotFoundError as e:
        return {"exit_code": 127, "stdout": "", "stderr": str(e)}


def normalize_entry(entry):
    # Move any top-level tool keys into a `tools` map for canonical shape
    tools = entry.get("tools") or {}
    for k in ("ruff", "mypy", "flake8"):
        if k in entry and k not in tools:
            tools[k] = entry.pop(k)
    entry["tools"] = tools
    return entry


def main():
    if not LINT_FILE.exists():
        print(f"lint results not found at {LINT_FILE}")
        sys.exit(1)

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    bak_ts = LINT_FILE.with_name(LINT_FILE.name + ".bak." + timestamp)
    shutil.copy2(LINT_FILE, bak_ts)
    print(f"backup written to {bak_ts}")

    data = json.loads(LINT_FILE.read_text())
    # normalize
    for entry in data:
        normalize_entry(entry)

    # collect files with ruff entries
    ruff_files = [e["file"] for e in data if "ruff" in e.get("tools", {})]
    print(f"ruff files to process: {len(ruff_files)}")

    modified_files = []
    for f in ruff_files:
        path = Path(f)
        # prefer repo-rooted path
        if not path.exists():
            path = ROOT / f
        print(f"running ruff --fix on: {path}")
        res_fix = run_cmd(["ruff", "--fix", str(path)])
        print(f"  ruff --fix exit={res_fix['exit_code']}")
        # run ruff check to get current status
        res_check = run_cmd(["ruff", "check", str(path)])
        # update data entry
        for entry in data:
            if entry["file"] == f:
                entry_tools = entry.setdefault("tools", {})
                entry_tools["ruff"] = {
                    "exit_code": res_check["exit_code"],
                    "stdout": res_check["stdout"],
                    "stderr": res_check["stderr"],
                }
                break
        if res_fix["exit_code"] == 0 or res_check["exit_code"] == 0:
            modified_files.append(str(path))

    # For files we modified (or attempted), re-run mypy and flake8 and update entries
    for path in modified_files:
        print(f"re-running mypy and flake8 for: {path}")
        mypy_res = run_cmd([sys.executable, "-m", "mypy", str(path)])
        flake_res = run_cmd([sys.executable, "-m", "flake8", str(path)])
        # find corresponding entry
        try:
            rel = str(Path(path).relative_to(ROOT))
        except Exception:
            rel = str(path)
        for entry in data:
            if entry["file"] == rel or entry["file"] == str(path):
                entry_tools = entry.setdefault("tools", {})
                entry_tools["mypy"] = {
                    "exit_code": mypy_res["exit_code"],
                    "stdout": mypy_res["stdout"],
                    "stderr": mypy_res["stderr"],
                }
                entry_tools["flake8"] = {
                    "exit_code": flake_res["exit_code"],
                    "stdout": flake_res["stdout"],
                    "stderr": flake_res["stderr"],
                }
                break

    # Remove tools that are successful (exit_code == 0 and empty stdout)
    remaining = []
    total_tool_entries = 0
    for entry in data:
        tools = entry.get("tools", {})
        for tool_name in list(tools.keys()):
            t = tools[tool_name]
            ec = t.get("exit_code")
            stdout = t.get("stdout", "") or ""
                # Consider a tool successful if it exited 0 (some tools print non-empty stdout on success)
                if ec == 0:
                tools.pop(tool_name, None)
        if tools:
            total_tool_entries += len(tools)
            remaining.append(entry)

    # write updated lint file
    out_ts = LINT_FILE.with_name(LINT_FILE.name + ".postruff." + timestamp)
    out_ts.write_text(json.dumps(remaining, indent=2))
    print(f"wrote updated lint_results to {out_ts}")
    print(f"remaining files: {len(remaining)}, remaining tool entries: {total_tool_entries}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except FileNotFoundError:
        return 127, '', f'Command not found: {cmd[0]}'


def run_ruff_json(path):
    py = sys.executable
    cmd = [py, '-m', 'ruff', 'check', '--format', 'json', str(path)]
    code, out, err = run_cmd(cmd)
    if out:
        try:
            return json.loads(out)
        except Exception:
            return []
    return []


def apply_simple_fixes(path: Path):
    changed = False
    findings = run_ruff_json(path)
    if not findings:
        return False

    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()

    # Helper to insert import asyncio if missing
    def ensure_asyncio():
        nonlocal lines, changed
        for ln in lines:
            if ln.strip().startswith('import asyncio') or ln.strip().startswith('from asyncio'):
                return
        # insert after shebang / encoding / module docstring / initial comments
        insert_at = 0
        # skip shebang
        if lines and lines[0].startswith('#!'):
            insert_at = 1
        # skip encoding or future imports
        while insert_at < len(lines) and (lines[insert_at].startswith('#') or lines[insert_at].startswith('from __future__') or lines[insert_at].strip() == ''):
            insert_at += 1
        lines.insert(insert_at, 'import asyncio')
        changed = True

    for f in findings:
        code = f.get('code') or f.get('rule_code') or ''
        message = f.get('message', '')
        # F401: unused import
        if code == 'F401' or 'imported but unused' in message:
            # try to extract name between backticks or after 'imported but unused'
            import re
            m = re.search(r'`([^`]+)`', message)
            name = None
            if m:
                name = m.group(1).split('.')[-1]
            else:
                m2 = re.search(r'([A-Za-z_][A-Za-z0-9_]*) imported but unused', message)
                if m2:
                    name = m2.group(1)

            if not name:
                continue

            # remove the name from any import line that contains it
            import_lines = []
            for idx, ln in enumerate(lines):
                if 'import ' in ln and name in ln:
                    import_lines.append(idx)

            for idx in reversed(import_lines):
                ln = lines[idx]
                # handle 'from X import a, b as c'
                if ln.strip().startswith('from ') and ' import ' in ln:
                    parts = ln.split(' import ', 1)
                    left, right = parts[0], parts[1]
                    # split by comma
                    items = [it.strip() for it in right.split(',')]
                    new_items = [it for it in items if it.split(' as ')[0].strip() != name]
                    if not new_items:
                        # remove entire line
                        lines.pop(idx)
                    else:
                        lines[idx] = left + ' import ' + ', '.join(new_items)
                    changed = True
                elif ln.strip().startswith('import '):
                    # 'import a, b'
                    items = [it.strip() for it in ln.replace('import ', '', 1).split(',')]
                    new_items = [it for it in items if it.split(' as ')[0].strip() != name]
                    if not new_items:
                        lines.pop(idx)
                    else:
                        lines[idx] = 'import ' + ', '.join(new_items)
                    changed = True

        # F821 undefined name asyncio -> add import
        if code == 'F821' and 'Undefined name' in message and 'asyncio' in message:
            ensure_asyncio()

    if changed:
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return changed


def main():
    p = Path('lint_results.json')
    if not p.exists():
        print('lint_results.json not found')
        return 2

    data = json.loads(p.read_text(encoding='utf-8'))
    # Collect files that have ruff entries
    files_with_ruff = [entry['file'] for entry in data if 'ruff' in entry]
    if not files_with_ruff:
        print('No ruff entries found')
        return 0

    py = sys.executable

    for rel in files_with_ruff:
        fp = Path(rel)
        print('Fixing ruff for', rel)
        # apply simple AST/text fixes first
        try:
            changed = apply_simple_fixes(fp)
            if changed:
                print('Applied simple fixes to', rel)
        except Exception as e:
            print('Error applying simple fixes to', rel, e)
        # Run ruff --fix via python -m ruff if available
        cmd = [py, '-m', 'ruff', 'check', '--fix', str(fp)]
        code, out, err = run_cmd(cmd)
        print('ruff exit', code)
        if out:
            print(out)
        if err:
            print(err)

    # After fixes, re-run ruff/flake8/mypy per affected file and update results
    updated = []
    for entry in data:
        f = entry['file']
        if f in files_with_ruff:
            new_entry = {'file': f}
            # ruff
            cmd = [py, '-m', 'ruff', 'check', str(Path(f))]
            code, out, err = run_cmd(cmd)
            if code != 0:
                new_entry['ruff'] = {'exit_code': code, 'stdout': out, 'stderr': err}
            # mypy
            cmd = [py, '-m', 'mypy', str(Path(f))]
            code, out, err = run_cmd(cmd)
            if code != 0:
                new_entry['mypy'] = {'exit_code': code, 'stdout': out, 'stderr': err}
            # flake8
            cmd = [py, '-m', 'flake8', str(Path(f))]
            code, out, err = run_cmd(cmd)
            if code != 0:
                new_entry['flake8'] = {'exit_code': code, 'stdout': out, 'stderr': err}
            updated.append(new_entry)
        else:
            # keep other entries unchanged
            updated.append(entry)

    # Remove entries that only contain 'file' (i.e., fully fixed)
    final = [e for e in updated if len(e.keys()) > 1]

    # Backup original
    p.with_suffix('.bak').write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
    p.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding='utf-8')

    print('Original files:', len(data))
    print('Remaining files after ruff fixes:', len(final))


if __name__ == '__main__':
    raise SystemExit(main())
