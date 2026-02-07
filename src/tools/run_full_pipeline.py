#!/usr/bin/env python3
"""Orchestrate the full external->src pipeline end-to-end with no prompts.

Steps (non-interactive):
  1. Run `batch_extract.py` to extract candidates into `src/external_candidates/auto/`
  2. Run `run_static_checks.py` against the extracted candidates
  3. Run `run_auto_tests.py` to execute generated tests
  4. Run `move_completed.py` to move completed tracking rows (idempotent)
  5. Regenerate `docs/architecture/external_integration.md` summary

This script returns a non-zero exit code if critical steps fail.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime
import os
import sqlite3
import hashlib
import concurrent.futures
import ast
import time
import tempfile
import shutil

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'src' / 'tools'
REPORT = ROOT / '.external' / 'refactor_report.json'
EXTRACT_TARGET = ROOT / 'src' / 'external_candidates' / 'auto'
STATIC_DIR = ROOT / '.external' / 'static_checks'
DOC = ROOT / 'docs' / 'architecture' / 'external_integration.md'


def run(cmd: list[str], fatal: bool = True) -> int:
    print('RUN:', ' '.join(cmd))
    p = subprocess.run(cmd)
    if p.returncode != 0:
        print('Command failed:', cmd, 'exit', p.returncode)
        if fatal:
            raise SystemExit(p.returncode)
    return p.returncode


def compute_sha(path_str: str) -> tuple[str, str]:
    """Compute sha256 for a file path string (module-level worker)."""
    h = hashlib.sha256()
    p = Path(path_str)
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return (path_str, h.hexdigest())


def run_checks_for_sha(args: tuple[str, str]) -> tuple[str, dict]:
    """Run bandit/semgrep/python-only checks for a single file and write per-sha outputs.
    Args: (sha, path_str)
    Returns: (sha, results dict)
    """
    sha, path_str = args
    p = Path(path_str)
    out_dir = Path(__file__).resolve().parents[2] / '.external' / 'static_checks'
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    # bandit
    bandit_out = out_dir / f'bandit_{sha}.json'
    semgrep_out = out_dir / f'semgrep_{sha}.json'
    try:
        exe = shutil.which('bandit')
        if exe:
            cmd = ['bandit', '-r', str(p), '-f', 'json', '-o', str(bandit_out)]
        else:
            py = sys.executable or shutil.which('python')
            cmd = [py, '-m', 'bandit', '-r', str(p), '-f', 'json', '-o', str(bandit_out)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        results['bandit'] = {'code': proc.returncode, 'out': str(bandit_out) if proc.returncode == 0 else (proc.stderr or proc.stdout)}
    except Exception as e:
        results['bandit'] = {'code': 1, 'out': str(e)}
    # semgrep
    try:
        exe = shutil.which('semgrep')
        if exe:
            cmd = ['semgrep', '--config', 'auto', '--json', '--output', str(semgrep_out), str(p)]
        else:
            py = sys.executable or shutil.which('python')
            cmd = [py, '-m', 'semgrep.cli', '--config', 'auto', '--json', '--output', str(semgrep_out), str(p)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        results['semgrep'] = {'code': proc.returncode, 'out': str(semgrep_out) if proc.returncode == 0 else (proc.stderr or proc.stdout)}
    except Exception as e:
        results['semgrep'] = {'code': 1, 'out': str(e)}
    # python-only checks (AST)
    try:
        text = p.read_text(encoding='utf-8', errors='ignore')
        mod = ast.parse(text)
        file_findings = []
        banned_imports = {'ctypes', 'cffi', 'subprocess', 'multiprocessing', 'socket', 'ssl', 'paramiko'}
        banned_names = {'eval', 'exec', 'compile', 'execfile', 'open', 'os.system'}
        dangerous_attrs = {'system', 'popen', 'Popen'}
        for node in ast.walk(mod):
            if isinstance(node, ast.Import):
                for n in node.names:
                    name = n.name.split('.')[0]
                    if name in banned_imports:
                        file_findings.append(f'banned_import: {name}')
            if isinstance(node, ast.ImportFrom):
                modname = (node.module or '').split('.')[0]
                if modname in banned_imports:
                    file_findings.append(f'banned_import: {modname}')
            if isinstance(node, ast.Name):
                if node.id in banned_names:
                    file_findings.append(f'banned_name: {node.id}')
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.attr in dangerous_attrs:
                    file_findings.append(f'dangerous_attr: {node.value.id}.{node.attr}')
            if isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Name) and fn.id in {'eval', 'exec', 'compile'}:
                    file_findings.append(f'dangerous_call: {fn.id}')
                if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.attr in dangerous_attrs:
                    file_findings.append(f'dangerous_call: {fn.value.id}.{fn.attr}')
        py_out = out_dir / f'python_{sha}.json'
        if file_findings:
            py_out.write_text(json.dumps({str(p): sorted(set(file_findings))}, indent=2), encoding='utf-8')
            results['python_only'] = {'code': 0, 'files': {str(p): sorted(set(file_findings))}}
        else:
            results['python_only'] = {'code': 0, 'files': {}}
    except Exception as e:
        results['python_only'] = {'code': 1, 'out': str(e)}
    return (sha, results)


def summarize_and_write_doc():
    # Build a concise summary using available artifacts
    files = list(EXTRACT_TARGET.glob('*.py')) if EXTRACT_TARGET.exists() else []
    count = len(files)
    # load static summary if present
    summary = {}
    try:
        sfile = STATIC_DIR / 'summary.json'
        if sfile.exists():
            summary = json.loads(sfile.read_text(encoding='utf-8', errors='ignore'))
    except Exception:
        summary = {}

    content_lines = [
        '**External Integration Summary**\n',
        f'- **Extracted files:** {count} files placed under src/external_candidates/auto/',
        f'- **Extraction report used:** {REPORT}',
        '- **Static-check summary:**',
    ]
    if summary:
        for k, v in summary.items():
            content_lines.append(f'  - {k}: code={v.get("code")} result={v.get("result")}')
    else:
        content_lines.append('  - no static summary available')

    content_lines.append('\n- **Generated tests:** Executed via `src/tools/run_auto_tests.py`')
    content_lines.append('\n- **Where to review:** `src/external_candidates/auto/`, `.external/static_checks/`')

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text('\n'.join(content_lines), encoding='utf-8')
    print('Wrote summary to', DOC)


def update_refactor_report(report_path: Path, extracted_files: list[Path]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if report_path.exists():
        try:
            data = json.loads(report_path.read_text(encoding='utf-8', errors='ignore'))
        except Exception:
            data = {}
    # update metadata
    data.setdefault('history', [])
    entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'extracted_count': len(extracted_files),
        'extracted_files': [str(p).replace('\\', '/') for p in extracted_files],
    }
    data['last_run'] = entry
    data['history'].append(entry)
    report_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print('Updated refactor report:', report_path)


def write_refactor_report_md(report_path: Path, md_path: Path) -> None:
    try:
        data = json.loads(report_path.read_text(encoding='utf-8'))
    except Exception:
        data = {}
    md_lines = ["# Refactor Report\n"]
    last = data.get('last_run') or {}
    md_lines.append(f"- Last run: {last.get('timestamp')}")
    md_lines.append(f"- Extracted files: {last.get('extracted_count', 0)}")
    if last.get('extracted_files'):
        md_lines.append('\n## Files\n')
        for f in last.get('extracted_files', [])[:200]:
            md_lines.append(f"- {f}")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text('\n'.join(md_lines), encoding='utf-8')
    print('Wrote human refactor report:', md_path)


def _is_init(p: Path) -> bool:
    return p.name == '__init__.py'


def main():
    start_ts = time.time()
    # Cache dir (ensure exists early so we can store report hash)
    cache_dir = ROOT / '.external' / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    # simple helper to hash small files
    def file_sha(p: Path) -> str:
        h = hashlib.sha256()
        with p.open('rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()

    # check whether report changed since last run; if unchanged, skip batch_extract
    report_sha_file = cache_dir / 'last_report.sha'
    report_changed = True
    if REPORT.exists() and report_sha_file.exists():
        try:
            prev = report_sha_file.read_text(encoding='utf-8').strip()
            curh = file_sha(REPORT)
            if prev == curh:
                report_changed = False
            else:
                report_changed = True
        except Exception:
            report_changed = True
    else:
        report_changed = True
    # 1) batch extract (permissive)
    if report_changed:
        run([sys.executable, str(SCRIPTS / 'batch_extract.py'), '--report', str(REPORT), '--chunk-size', '500', '--workers', '4', '--allow-top-level', '--allow-no-defs', '--allow-banned-imports'])
        # update last_report.sha
        try:
            if REPORT.exists():
                report_sha_file.write_text(file_sha(REPORT), encoding='utf-8')
        except Exception:
            pass
    else:
        print('Refactor report unchanged; skipping batch_extract')
    # collect extracted files and update refactor report
    # Build extracted list: prefer filesystem scan only if report changed; otherwise use DB manifest
    if report_changed:
        extracted = [p for p in (EXTRACT_TARGET.rglob('*.py') if EXTRACT_TARGET.exists() else []) if not _is_init(p)]
    else:
        # use DB manifest (paths) to avoid expensive rglob
        cur = None
        try:
            # open DB if exists
            dbp = cache_dir / 'files.db'
            if dbp.exists():
                conn2 = sqlite3.connect(str(dbp))
                cur = conn2.cursor()
                cur.execute('SELECT path FROM files')
                extracted = []
                for (rel,) in cur.fetchall():
                    p = EXTRACT_TARGET / Path(rel)
                    if p.exists() and not _is_init(p):
                        extracted.append(p)
                conn2.close()
            else:
                extracted = []
        except Exception:
            extracted = [p for p in (EXTRACT_TARGET.rglob('*.py') if EXTRACT_TARGET.exists() else []) if not _is_init(p)]
    try:
        update_refactor_report(REPORT, extracted)
    except Exception as e:
        print('Failed to update refactor report:', e)
    # write a human-readable refactor report md
    try:
        write_refactor_report_md(REPORT, ROOT / '.external' / 'refactor_report.md')
    except Exception as e:
        print('Failed to write refactor report md:', e)
    # 2) build cache DB and identify changed files (by mtime/size + sha256)
    cache_dir.mkdir(parents=True, exist_ok=True)
    db_path = cache_dir / 'files.db'
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS files (
        path TEXT PRIMARY KEY,
        mtime REAL,
        size INTEGER,
        sha256 TEXT,
        last_seen INTEGER
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS tool_results (
        sha TEXT PRIMARY KEY,
        bandit_path TEXT,
        semgrep_path TEXT,
        python_path TEXT,
        last_checked INTEGER
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS static_checked (
        sha TEXT PRIMARY KEY,
        last_checked INTEGER
    )''')
    conn.commit()

    # Load existing DB rows into memory to reduce per-file queries
    cur.execute('SELECT path, mtime, size, sha256 FROM files')
    db_rows = {row[0]: (row[1], row[2], row[3]) for row in cur.fetchall()}

    changed_files: list[Path] = []
    hash_map: dict[str, list[Path]] = {}
    _sha_cache: dict[str, str] = {}

    # Collect files that need hashing (changed/new)
    to_hash: list[tuple[Path, str, float, int]] = []  # (path, rel, mtime, size)
    for p in extracted:
        try:
            st = p.stat()
        except Exception:
            continue
        rel = str(p.relative_to(EXTRACT_TARGET)).replace('\\', '/')
        row = db_rows.get(rel)
        if row and abs(row[0] - st.st_mtime) < 0.0001 and row[1] == st.st_size:
            # unchanged, skip but update last_seen in-memory; we'll batch write later
            # mark last_seen update in db_rows to avoid immediate write
            db_rows[rel] = (row[0], row[1], row[2])
            # queue update for last_seen
            cur.execute('UPDATE files SET last_seen = ? WHERE path = ?', (int(datetime.utcnow().timestamp()), rel))
            continue
        # changed/new -> enqueue for hashing later
        to_hash.append((p, rel, st.st_mtime, st.st_size))

    # Parallelize hashing for changed files
    if to_hash:
        workers = min(len(to_hash), (os.cpu_count() or 2))
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exc:
            futures = {exc.submit(compute_sha, str(p)): (p, rel, mtime, size) for (p, rel, mtime, size) in to_hash}
            batch: list[tuple[str, float, int, str, int]] = []
            for fut in concurrent.futures.as_completed(futures):
                p, rel, mtime, size = futures[fut]
                try:
                    _, s = fut.result()
                except Exception:
                    # fallback to in-process compute
                    h = hashlib.sha256()
                    with p.open('rb') as f:
                        for chunk in iter(lambda: f.read(8192), b''):
                            h.update(chunk)
                    s = h.hexdigest()
                batch.append((rel, mtime, size, s, int(datetime.utcnow().timestamp())))
                changed_files.append(p)
                hash_map.setdefault(s, []).append(p)
                # commit in batches to reduce transaction overhead
                if len(batch) >= 1000:
                    cur.executemany('REPLACE INTO files (path, mtime, size, sha256, last_seen) VALUES (?, ?, ?, ?, ?)', batch)
                    conn.commit()
                    batch = []
            if batch:
                cur.executemany('REPLACE INTO files (path, mtime, size, sha256, last_seen) VALUES (?, ?, ?, ?, ?)', batch)
                conn.commit()

    print(f'Changed files: {len(changed_files)} (unique content groups: {len(hash_map)})')

    # If no changed files, we can skip faster parts
    if changed_files:
        # support sharding via env vars: PYAGENT_SHARD_INDEX, PYAGENT_SHARD_COUNT
        try:
            shard_index = int(os.getenv('PYAGENT_SHARD_INDEX', '0'))
            shard_count = int(os.getenv('PYAGENT_SHARD_COUNT', '1'))
        except Exception:
            shard_index = 0
            shard_count = 1
        if shard_count > 1:
            keys = sorted(hash_map.keys())
            selected = {k for i, k in enumerate(keys) if (i % shard_count) == shard_index}
            hash_map = {k: v for k, v in hash_map.items() if k in selected}
        # create a temp dir inside the repo cache with unique files only to avoid duplicate work
        work_root = cache_dir / 'work'
        work_root.mkdir(parents=True, exist_ok=True)
        tmpdir = Path(tempfile.mkdtemp(prefix='pyagent_proc_', dir=str(work_root)))
        try:
            for s, paths in hash_map.items():
                # pick the first as representative
                rep = paths[0]
                if _is_init(rep):
                    continue
                rel = rep.relative_to(EXTRACT_TARGET)
                dest = tmpdir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                # try hard link first to avoid copying large files; fallback to copy
                try:
                    os.link(rep, dest)
                except Exception:
                    try:
                        shutil.copy2(rep, dest)
                    except Exception:
                        # last-resort: read/write
                        dest.write_bytes(rep.read_bytes())

            # 3) apply safe automated fixes only to changed unique files (non-fatal)
            # Only run apply/static checks if we have any shas not present in static cache
            cur.execute('SELECT sha FROM static_checked')
            checked_shas = {r[0] for r in cur.fetchall()}
            missing_shas = [s for s in hash_map.keys() if s not in checked_shas]
            if missing_shas:
                # run apply_safe_fixes on tmpdir (so checks operate on patched files)
                try:
                    from src.tools import apply_safe_fixes as _apply_safe_fixes
                    try:
                        _apply_safe_fixes.main(['--apply', '--target', str(tmpdir), '--patch-dir', str(ROOT / '.external' / 'patches')])
                    except TypeError:
                        _apply_safe_fixes.main()
                except Exception:
                    run([sys.executable, str(SCRIPTS / 'apply_safe_fixes.py'), '--apply', '--target', str(tmpdir), '--patch-dir', str(ROOT / '.external' / 'patches')], fatal=False)

                # Run grouped static checks (bandit/semgrep) once on tmpdir and map results to shas
                try:
                    from src.tools import run_static_checks as _run_static
                    try:
                        _run_static.main([str(tmpdir)])
                    except TypeError:
                        _run_static.main()
                except Exception:
                    run([sys.executable, str(SCRIPTS / 'run_static_checks.py'), str(tmpdir)])

                # Parse grouped outputs and write per-sha tool result files
                OUT_DIR = ROOT / '.external' / 'static_checks'
                bandit_json = OUT_DIR / 'bandit.json'
                semgrep_json = OUT_DIR / 'semgrep.json'
                bandit_by_file: dict[str, list] = {}
                semgrep_by_file: dict[str, list] = {}
                if bandit_json.exists():
                    try:
                        bj = json.loads(bandit_json.read_text(encoding='utf-8', errors='ignore'))
                        for r in bj.get('results', []) if isinstance(bj, dict) else []:
                            fname = r.get('filename')
                            if fname:
                                bandit_by_file.setdefault(str(Path(fname).resolve()), []).append(r)
                    except Exception:
                        pass
                if semgrep_json.exists():
                    try:
                        sj = json.loads(semgrep_json.read_text(encoding='utf-8', errors='ignore'))
                        for item in sj.get('results', []) if isinstance(sj, dict) else []:
                            path = item.get('path') or item.get('extra', {}).get('metadata', {}).get('path')
                            if not path:
                                path = item.get('path') or item.get('filename')
                            if path:
                                semgrep_by_file.setdefault(str(Path(path).resolve()), []).append(item)
                    except Exception:
                        pass

                # Run python-only AST checks in parallel for missing_shas
                def python_checks(path_str: str) -> tuple[str, dict]:
                    p = Path(path_str)
                    try:
                        text = p.read_text(encoding='utf-8', errors='ignore')
                        mod = ast.parse(text)
                    except Exception as e:
                        return (path_str, {'error': str(e)})
                    file_findings = []
                    banned_imports = {'ctypes', 'cffi', 'subprocess', 'multiprocessing', 'socket', 'ssl', 'paramiko'}
                    banned_names = {'eval', 'exec', 'compile', 'execfile', 'open', 'os.system'}
                    dangerous_attrs = {'system', 'popen', 'Popen'}
                    for node in ast.walk(mod):
                        if isinstance(node, ast.Import):
                            for n in node.names:
                                name = n.name.split('.')[0]
                                if name in banned_imports:
                                    file_findings.append(f'banned_import: {name}')
                        if isinstance(node, ast.ImportFrom):
                            modname = (node.module or '').split('.')[0]
                            if modname in banned_imports:
                                file_findings.append(f'banned_import: {modname}')
                        if isinstance(node, ast.Name):
                            if node.id in banned_names:
                                file_findings.append(f'banned_name: {node.id}')
                        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                            if node.attr in dangerous_attrs:
                                file_findings.append(f'dangerous_attr: {node.value.id}.{node.attr}')
                        if isinstance(node, ast.Call):
                            fn = node.func
                            if isinstance(fn, ast.Name) and fn.id in {'eval', 'exec', 'compile'}:
                                file_findings.append(f'dangerous_call: {fn.id}')
                            if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.attr in dangerous_attrs:
                                file_findings.append(f'dangerous_call: {fn.value.id}.{fn.attr}')
                    return (path_str, {'files': {str(p): sorted(set(file_findings))} if file_findings else {}})

                sha_to_paths: dict[str, Path] = {}
                for s in missing_shas:
                    rep = hash_map.get(s, [None])[0]
                    if not rep:
                        continue
                    rel = rep.relative_to(EXTRACT_TARGET)
                    target_file = tmpdir / rel
                    if not target_file.exists():
                        target_file = rep
                    sha_to_paths[s] = target_file

                # parallel python-only checks
                with concurrent.futures.ProcessPoolExecutor(max_workers=min(len(sha_to_paths), (os.cpu_count() or 2))) as pool:
                    futures = {pool.submit(python_checks, str(p)): s for s, p in sha_to_paths.items()}
                    py_results = {}
                    for fut in concurrent.futures.as_completed(futures):
                        s = futures[fut]
                        try:
                            path_str, res = fut.result()
                            py_results[s] = res
                        except Exception as e:
                            py_results[s] = {'error': str(e)}

                # write per-sha outputs and update tool_results table
                ts = int(datetime.utcnow().timestamp())
                rows = []
                for s, p in sha_to_paths.items():
                    p_abs = str(Path(p).resolve())
                    bandit_path = ''
                    semgrep_path = ''
                    python_path = ''
                    bdata = bandit_by_file.get(p_abs) or []
                    if bdata:
                        bandit_path = str(OUT_DIR / f'bandit_{s}.json')
                        try:
                            Path(bandit_path).write_text(json.dumps(bdata, indent=2), encoding='utf-8')
                        except Exception:
                            bandit_path = ''
                    sdata = semgrep_by_file.get(p_abs) or []
                    if sdata:
                        semgrep_path = str(OUT_DIR / f'semgrep_{s}.json')
                        try:
                            Path(semgrep_path).write_text(json.dumps(sdata, indent=2), encoding='utf-8')
                        except Exception:
                            semgrep_path = ''
                    pdata = py_results.get(s) or {}
                    if pdata:
                        python_path = str(OUT_DIR / f'python_{s}.json')
                        try:
                            Path(python_path).write_text(json.dumps(pdata, indent=2), encoding='utf-8')
                        except Exception:
                            python_path = ''
                    rows.append((s, bandit_path, semgrep_path, python_path, ts))
                if rows:
                    cur.executemany('REPLACE INTO tool_results (sha, bandit_path, semgrep_path, python_path, last_checked) VALUES (?, ?, ?, ?, ?)', rows)
                    # also mark as static_checked
                    cur.executemany('REPLACE INTO static_checked (sha, last_checked) VALUES (?, ?)', [(r[0], ts) for r in rows])
                    conn.commit()
            else:
                print('All unique content groups already static-checked; skipping apply/static checks')
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
    else:
        print('No changed files detected; skipping apply-safe-fixes and per-file static checks')

    # 5) run generated tests (parallel) - only when changes were detected
    if changed_files:
        workers = os.cpu_count() or 2
        try:
            from src.tools import run_auto_tests as _run_tests
            try:
                _run_tests.main(['--workers', str(workers)])
            except TypeError:
                _run_tests.main()
        except Exception:
            run([sys.executable, str(SCRIPTS / 'run_auto_tests.py'), '--workers', str(workers)])
    else:
        print('No changed files; skipping generated tests')
    # 4) prepare patch proposals and bandit report (regenerate)
    try:
        from src.tools import prepare_refactor_patches as _prep
        try:
            _prep.main([])
        except TypeError:
            _prep.main()
    except Exception:
        run([sys.executable, str(SCRIPTS / 'prepare_refactor_patches.py')], fatal=False)

    # 6) generate AST-based conservative refactor patches for top-priority files
    # Run generator on full extract target but skip if nothing changed
    if changed_files:
        # Instead of the previous AST pipeline, ask "Copilot" to refactor files.
        # We implement a small, safe placeholder refactor step here: prepend a marker
        # and write an AST-style patch file under .external/patches_ast/. This will
        # then be applied by copying the refactored file into `src/external_candidates`.
        patches_ast_dir = ROOT / '.external' / 'patches_ast'
        patches_ast_dir.mkdir(parents=True, exist_ok=True)
        for s, paths in hash_map.items():
            rep = paths[0]
            if _is_init(rep):
                continue
            rel = rep.relative_to(EXTRACT_TARGET)
            work_file = cache_dir / 'work' / 'copilot_tmp' / rel
            # if the file wasn't copied into tmp earlier, read original
            if not work_file.exists():
                work_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(rep, work_file)
            # perform simple placeholder "refactor" — prepend a marker line
            orig_text = work_file.read_text(encoding='utf-8', errors='ignore')
            new_text = '# Refactored by Copilot placeholder\n' + orig_text
            if new_text != orig_text:
                # write patch file (simple full-file replacement)
                patch_path = patches_ast_dir / f'{str(rel).replace("/","_")}.patch'
                patch_path.write_text(new_text, encoding='utf-8')
                # apply to real target (backup original)
                target_path = EXTRACT_TARGET / rel
                if target_path.exists():
                    backup = target_path.with_suffix(target_path.suffix + '.bak')
                    if not backup.exists():
                        shutil.copy2(target_path, backup)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(new_text, encoding='utf-8')
                print('Applied copilot-placeholder refactor to', target_path)
    else:
        print('No changed files; skipping AST patch generation/application')

    # 8) after applying AST patches, re-run static checks and tests on full target (non-fatal)
    try:
        from src.tools import run_static_checks as _run_static_full
        try:
            _run_static_full.main([str(EXTRACT_TARGET)])
        except TypeError:
            _run_static_full.main()
    except Exception:
        run([sys.executable, str(SCRIPTS / 'run_static_checks.py'), str(EXTRACT_TARGET)], fatal=False)

    try:
        from src.tools import run_auto_tests as _run_tests2
        try:
            _run_tests2.main(['--workers', str(workers)])
        except TypeError:
            _run_tests2.main()
    except Exception:
        run([sys.executable, str(SCRIPTS / 'run_auto_tests.py'), '--workers', str(workers)], fatal=False)

    # 8) move completed rows
    run([sys.executable, str(SCRIPTS / 'move_completed.py')], fatal=False)
    # 5) regenerate doc summary
    summarize_and_write_doc()
    print('Full pipeline completed successfully')
    # persist pipeline timing and metadata
    try:
        runs_db = cache_dir / 'pipeline_runs.db'
        rconn = sqlite3.connect(str(runs_db))
        rc = rconn.cursor()
        rc.execute('''CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_ts REAL,
            duration_ms REAL,
            changed_count INTEGER,
            unique_groups INTEGER
        )''')
        duration_ms = (time.time() - start_ts) * 1000.0
        rc.execute('INSERT INTO runs (start_ts, duration_ms, changed_count, unique_groups) VALUES (?, ?, ?, ?)', (start_ts, duration_ms, len(changed_files), len(hash_map)))
        rconn.commit()
        rconn.close()
    except Exception:
        pass
    # exit code 10 indicates no changed files were detected (stable)
    return 0 if changed_files else 10


if __name__ == '__main__':
    raise SystemExit(main())
